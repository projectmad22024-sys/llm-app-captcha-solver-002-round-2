# OCR CAPTCHA Solver Web Application

This project implements a Flask-based web application that generates simple CAPTCHA images and provides an endpoint to automatically recognize and solve the CAPTCHA using OCR technology.

## Features

- Serves dynamically generated CAPTCHA images with random alphanumeric text.
- Allows users to request the solution to the current CAPTCHA within 12 seconds.
- Utilizes Tesseract OCR engine for text recognition.
- Encapsulated within a Docker container for ease of deployment.

## How It Works

Upon startup, the server generates a random CAPTCHA text and creates an image displayed to the user. Users can request to solve the CAPTCHA by clicking the "Solve CAPTCHA" button, which fetches the current image and runs OCR to extract the text. The result is displayed on the page.

## Running Locally

1. Ensure Docker is installed.
2. Build the Docker image:

```bash
docker build -t ocr-captcha-solver .
```
3. Run the container:

```bash
docker run -p 5000:5000 ocr-captcha-solver
```
4. Open your browser and navigate to `http://localhost:5000`.

## Usage

- View the CAPTCHA image.
- Click "Reload CAPTCHA" to generate a new one.
- Click "Solve CAPTCHA" to attempt to recognize the text automatically.

## License

MIT License

---

**Note:** This implementation uses Tesseract OCR and Python's pillow for image generation. For production deployment, further enhancements such as CAPTCHA complexity, better OCR handling, and security are recommended.
