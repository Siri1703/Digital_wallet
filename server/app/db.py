# setup_db.py
import asyncio
import os

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from .models import User

# MongoDB connection URI
MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
db = client["digital_wallet_db"]

# Collections
wallet_collection: AsyncIOMotorCollection = db["wallets"]
transaction_collection: AsyncIOMotorCollection = db["transactions"]
audit_log_collection: AsyncIOMotorCollection = db["audit_logs"]
user_collection: AsyncIOMotorCollection = db['user_collection']


async def create_collections():
    try:
        # Check if collections already exist, if not, create them
        collection_names = await db.list_collection_names()

        # Create Wallet Collection with Indexes
        if "wallets" not in collection_names:
            await wallet_collection.create_index("user_id", unique=True)
            await wallet_collection.create_index("status")
            print("Created 'wallets' collection with indexes.")

        # Create Transaction Collection with Indexes
        if "transactions" not in collection_names:
            await transaction_collection.create_index("wallet_id")
            await transaction_collection.create_index("date")
            print("Created 'transactions' collection with indexes.")

        # Create Audit Log Collection with Indexes
        if "audit_logs" not in collection_names:
            await audit_log_collection.create_index("wallet_id")
            await audit_log_collection.create_index("timestamp")
            print("Created 'audit_logs' collection with indexes.")
    except Exception as e:
        print(f"Error creating collections: {e}")

async def get_user_by_email(email: str) -> User:
    try:
        user_data = await user_collection.find_one({"_id": ObjectId(email)})
        if user_data:
            return User(**user_data)  # Return a User instance if found
        return None  # Return None if no user found
    except Exception as e:
        print(f"Error retrieving user by email: {e}")
        return None

async def main():
    try:
        await create_collections()
        print("Database setup complete.")
    except Exception as e:
        print(f"Error during database setup: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
