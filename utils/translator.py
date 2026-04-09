# utils/translator.py
from googletrans import Translator
import time

translator = Translator()

LANGUAGE_CODES = {
    "english": "en",
    "hindi": "hi",
    "tamil": "ta",
    "telugu": "te",
    "kannada": "kn",
    "bengali": "bn",
    "marathi": "mr",
    "gujarati": "gu",
    "punjabi": "pa",
    "malayalam": "ml",
    "odia": "or",
    "assamese": "as",
    # Add more if needed
}

def detect_language(text: str) -> str:
    """Returns language code (e.g., 'hi', 'ta', 'en')"""
    try:
        return translator.detect(text).lang
    except:
        return "en"

def translate_text(text: str, target_lang: str = "en") -> str:
    """
    Translate text to target language.
    target_lang can be full name or code (hindi / hi)
    """
    if not text or len(text.strip()) < 2:
        return text

    # Convert full name to code
    if target_lang.lower() in LANGUAGE_CODES:
        target_lang = LANGUAGE_CODES[target_lang.lower()]

    try:
        result = translator.translate(text, dest=target_lang)
        time.sleep(0.2)          # Small delay to avoid rate limit
        return result.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # fallback to original text
