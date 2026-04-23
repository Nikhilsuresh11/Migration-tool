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
    def get_cors_origins() -> list:
        """
        Build list of allowed CORS origins.
        Allows:
        - Local development (localhost, 127.0.0.1)
        - All Vercel deployments (*.vercel.app)
        - Custom domain from FRONTEND_URL env variable (if set)
        """
        origins = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "https://migration-tool-mu.vercel.app",  # Explicitly add your Vercel app
            "https://*.vercel.app",  # Flask-CORS will match this pattern
        ]
        
        custom_domain = os.getenv("FRONTEND_URL", "")
        if custom_domain:
            origins.append(custom_domain)
        
        return origins

    @staticmethod
    def init_upload_folder():
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
