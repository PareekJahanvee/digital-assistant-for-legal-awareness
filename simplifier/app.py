from flask import Flask, render_template, request
from preprocess import preprocess_text
from summarizer import summarize_text
from PyPDF2 import PdfReader
from docx import Document
import os
from database import init_db, save_document, get_all_documents, get_document, delete_document
from flask import redirect

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["GET", "POST"])
def summarize():
    summary_text = ""
    original_text = ""
    try:
        if request.method == "POST":
            file = request.files.get("file")
            if not file or not file.filename:
                summary_text = "Please upload a valid TXT, PDF or DOCX file."
            else:
                ext = os.path.splitext(file.filename)[1].lower()
                text = ""
                if ext == ".txt":
                    text = file.read().decode("utf-8", errors="ignore")
                elif ext == ".pdf":
                    reader = PdfReader(file)
                    text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
                elif ext == ".docx":
                    doc = Document(file)
                    text = "\n".join([p.text for p in doc.paragraphs])
                else:
                    summary_text = "Unsupported file type. Please upload TXT, PDF or DOCX."

                if text.strip():
                    original_text = text  # Save original
                    cleaned, chunks = preprocess_text(text)
                    summaries = [summarize_text(c) for c in chunks]
                    summary_text = " ".join(summaries)
                    title = os.path.splitext(file.filename)[0]
                    save_document(title, file.filename, original_text, summary_text)
                else:
                    summary_text = "Could not extract readable text from the document."

    except Exception as e:
        summary_text = f"Error: {str(e)}"

    return render_template(
        "summarize.html",
        summary=summary_text,
        original_text=original_text  # Pass original text
    )
    
@app.route("/dashboard")
def dashboard():
    documents = get_all_documents()
    return render_template("dashboard.html", documents=documents)

@app.route("/document/<int:doc_id>")
def view_document(doc_id):
    document = get_document(doc_id)
    return render_template("view_document.html", document=document)

@app.route("/delete/<int:doc_id>")
def delete(doc_id):
    delete_document(doc_id)
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)
