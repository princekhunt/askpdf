from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile
from tools import generate_session_id, store_file
from db import insert_data, fetch_data, update_data
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from core import ask
from time import time
from tools import fetch_file_from_s3
import shutil
import uuid
import os

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://askpdf.bytespot.tech",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Constants
ALLOWED_CONTENT_TYPE = "application/pdf"
UPLOAD_DIRECTORY = "uploads"


# Root endpoint
@app.get("/")
def read_root():
    return {"success": True, "message": "Welcome to the AI Planet API"}

# accept pdf file and create a unique session and return the session id
@app.post("/upload/")
async def create_upload_file(file: UploadFile):
    if file.content_type != ALLOWED_CONTENT_TYPE:
        return JSONResponse(status_code=400, content={"success":False, "message": "Only pdf files are allowed"})

    # Generate a unique session ID
    session_id = generate_session_id()
    # Sanitize file name
    file.filename = file.filename.replace(" ", "_")
    
    #store locally
    file_path = os.path.join(UPLOAD_DIRECTORY, f"{session_id}.pdf")
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    #save data in database
    data = {
        'filename': file.filename,
        'upload_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'session': session_id,
        'active': True,
    }
    if insert_data('uploaded_documents', data) == False:
        return JSONResponse(status_code=500, content={"success":False, "message": "Error in storing data"})
    
    # Store the file S3 bucket
    object_name = f"{session_id}.pdf"
    if store_file(file_path, object_name) == False:
        return JSONResponse(status_code=500, content={"success":False, "message": "Error storing file"})

    # Remove the file from local storage
    os.remove(file_path)

    return {"success": True,
            "session_id": session_id}

# chat endpoint
@app.get("/chat/{session_id}")
async def read_chat(session_id: str, q: str = None):
    start = time()

    #sanitize session id
    try:
        session_id = uuid.UUID(session_id)
    except ValueError:
        return JSONResponse(status_code=400, content={"success":False, "message": "Invalid session ID"})

    # Fetch data from database
    data = fetch_data('uploaded_documents', str(session_id))
    if data == False:
        return JSONResponse(status_code=404, content={"success":False, "message": "Session ID not found"})

    if q is None:
        return {"success": False, "message": "Please provide a question"}
    
    #check if file exists in data folder
    file_path = f"data/{session_id}.pdf"
    if not os.path.exists(file_path):
        file_path = fetch_file_from_s3(session_id)
        if file_path is None:
            return JSONResponse(status_code=500, content={"success":False, "message": "Error fetching file"})    

    
    result = ask(q, session_id)
    return {"success": True, "session_id": session_id, "a": result}


#trash session
@app.delete("/trash/{session_id}")
async def delete_file(session_id: str):
    #sanitize session id
    try:
        session_id = uuid.UUID(session_id)
    except ValueError:
        return JSONResponse(status_code=400, content={"success":False, "message": "Invalid session ID"})

    # Fetch data from database
    data = fetch_data('uploaded_documents', str(session_id))
    if data == False:
        return JSONResponse(status_code=404, content={"success":False, "message": "Session ID not found"})

    #delete file from data folder
    file_path = f"data/{session_id}.pdf"
    if os.path.exists(file_path):
        os.remove(file_path)

    #remove vector data
    vector_data_path = "vector_data/{}".format(session_id)
    if os.path.exists(vector_data_path):
        shutil.rmtree(vector_data_path, ignore_errors=True)

    #update active to false in database
    data = {
        'active': False
    }
    if update_data('uploaded_documents', str(session_id), data) == False:
        return JSONResponse(status_code=500, content={"success":False, "message": "Error in updating data"})

    return {"success": True, "message": "Session trashed successfully"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)