"""
FastAPI app for resume parsing service.
Provides endpoints to extract text from resume files or directly process text.
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from .parser import process_resume_file, process_resume_text

app = FastAPI(title="Resume Parser API", 
              description="API for extracting text from resume files",
              version="1.0.0")

# Add CORS middleware to allow requests from our Next.js app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://hire-genie-git-main-sanchitagarwal0332-gmailcoms-projects.vercel.app", 
         "https://www.hiregenie.io" # Replace with your actual Vercel domain
        # "https://*.vercel.app"  # All Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextInput(BaseModel):
    """Model for direct text input."""
    text: str


@app.get("/")
def read_root():
    """Root endpoint with basic service info."""
    return {
        "service": "Resume Parser API",
        "status": "running",
        "endpoints": {
            "/parse/file": "Parse resume from file upload",
            "/parse/text": "Parse resume from text input"
        }
    }


@app.post("/parse/file")
async def parse_resume_file(
    file: UploadFile = File(...),
    max_size: Optional[int] = Form(5 * 1024 * 1024)  # 5MB default limit
):
    """
    Parse resume from uploaded file.
    Supports PDF, DOCX, and DOC formats.
    """
    # Validate file size
    file_size = 0
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > max_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {max_size} bytes."
        )
    
    # Validate file type
    filename = file.filename.lower()
    if not (filename.endswith('.pdf') or filename.endswith('.docx') or filename.endswith('.doc')):
        raise HTTPException(
            status_code=415,
            detail="Unsupported file type. Please upload a PDF, DOCX, or DOC file."
        )
    
    # Process the file
    result = process_resume_file(file_content, filename)
    
    if not result["success"]:
        raise HTTPException(
            status_code=422,
            detail=result.get("error", "Failed to process resume file.")
        )
    
    return result


@app.post("/parse/text")
async def parse_resume_text(input_data: TextInput):
    """
    Parse resume from direct text input.
    """
    if not input_data.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text input cannot be empty."
        )
    
    result = process_resume_text(input_data.text)
    
    if not result["success"]:
        raise HTTPException(
            status_code=422,
            detail=result.get("error", "Failed to process resume text.")
        )
    
    return result
