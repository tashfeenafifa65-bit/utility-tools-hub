from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import io
from pdf2image import convert_from_path
from zipfile import ZipFile
import tempfile
import shutil
from rembg import remove
from PIL import Image
import io
import os
import tempfile
from flask import request, send_file





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Simple Model for future features
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tools = [
        {'id': 'background-remover','name': 'AI Background Remover','description': 'Remove image backgrounds automatically using AI. Supports JPG, PNG and WEBP.','icon': 'fa-solid fa-scissors'},
        {'id': 'pdf-to-image','name': 'PDF to Image Converter','description': 'Convert PDF pages into JPG, PNG, WEBP and TIFF images online.','icon': 'fa-file-image'},
        {'id': 'image-resizer','name': 'Image Resizer','description': 'Resize JPG, PNG, and WEBP images online instantly.','icon': 'fa-expand'},
        {'id': 'image-compressor','name': 'Image Compressor','description': 'Compress JPG, PNG and WEBP images online without losing quality.','icon': 'fa-compress'},
        {'id': 'percentage-calculator', 'name': 'Percentage Calculator', 'description': 'Calculate percentages, increases, decreases and percentage differences instantly.', 'icon': 'fa-percent'},
        {'id': 'image-format-converter', 'name': 'Image Format Converter', 'description': 'Convert images between JPG, PNG, WEBP and other popular formats.', 'icon': 'fa-image'},
        {'id': 'meta-tag-generator', 'name': 'Meta Tag Generator', 'description': 'Generate SEO meta tags for your website instantly.', 'icon': 'fa-code'},
        {'id': 'qr-code-generator', 'name': 'QR Code Generator', 'description': 'Generate QR codes instantly for URLs and text.', 'icon': 'fa-qrcode'},
        {'id': 'bmi-calculator', 'name': 'BMI Calculator', 'description': 'Calculate your Body Mass Index instantly using height and weight.', 'icon': 'fa-heartbeat'},
        {'id': 'age-calculator', 'name': 'Age Calculator', 'description': 'Calculate your exact age in years, months, and days.', 'icon': 'fa-calendar-alt'},
        {'id': 'word-counter', 'name': 'Word Counter', 'description': 'Analyze text for word count, character count, and more.', 'icon': 'fa-text-height'},
        {'id': 'password-generator', 'name': 'Password Generator', 'description': 'Generate secure, random passwords with custom options.', 'icon': 'fa-lock'},
        {'id': 'case-converter', 'name': 'Case Converter', 'description': 'Convert text between different letter cases easily.', 'icon': 'fa-font'},
        {'id': 'unit-converter', 'name': 'Unit Converter', 'description': 'Quickly convert between different units of measurement.', 'icon': 'fa-exchange-alt'},
        {'id': 'image-converter', 'name': 'Image to PDF', 'description': 'Convert your images to high-quality PDF files instantly.', 'icon': 'fa-file-pdf'},
    ]
    return render_template('index.html', tools=tools)

@app.route('/tool/<tool_id>')
def tool_page(tool_id):
    return render_template(f'tools/{tool_id}.html')

@app.route('/convert-image', methods=['POST'])
def convert_image():
    if 'image' not in request.files:
        return "No image uploaded", 400
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    
    try:
        img = Image.open(file.stream)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        pdf_io = io.BytesIO()
        img.save(pdf_io, 'PDF', resolution=100.0)
        pdf_io.seek(0)
        
        return send_file(pdf_io, mimetype='application/pdf', as_attachment=True, download_name='converted.pdf')
    except Exception as e:
        return str(e), 500

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Future: Save to DB
        return "Message sent successfully!"
    return render_template('contact.html')
from flask import send_from_directory

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/tool/qr-code-generator')
def qr_code_generator():
    return render_template('tools/qr-code-generator.html')

@app.route('/convert-pdf-to-image', methods=['POST'])
def convert_pdf_to_image():

    pdf_file = request.files['pdf']
    output_format = request.form['format']

    temp_dir = tempfile.mkdtemp()

    pdf_path = os.path.join(temp_dir, pdf_file.filename)
    pdf_file.save(pdf_path)

    pages = convert_from_path(pdf_path)

    zip_path = os.path.join(temp_dir, "converted_images.zip")

    format_map = {
        'jpg': 'JPEG',
        'png': 'PNG',
        'webp': 'WEBP',
        'tiff': 'TIFF'
    }

    with ZipFile(zip_path, 'w') as zipf:

        for i, page in enumerate(pages):

            image_name = f"page_{i+1}.{output_format}"

            image_path = os.path.join(
                temp_dir,
                image_name
            )

            # JPEG does not support RGBA
            if output_format.lower() == 'jpg':
                page = page.convert("RGB")

            page.save(
                image_path,
                format_map[output_format.lower()]
            )

            zipf.write(
                image_path,
                image_name
            )

    return send_file(
        zip_path,
        as_attachment=True,
        download_name="pdf-images.zip"
    )

from flask import jsonify
import base64

@app.route('/remove-background', methods=['POST'])
def remove_background():


    if 'image' not in request.files:
        return jsonify({"success":False})

    file=request.files['image']

    try:

        input_bytes=file.read()

        output_bytes=remove(input_bytes)

        image_base64=base64.b64encode(output_bytes).decode("utf-8")

        return jsonify({
            "success":True,
            "image":"data:image/png;base64,"+image_base64
        })

    except Exception as e:

        return jsonify({
            "success":False,
            "error":str(e)
        })






if __name__ == '__main__':
    app.run(debug=True)
