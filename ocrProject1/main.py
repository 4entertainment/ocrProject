import os
from flask import Flask, render_template, request
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import time


app = Flask(__name__)

# Ana sayfa yolu için Flask route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            text, filename, elapsed_time = process_pdf(uploaded_file)  # PDF'i işleyip metne çevir ve dosya adını al
            return render_template('index.html', text=text, filename=filename, elapsed_time=elapsed_time)  # HTML şablonuna dosya adını da gönder
    return render_template('index.html', text=None)

# PDF dosyasını işle ve metni çıkar
def process_pdf(pdf_file):
    pdf_data = pdf_file.read()

    pdf_document = fitz.open(stream=pdf_data, filetype='pdf')
    text = ""

    start_time = time.time() # Record the start time

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        page_text = extract_text_from_page(page)  # Sayfadaki metni çıkar
        text += page_text

    end_time = time.time() # Record the end time
    elapsed_time = end_time - start_time

    return text, pdf_file.filename, elapsed_time  # Metni ve dosya adını döndür

# Sayfadaki metni çıkarma
def extract_text_from_page(page):
    image = page.get_pixmap()
    pil_image = Image.frombytes("RGB", (image.width, image.height), image.samples)
    page_text = pytesseract.image_to_string(pil_image, lang='tur')  # Tesseract ile metni çıkar
    return page_text

# Uygulamayı çalıştır
if __name__ == '__main__':
    app.run(debug=True)