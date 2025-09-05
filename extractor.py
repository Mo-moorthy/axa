import pdfplumber, re, yaml
from dataclasses import dataclass
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract

@dataclass
class Extraction:
    key: str
    value: str
    confidence: float
    page: int
    pattern: str

class FieldExtractor:
    def __init__(self, config_path: Path):
        import json
        if config_path.suffix in [".yml", ".yaml"]:
            with open(config_path, "r") as f:
                self.config = yaml.safe_load(f)
        else:
            with open(config_path, "r") as f:
                self.config = json.load(f)
        self.fields = self.config.get("fields", {})

    def extract_text_page(self, pdf_path: Path, page_num: int):
        """Try pdfplumber first, fallback to OCR"""
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                return text
        # OCR fallback
        images = convert_from_path(pdf_path, first_page=page_num+1, last_page=page_num+1)
        if images:
            return pytesseract.image_to_string(images[0])
        return ""

    def extract_from_pdf(self, pdf_path: Path):
        results = []
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)
        for pnum in range(num_pages):
            text = self.extract_text_page(pdf_path, pnum) or ""
            for key, field in self.fields.items():
                for pat in field.get("patterns", []):
                    m = re.search(pat, text, re.IGNORECASE)
                    if m:
                        val = m.group("val").strip()
                        conf = 0.9 if val else 0.5
                        results.append(Extraction(key, val, conf, pnum+1, pat))
                        break
        return results
