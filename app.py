from flask import Flask, send_file, jsonify, make_response
import io
import random
import string
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import threading
import time

app = Flask(__name__)

# Generate a simple captcha image with random text
def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

captcha_text = ''
captcha_lock = threading.Lock()

# Generate a new captcha text and update global variable
def refresh_captcha():
    global captcha_text
    with captcha_lock:
        captcha_text = generate_captcha_text()

# Create an image for the current captcha text
def create_captcha_image(text):
    width, height = 200, 70
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    # Use a basic font
    try:
        font = ImageFont.truetype('arial.ttf', 40)
    except:
        font = ImageFont.load_default()
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))
    # Add some noise or lines for complexity (optional)
    return image

# Route to serve captcha image
@app.route('/captcha-image')
def get_captcha_image():
    global captcha_text
    with captcha_lock:
        text = captcha_text
    image = create_captcha_image(text)
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

# Route to solve captcha
@app.route('/solve-captcha', methods=['POST'])
def solve_captcha():
    global captcha_text
    start_time = time.time()
    # Download the current captcha image
    import requests
    response = requests.get('http://localhost:5000/captcha-image')
    image_bytes = io.BytesIO(response.content)
    image = Image.open(image_bytes)
    # Use pytesseract to recognize text
    try:
        ocr_result = pytesseract.image_to_string(image, config='--psm 8').strip()
        # Sometimes OCR may produce extra whitespaces; clean up
        ocr_result = ''.join(filter(str.isalnum, ocr_result)).upper()
    except Exception as e:
        ocr_result = ''
    elapsed_time = time.time() - start_time
    # Check if OCR matches the captcha
    with captcha_lock:
        actual_text = captcha_text
    success = (ocr_result == actual_text)
    # Prepare response
    if elapsed_time > 12:
        return jsonify({'success': False, 'error': 'Timeout exceeded'}), 408
    return jsonify({'success': success, 'text': ocr_result})

# Initialize captcha
refresh_captcha()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
