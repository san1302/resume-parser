# Resume Parser Service

A simple, focused Python service that extracts text from resume files (PDF, DOCX, DOC) to be used with HireGenie's cover letter generator.

## Features

- Extract text from PDF files using pdfplumber
- Extract text from DOCX files using python-docx
- Extract text from DOC files using textract
- Basic text processing with spaCy
- Simple REST API with FastAPI

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

4. For PDF text extraction, you'll need:
```bash
pip install pdfminer.six
```

5. For DOC file support, you'll need additional system dependencies:
```bash
# On Ubuntu/Debian
sudo apt-get install -y antiword unrtf poppler-utils pstotext tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig

# On macOS
brew install antiword unrtf poppler tesseract swig
```

## Running the service

Start the API server:
```bash
cd resume-parser
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

## API Usage

### Parse resume from file
```
POST /parse/file
```
- Upload a file using multipart/form-data
- Returns extracted text and metadata

### Parse resume text directly
```
POST /parse/text
```
- Send JSON with a "text" field
- Returns processed text and metadata

## Integration with HireGenie

The Next.js application can call this service to extract text from uploaded resume files before generating cover letters. Example integration:

```typescript
// In HireGenie's API route
async function extractResumeText(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/parse/file', {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error('Failed to extract resume text');
  }
  
  return await response.json();
}
``` 