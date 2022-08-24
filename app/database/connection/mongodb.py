import os
import motor.motor_asyncio

def mongodb():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db = client.z1data
    return db

