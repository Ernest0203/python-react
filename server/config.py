import os
from dotenv import load_dotenv

env = os.getenv("ENV", "development")

if env == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.development")

MONGO_URI = os.getenv("MONGO_URI")
