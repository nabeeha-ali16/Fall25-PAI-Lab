import os
import re
from flask import Flask, render_template, request
from nlp_engine import load_dataset, calculate_similarity

from pypdf import PdfReader
PDF_SUPPORT = True

try:
    from docx import Document as DocxDocument
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATASET_PATH = os.path.join(BASE_DIR, "data", "dataset.txt")


def extract_text_from_file(file_path, filename):
    """Extract text from TXT, PDF, or DOCX files."""
    ext = os.path.splitext(filename)[1].lower()

    if ext == '.txt':
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    text = f.read()
                text = text.replace('\r\n', '\n').replace('\r', '\n')
                return text, None
            except UnicodeDecodeError:
                continue
        return None, "Could not read TXT file — try saving it as UTF-8."

    elif ext == '.pdf':
        if not PDF_SUPPORT:
            return None, "PDF support not installed. Run: pip install pypdf"
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            if not text.strip():
                return None, "Could not extract text from PDF."
            return text.strip(), None
        except Exception as e:
            return None, f"Error reading PDF: {str(e)}"

    elif ext == '.docx':
        if not DOCX_SUPPORT:
            return None, "DOCX support not installed. Run: pip install python-docx"
        try:
            doc = DocxDocument(file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            text = "\n\n".join(paragraphs)
            if not text.strip():
                return None, "DOCX file appears to be empty."
            return text, None
        except Exception as e:
            return None, f"Error reading DOCX: {str(e)}"

    else:
        return None, f"Unsupported file type: {ext}"


def highlight_text(text, plagiarized_words):
    if not plagiarized_words:
        return text

    word_set = set(w.lower() for w in plagiarized_words)

    def replacer(match):
        word = match.group(0)
        if word.lower() in word_set:
            return f'<mark class="plagiarized">{word}</mark>'
        return word

    return re.sub(r'\b[a-zA-Z]+\b', replacer, text)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    user_text = request.form.get('text')
    file = request.files.get('file')

    if file and file.filename != "":
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        extracted_text, error = extract_text_from_file(file_path, file.filename)

        if error:
            return render_template('result.html',
                                   similarity=0,
                                   matched_text=error,
                                   input_text="",
                                   highlighted_input="",
                                   highlighted_match="")

        user_text = extracted_text

    if not user_text or user_text.strip() == "":
        return render_template('result.html',
                               similarity=0,
                               matched_text="No input provided!",
                               input_text="",
                               highlighted_input="",
                               highlighted_match="")

    documents = load_dataset(DATASET_PATH)

    print("Dataset loaded:", documents)  

    if not documents:
        return render_template('result.html',
                               similarity=0,
                               matched_text="Dataset not found or empty!",
                               input_text=user_text,
                               highlighted_input="",
                               highlighted_match="")

    similarity, matched_doc, plagiarized_words = calculate_similarity(user_text, documents)

    highlighted_input = highlight_text(user_text, plagiarized_words)
    highlighted_match = highlight_text(matched_doc, plagiarized_words)

    return render_template('result.html',
                           input_text=user_text,
                           similarity=round(similarity, 2),
                           matched_text=matched_doc,
                           highlighted_input=highlighted_input,
                           highlighted_match=highlighted_match)


if __name__ == '__main__':
    app.run(debug=True)