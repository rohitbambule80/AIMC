from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.models import ChatRequest
from app.rag import ask_question
from app.ingest import ingest_pdf
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "message": "AIMC Running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_pdf(file_path)

    return {
        "message": "PDF uploaded successfully"
    }


@app.post("/chat")
def chat(req: ChatRequest):

    response = ask_question(req.question)

    return response
