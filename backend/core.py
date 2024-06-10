from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ask(question, session):

    #get file from data folder
    file = "data/{}.pdf".format(session)
    loader = PyPDFLoader(file)
    pages = loader.load() # this will load a list of documents
    trimmed_pages = pages[0:len(pages)]
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 150
    )
    docs = text_splitter.split_documents(trimmed_pages)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="vector_data/{}".format(session)
    )

    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name='gpt-3.5-turbo',
        temperature=0.0
    )
    # conversational memory
    conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        #make it unique
        session_key=session,
        #remeber only last 1 message
        k=0,
        #do not save history of messages
        max_history=0, 
        config={"configurable":{
            "session_id": session,
        }},

        return_messages=True
    )
    # retrieval qa chain
    qa = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=vectordb.as_retriever(),
        memory=conversational_memory,
    )

    result = qa({"question": question})
    return result['answer']