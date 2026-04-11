import requests
import json
import time

API_URL = "http://localhost:8000"
API_KEY = "sia_translation_key_2024"

def test_root():
    response = requests.get(API_URL)
    print(f"Root: {response.status_code} - {response.json()}")

def test_unauthorized():
    data = {
        "text": "Hello world",
        "src_lang": "en",
        "target_lang": "es"
    }
    response = requests.post(f"{API_URL}/translate", json=data)
    print(f"Unauthorized (should be 403): {response.status_code} - {response.json()}")

def test_translate(text="Hello, how are you?", src="en", target="es"):
    headers = {"X-API-Key": API_KEY}
    data = {
        "text": text,
        "src_lang": src,
        "target_lang": target
    }
    response = requests.post(f"{API_URL}/translate", json=data, headers=headers, timeout=60)
    print(f"Translate: {response.status_code} - {response.json()}")

def test_rate_limiting():
    headers = {"X-API-Key": API_KEY}
    data = {"text": "Test", "src_lang": "en", "target_lang": "fr"}
    print("Testing rate limiting (sending 5 requests)...")
    for i in range(5):
        response = requests.post(f"{API_URL}/translate", json=data, headers=headers, timeout=10)
        print(f"Request {i+1}: {response.status_code}")
        if response.status_code == 429:
            print("Rate limit hit!")
            break

if __name__ == "__main__":
    test_root()
    test_unauthorized()
    print("Waiting 10 seconds for model buffer...")
    time.sleep(10)
    test_translate()
    test_rate_limiting()
