import styles from "./Navbar.module.css";
import toast from "react-hot-toast";

let button = "upload"; //Button is acting as upload button

// Trash the session
function TrashSession() {
  toast.loading("Trashing session...");
  const session_id = localStorage.getItem("session");
  fetch("https://api.askpdf.bytespot.tech/trash/" + session_id, {
    method: "DELETE", // send DELETE request
    headers: {
      "Content-Type": "application/json",
      session_id: session_id,
    },
  })
    .then((response) => response.json())
    .then((result) => {
      if (result["success"] === true) {
        toast.dismiss();
        localStorage.removeItem("session"); // remove session from local storage
        toast.success("Session trashed successfully!", { duration: 3000 });
        setTimeout(() => {
          window.location.reload();
        }, 1000);
      } else if (result["success"] === false) {
        toast.dismiss(); //something went wrong from server side
        toast.error("Error: " + result["message"], { duration: 5000 });
      }
    })
    .catch((error) => {
      toast.dismiss();
      toast.error("Error: " + error, { duration: 5000 });
    });
}

function ActionFileUpload() {
  if (button === "trash") { //  If button is trash, then do nothing
    return;
  }
  //click the file input
  const fileInput = document.getElementsByName("FileUpload")[0];
  fileInput.click();
  UploadFile(); // Invoke the File Upload function
}

function UploadFile() {
  let fileInput = document.getElementsByName("FileUpload")[0];
  fileInput.removeEventListener("change", handleFileChange);
  function handleFileChange(event) {

    const file = event.target.files[0];
    const formData = new FormData();
    formData.append("file", file);
    toast.loading("Uploading file...");

    //Send the file to the server
    fetch("https://api.askpdf.bytespot.tech/upload", {
      method: "POST", // send POST request
      body: formData,
    })
      .then((response) => response.json())
      .then((result) => {
        if (result["success"] === true) {
          const session = result["session_id"];

          //save session in local storage
          localStorage.setItem("session", session);

          //enable the input field
          const input = document.getElementsByName("question")[0];
          input.disabled = false;
          toast.dismiss();
          toast.success("File uploaded successfully! You can chat now.", {
            duration: 5000,
          });

          //show file name
          const FileComponent = document.getElementById("FileComponent");
          FileComponent.style.display = "flex";
          const FileNameComponent = document.getElementById("FileName");
          FileNameComponent.innerHTML = file.name;


          //change the upload button to red trash button
          const UploadPDF = document.getElementById("UploadPDF");
          UploadPDF.innerHTML = "Trash Session";
          const UploadPDFButton = document.getElementById("UploadPDFButton");
          UploadPDFButton.style.backgroundColor = "#e87285";
          UploadPDFButton.removeEventListener("click", ActionFileUpload);
          UploadPDFButton.addEventListener("click", TrashSession);
          //onhover effect
          UploadPDFButton.addEventListener("mouseover", function () {
            UploadPDFButton.style.backgroundColor = "#e62544";
          });
          UploadPDFButton.addEventListener("mouseout", function () {
            UploadPDFButton.style.backgroundColor = "#e87285";
          });
          // Now button is for trashing, so upload mechanism is disabled
          button = "trash";
          //remove icon with trash icon
          const PlusIcon = document.getElementById("PlusIcon");
          PlusIcon.src = "trash.svg";
          fileInput.removeEventListener("change", handleFileChange);

          
        } else if (result["success"] === false) { // something went wrong from server side
          toast.dismiss();
          toast.error("Error: " + result["message"], { duration: 5000 });
        }
        fileInput.removeEventListener("change", handleFileChange);
      })

      .catch((error) => {
        toast.dismiss();
        toast.error("Error" + error, { duration: 5000 });
        fileInput.removeEventListener("change", handleFileChange);
      });
  }
  fileInput.addEventListener("change", handleFileChange);
}

const GroupComponent = () => {
  return (
    <nav>
      <div className={styles.title}>
        <img width="100px" src="askpdf.png" alt="logo" />
      </div>
      <input
        className={styles.FileInput}
        type="file"
        name="FileUpload"
        accept=".pdf"
      />

      <div id="FileComponent" className={styles.FileComponent}>
        <img
          id="FileIcon"
          className={styles.FileIcon}
          alt="FileIcon"
          src="FileIcon.svg"
        />
        <div id="FileName" className={styles.FileName}></div>
      </div>
      <button
        id="UploadPDFButton"
        onClick={ActionFileUpload}
        className={styles.NavbarGroup}
      >
        <div id="NavFrame" className={styles.NavFrame} />
        <img
          id="PlusIcon"
          className={styles.PlusIcon}
          alt=""
          src="PlusIcon.svg"
        />
        <div id="UploadPDF" className={styles.UploadPDF}>
          Upload PDF
        </div>
      </button>
    </nav>
  );
};

export default GroupComponent;
