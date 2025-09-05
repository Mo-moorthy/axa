# PDF Form Extractor (with OCR Fallback)

A simple Python demo project for extracting key:value data from PDF forms, with OCR fallback.

## Features
- Configurable fields (regex-based)
- Rule-based extraction with pdfplumber
- OCR fallback with Tesseract for scanned PDFs
- SQLite storage
- Streamlit UI for upload and results
- Pytest tests

## Run
```
pip install -r requirements.txt
streamlit run app.py
```

Upload sample PDFs to see extracted fields.

## Config
Edit `config/fields.yml` (JSON content) to add or adjust extraction rules.
