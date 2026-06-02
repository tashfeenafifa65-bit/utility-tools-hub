from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import io

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

    @app.route('/googled3f9ca86626307df.html')
def google_verification():
    return send_from_directory('.', 'googled3f9ca86626307df.html')

if __name__ == '__main__':
    app.run(debug=True)
