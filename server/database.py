from config import MONGO_URI
import motor.motor_asyncio
from pymongo import MongoClient
import os

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.python
