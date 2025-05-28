"""
Resume parser module for extracting text from different file formats.
Focused on simplicity and effectiveness for cover letter generation.
"""

import io
import os
from typing import Dict, Any

import pdfplumber
import docx
from spacy import load
import docx2txt
import subprocess

# Load spaCy model for basic text processing
try:
    nlp = load("en_core_web_sm")
except:
    # Fallback in case the model is not installed
    import spacy
    nlp = spacy.blank("en")


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text(x_tolerance=3, y_tolerance=3)
                if page_text:
                    text += page_text + "\n\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX file using python-docx."""
    text = ""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""


def extract_text_from_doc(file_bytes: bytes) -> str:
    """Extract text from DOC file using antiword or docx2txt as fallback."""
    try:
        # Save temporarily
        temp_path = "temp_file.doc"
        with open(temp_path, "wb") as f:
            f.write(file_bytes)
        
        # First try with antiword if available
        try:
            text = subprocess.check_output(['antiword', temp_path]).decode('utf-8')
        except (subprocess.SubprocessError, FileNotFoundError):
            # Fallback to docx2txt
            try:
                text = docx2txt.process(temp_path)
            except:
                text = ""
                print("Failed to extract text from DOC file using available methods")
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from DOC: {e}")
        # Clean up in case of exception
        if os.path.exists("temp_file.doc"):
            os.remove("temp_file.doc")
        return ""


def process_resume_file(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """
    Process resume file and extract text based on file type.
    Returns a dictionary with the extracted text and metadata.
    """
    file_type = filename.lower().split('.')[-1]
    extracted_text = ""
    
    # Extract text based on file type
    if file_type == 'pdf':
        extracted_text = extract_text_from_pdf(file_bytes)
    elif file_type == 'docx':
        extracted_text = extract_text_from_docx(file_bytes)
    elif file_type == 'doc':
        extracted_text = extract_text_from_doc(file_bytes)
    else:
        return {
            "success": False,
            "text": "",
            "error": f"Unsupported file type: {file_type}"
        }
    
    # Basic processing with spaCy
    if extracted_text:
        # Apply some basic cleanup if needed
        doc = nlp(extracted_text)
        
        # We could extract entities, but keeping it simple for now
        # Just using spaCy for basic text normalization
        
        return {
            "success": True,
            "text": extracted_text,
            "word_count": len(doc),
            "file_type": file_type
        }
    else:
        return {
            "success": False,
            "text": "",
            "error": "Failed to extract text from file"
        }


def process_resume_text(text: str) -> Dict[str, Any]:
    """Process resume text that's directly provided."""
    if not text:
        return {
            "success": False,
            "text": "",
            "error": "No text provided"
        }
    
    doc = nlp(text)
    
    return {
        "success": True,
        "text": text,
        "word_count": len(doc)
    }
