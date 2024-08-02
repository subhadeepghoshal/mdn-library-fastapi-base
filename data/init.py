"""Initialize SQLite database"""
import os
from dotenv import load_dotenv
load_dotenv()

import motor.motor_asyncio

db: any

def get_db():
    global db
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db = client.library

get_db()
