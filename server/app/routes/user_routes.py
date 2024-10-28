import pymongo
from app.db import transaction_collection, wallet_collection
from app.dependencies import get_current_user
from app.models import Transaction, User, Wallet
from fastapi import APIRouter, Body, Depends, HTTPException, status

user_router = APIRouter()

# Create a new wallet
@user_router.post("/", response_model=Wallet)
async def create_wallet(wallet: Wallet):
    """
    Creates a new wallet for a user.

    Args:
        wallet (Wallet): The wallet data, including user_id and initial balance.

    Raises:
        HTTPException: If a wallet with the same user_id already exists.

    Returns:
        Dict: The created wallet data including its new ObjectId.
    """
    try:
        print(wallet)
        wallet_data = wallet.dict()
        result = await wallet_collection.insert_one(wallet_data)
        wallet_data["_id"] = str(result.inserted_id)
        return wallet_data
    except pymongo.errors.DuplicateKeyError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wallet with user_id already exists"
        ) from ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating wallet: {e}")

# Deposit funds
@user_router.post("/{wallet_id}/deposit")
async def deposit(wallet_id: str, amount: float = Body(...), description: str = Body("")):
    """
    Deposits funds into a wallet.

    Args:
        wallet_id (str): The unique identifier of the wallet.
        amount (float): The amount to deposit.
        description (str): An optional description of the transaction.

    Raises:
        HTTPException: If the wallet is not found or if the deposit amount is invalid.

    Returns:
        Dict: A success message and the wallet's new balance.
    """
    try:
        wallet = await wallet_collection.find_one({"wallet_id": wallet_id})
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Invalid deposit amount")
        
        wallet['balance'] += amount
        await wallet_collection.update_one({"wallet_id": wallet_id}, {"$set": {"balance": wallet['balance']}})
        
        transaction = Transaction(wallet_id=wallet_id, type="deposit", amount=amount, description=description)
        await transaction_collection.insert_one(transaction.dict())
        
        return {"status": "success", "new_balance": wallet['balance']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error depositing funds: {e}")

# Withdraw funds
@user_router.post("/{wallet_id}/withdraw")
async def withdraw(wallet_id: str, amount: float = Body(...), description: str = Body("")):
    """
    Withdraws funds from a wallet.

    Args:
        wallet_id (str): The unique identifier of the wallet.
        amount (float): The amount to withdraw.
        description (str): An optional description of the transaction.

    Raises:
        HTTPException: If the wallet is not found, or if the withdrawal amount is invalid or exceeds the balance.

    Returns:
        Dict: A success message and the wallet's new balance.
    """
    try:
        wallet = await wallet_collection.find_one({"wallet_id": wallet_id})
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        if amount <= 0 or amount > wallet['balance']:
            raise HTTPException(status_code=400, detail="Invalid withdrawal amount or insufficient balance")

        wallet['balance'] -= amount
        await wallet_collection.update_one({"wallet_id": wallet_id}, {"$set": {"balance": wallet['balance']}})
        
        transaction = Transaction(wallet_id=wallet_id, type="withdrawal", amount=amount, description=description)
        await transaction_collection.insert_one(transaction.dict())
        
        return {"status": "success", "new_balance": wallet['balance']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error withdrawing funds: {e}")

# Transfer funds
@user_router.post("/{wallet_id}/transfer")
async def transfer(wallet_id: str, target_wallet_id: str = Body(...), amount: float = Body(...), description: str = Body(""), current_user:User= Depends(get_current_user)):
    """
    Transfers funds from one wallet to another.

    Args:
        wallet_id (str): The unique identifier of the source wallet.
        target_wallet_id (str): The unique identifier of the target wallet.
        amount (float): The amount to transfer.
        description (str): An optional description of the transaction.

    Raises:
        HTTPException: If either wallet is not found, or if the transfer amount is invalid or exceeds the balance.

    Returns:
        Dict: A success message and the source wallet's new balance.
    """
    try:
        source_wallet = await wallet_collection.find_one({"wallet_id": wallet_id})
        target_wallet = await wallet_collection.find_one({"wallet_id": target_wallet_id})
        
        if not source_wallet or not target_wallet:
            raise HTTPException(status_code=404, detail="One or both wallets not found")
        if amount <= 0 or amount > source_wallet['balance']:
            raise HTTPException(status_code=400, detail="Invalid transfer amount or insufficient balance")

        # Update balances
        source_wallet['balance'] -= amount
        target_wallet['balance'] += amount
        await wallet_collection.update_one({"wallet_id": wallet_id}, {"$set": {"balance": source_wallet['balance']}})
        await wallet_collection.update_one({"wallet_id": target_wallet_id}, {"$set": {"balance": target_wallet['balance']}})
        
        transaction = Transaction(wallet_id=wallet_id, type="transfer", amount=amount, description=description, source_wallet=wallet_id, destination_wallet=target_wallet_id)
        await transaction_collection.insert_one(transaction.dict())
        
        return {"status": "success", "new_balance": source_wallet['balance']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transferring funds: {e}")

# Get transaction history
@user_router.get("/{wallet_id}/transactions")
async def get_transactions(wallet_id: str):
    """
    Retrieves the transaction history for a specific wallet.

    Args:
        wallet_id (str): The unique identifier of the wallet.

    Returns:
        List[Dict]: A list of transactions associated with the specified wallet.
    """
    try:
        transactions = await transaction_collection.find({"wallet_id": wallet_id}, {'_id': 0}).to_list(length=100)
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving transactions: {e}")
