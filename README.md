# Sia Translation API

A robust, authenticated, and rate-limited Translation API built with FastAPI and Hugging Face's M2M100 model.

## Features
- **Multi-language Support**: Powered by `facebook/m2m100_418M`, supporting translation between 100 languages.
- **Authentication**: Secure access using X-API-Key header.
- **Rate Limiting**: Built-in protection against abuse using `slowapi`.
- **Automatic Documentation**: Interactive API docs provided by FastAPI (Swagger UI).
- **Asynchronous Execution**: High-performance handling of requests.

## Prerequisites
- **Python**: 3.8 or higher (Tested with Python 3.14.2)
- **RAM**: Minimum 4GB for model execution.

## Installation Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd SiaFinal
   ```

2. **Set up Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration Guide

1. **Environment Variables**
   Create a `.env` file in the root directory (copy from `.env.example`):
   ```env
   API_KEY=your_secret_api_key_here
   RATE_LIMIT_PER_MINUTE=60
   ```
   - `API_KEY`: The secret key required to access the `/translate` endpoint.
   - `RATE_LIMIT_PER_MINUTE`: Maximum requests allowed per minute per client.

## API Endpoints Documentation

### 1. Root Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Description**: Health check and welcome message.

### 2. Translation Endpoint
- **URL**: `/translate`
- **Method**: `POST`
- **Headers**:
  - `X-API-Key`: Your secret API key.
- **Payload Example**:
  ```json
  {
    "text": "Hello, how are you?",
    "src_lang": "en",
    "target_lang": "es"
  }
  ```
- **Response Example**:
  ```json
  {
    "translated_text": "Hola, ¿cómo estás?",
    "src_lang": "en",
    "target_lang": "es"
  }
  ```

## Authentication & Rate Limiting Details

- **Authentication**: Header-based authentication is used. All sensitive endpoints require the `X-API-Key` header.
- **Rate Limiting**: Clients are limited by their IP address. If the limit is exceeded, the API returns a `429 Too Many Requests` status code.



## Testing Instructions

1. **Start the Server**
   ```bash
   python main.py
   ```
   *(Wait for the model to download and load on first run)*

2. **Run the Test Script**
   ```bash
   python test_api.py
   ```

3. **Manual Testing via SwaggerUI**
   Access `http://localhost:8000/docs` in your browser.

## Troubleshooting Guide
- **Model Loading Slow**: The model `m2m100_418M` is about 1.8GB. First startup requires downloading this from Hugging Face.
- **CUDA Errors**: If you don't have a GPU, the API will automatically fall back to CPU. Ensure you have enough RAM.
- **Port Already in Use**: Change the port in `main.py` if 8000 is occupied.

## Team Members and Contributions
