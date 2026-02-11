import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()
    return {
        "LLM_PROVIDER": os.getenv("LLM_PROVIDER", "NONE"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "MODEL_NAME": os.getenv("MODEL_NAME", "gpt-4.1-mini"),
    }

def normalize_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    return s.strip().lower()
