from functools import lru_cache
from ..config import get_settings
@lru_cache
def get_client():
    from google import genai
    key=get_settings().gemini_api_key
    if not key: raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=key)
def generate_text(model,prompt):
    from google.genai import types
    r=get_client().models.generate_content(model=model,contents=prompt,config=types.GenerateContentConfig(temperature=.4,max_output_tokens=5000))
    text=getattr(r,"text",None)
    if not text: raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
