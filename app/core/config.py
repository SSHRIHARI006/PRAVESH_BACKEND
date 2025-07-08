from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
   # FERNET_SECRET_KEY: str = os.getenv("FERNET_SECRET_KEY")

settings = Settings()
