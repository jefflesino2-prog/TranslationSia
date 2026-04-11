import requests
import json
import time

API_URL = "http://localhost:8000"
API_KEY = "sia_translation_key_2024"
INVALID_KEY = "wrong_key"

def test_root():
    print("\n--- Testing Root ---")
    try:
        response = requests.get(API_URL)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_no_api_key():
    print("\n--- Testing Missing API Key ---")
    data = {"text": "Hello", "src_lang": "en", "target_lang": "es"}
    try:
        response = requests.post(f"{API_URL}/translate", json=data)
        print(f"Status (Expected 403): {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_invalid_api_key():
    print("\n--- Testing Invalid API Key ---")
    headers = {"X-API-Key": INVALID_KEY}
    data = {"text": "Hello", "src_lang": "en", "target_lang": "es"}
    try:
        response = requests.post(f"{API_URL}/translate", json=data, headers=headers)
        print(f"Status (Expected 403): {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_missing_fields():
    print("\n--- Testing Missing Fields ---")
    headers = {"X-API-Key": API_KEY}
    data = {"text": "Hello"} # Missing src_lang and target_lang
    try:
        response = requests.post(f"{API_URL}/translate", json=data, headers=headers)
        print(f"Status (Expected 422): {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_invalid_language_code():
    print("\n--- Testing Invalid Language Code ---")
    headers = {"X-API-Key": API_KEY}
    data = {"text": "Hello", "src_lang": "invalid_lang", "target_lang": "es"}
    try:
        response = requests.post(f"{API_URL}/translate", json=data, headers=headers)
        print(f"Status (Expected 500 or 400): {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_rate_limiting():
    print("\n--- Testing Rate Limiting (Limit=2/min) ---")
    headers = {"X-API-Key": API_KEY}
    data = {"text": "Test", "src_lang": "en", "target_lang": "fr"}
    for i in range(4):
        try:
            response = requests.post(f"{API_URL}/translate", json=data, headers=headers)
            print(f"Request {i+1} Status: {response.status_code}")
            if response.status_code == 429:
                print(f"Rate Limited: {response.json()}")
        except Exception as e:
            print(f"Error on request {i+1}: {e}")

if __name__ == "__main__":
    # Give the model some time to initialize if it's still loading
    print("Starting error handling tests...")
    test_root()
    test_no_api_key()
    test_invalid_api_key()
    test_missing_fields()
    
    # These might take longer as they involve the model
    test_invalid_language_code()
    test_rate_limiting()
