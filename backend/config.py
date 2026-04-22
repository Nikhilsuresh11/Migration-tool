import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = True

    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"pdf", "docx"}

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL")
    GROQ_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS") or 4096)
    GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE") or 0.1)

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemma-4-26b-a4b-it:free")

    @staticmethod
    def init_upload_folder():
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
