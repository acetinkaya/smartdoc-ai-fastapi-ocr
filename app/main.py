from fastapi import FastAPI, UploadFile, File
import shutil
import os

from app.services.ocr_service import extract_text
from app.services.doc_analysis import analyze_document

app = FastAPI(
    title="SmartDoc AI API",
    description="OCR ve Akıllı Doküman İşleme Sistemi",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "SmartDoc AI API çalışıyor",
        "endpoints": {
            "OCR": "/ocr",
            "Health": "/health"
        }
    }


@app.get("/health")
def health():
    return {
        "status": "active",
        "service": "SmartDoc AI"
    }


@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR işlemi
    text = extract_text(file_path)

    # Analiz işlemi
    analysis = analyze_document(text)

    return {
        "filename": file.filename,
        "ocr_text": text,
        "analysis": analysis
    }
