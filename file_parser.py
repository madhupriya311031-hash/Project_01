from pathlib import Path

def extract_text_from_upload(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()

    if suffix == ".txt":
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")

    if suffix == ".pdf":
        import PyPDF2
        reader = PyPDF2.PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if suffix == ".docx":
        from docx import Document
        doc = Document(uploaded_file)
        return "\n".join(p.text for p in doc.paragraphs)

    raise ValueError("Unsupported file type.")
