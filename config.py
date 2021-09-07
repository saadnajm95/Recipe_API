
import os
from dotenv import load_dotenv


API_KEY= 'YVTbqzJ6vA4YmkcJ9WNP8P5LQRmfS3Wj'

# ENVIRONNEMENT CONFIGURATION

## Load .env file
load_dotenv(verbose=True)

## Get these value from .env or from environnement
STRAPI_HOST = os.getenv("STRAPI_HOST", default="http://146.59.225.32")
MONGO_URI = os.getenv("MONGO_URI", default="mongodb://localhost:27017/app")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", default="token")