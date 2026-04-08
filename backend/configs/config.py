# backend/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    VLR_API_BASE_URL = os.getenv("VLR_API_BASE_URL", "http://localhost:3001")
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"