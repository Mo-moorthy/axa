import streamlit as st
from pathlib import Path
from extractor import FieldExtractor
from db import DB
import pandas as pd
import tempfile, os

st.title("PDF Form Extractor (with OCR Fallback)")

cfg_path = Path("config/fields.yml")
fx = FieldExtractor(cfg_path)
db = DB(Path("sample.db"))

uploaded_files = st.file_uploader("Upload PDF forms", type=["pdf"], accept_multiple_files=True)
if uploaded_files:
    all_results = []
    for uf in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uf.read())
            tmp.flush()
            doc_id = db.add_document(uf.name)
            matches = fx.extract_from_pdf(Path(tmp.name))
            db.add_extractions(doc_id, [(m.key, m.value, m.confidence, m.page, m.pattern) for m in matches])
            for m in matches:
                all_results.append({"filename": uf.name, "key": m.key, "value": m.value, "confidence": m.confidence, "page": m.page})
            os.unlink(tmp.name)
    st.write(pd.DataFrame(all_results))
