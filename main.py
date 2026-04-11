import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import torch

from config import Config
from auth import get_api_key

# Request/Response Schemas
class TranslationRequest(BaseModel):
    text: str = Field(..., example="Hello, how are you?")
    src_lang: str = Field(..., example="en")
    target_lang: str = Field(..., example="es")

class TranslationResponse(BaseModel):
    translated_text: str
    src_lang: str
    target_lang: str

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)

# Global model and tokenizer
model = None
tokenizer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model and tokenizer on startup
    global model, tokenizer
    print(f"Loading model {Config.MODEL_NAME}...")
    tokenizer = M2M100Tokenizer.from_pretrained(Config.MODEL_NAME)
    model = M2M100ForConditionalGeneration.from_pretrained(Config.MODEL_NAME)
    # Move to GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    print(f"Model loaded on {device}.")
    yield
    # Clean up (if needed)
    del model
    del tokenizer

app = FastAPI(
    title="Sia Translation API",
    description="A high-performance translation API powered by Hugging Face M2M100 model.",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limit handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
async def root():
    return {"message": "Welcome to Sia Translation API. Access /docs for documentation."}

@app.post("/translate", response_model=TranslationResponse, dependencies=[Depends(get_api_key)])
@limiter.limit(f"{Config.RATE_LIMIT_PER_MINUTE}/minute")
async def translate(request: Request, translation_data: TranslationRequest):
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Set source language
        tokenizer.src_lang = translation_data.src_lang
        
        # Tokenize input
        encoded_input = tokenizer(translation_data.text, return_tensors="pt").to(model.device)
        
        # Generate translation
        generated_tokens = model.generate(
            **encoded_input, 
            forced_bos_token_id=tokenizer.get_lang_id(translation_data.target_lang)
        )
        
        # Decode translation
        translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        
        return TranslationResponse(
            translated_text=translated_text,
            src_lang=translation_data.src_lang,
            target_lang=translation_data.target_lang
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
