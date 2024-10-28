from datetime import datetime
from typing import Optional

from app.db import (audit_log_collection, transaction_collection,
                    wallet_collection)
from app.dependencies import role_required
from fastapi import APIRouter, Depends, HTTPException

admin_router = APIRouter()

# List all wallets
@admin_router.get("/wallets")
async def list_wallets():
    """
    Retrieves a list of all wallets in the system.
    
    Converts MongoDB ObjectId fields to strings to ensure compatibility with JSON serialization.
    
    Returns:
        List[Dict]: A list of dictionaries, each representing a wallet.
    """
    try:
        wallets = await wallet_collection.find().to_list(length=100)
        for wallet in wallets:
            wallet["_id"] = str(wallet["_id"])
        return wallets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving wallets: {e}")

# Suspend a wallet
@admin_router.put("/wallets/{wallet_id}/suspend")
async def suspend_wallet(wallet_id: str):
    """
    Suspends a wallet by updating its status to 'suspended'.
    
    Args:
        wallet_id (str): The unique identifier of the wallet to suspend.
    
    Raises:
        HTTPException: If the wallet with the specified ID is not found.
    
    Returns:
        Dict: A success message indicating the wallet has been suspended.
    """
    try:
        wallet = await wallet_collection.find_one({"wallet_id": wallet_id})
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        
        await wallet_collection.update_one({"wallet_id": wallet_id}, {"$set": {"status": "suspended"}})
        audit_log = {"action": "suspend_wallet", "performed_by": "admin", "wallet_id": wallet_id, "timestamp": datetime.utcnow()}
        await audit_log_collection.insert_one(audit_log)
        return {"status": "wallet suspended"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error suspending wallet: {e}")

@admin_router.get("/transactions", summary="Retrieve transactions with filters")
async def get_transactions(
    transaction_type: Optional[str],
    start_date: Optional[datetime],
    end_date: Optional[datetime],
):
    """
    Retrieves transactions based on optional filters for transaction type, start date, and end date.
    
    Args:
        transaction_type (Optional[str]): The type of transactions to filter by (e.g., "deposit", "withdrawal").
        start_date (Optional[datetime]): The earliest transaction date to include.
        end_date (Optional[datetime]): The latest transaction date to include.
    
    Returns:
        Dict: A dictionary containing a list of filtered transactions.
    """
    try:
        filters = {}
        if transaction_type:
            filters["type"] = transaction_type
        if start_date and end_date:
            filters["date"] = {"$gte": start_date, "$lte": end_date}
        elif start_date:
            filters["date"] = {"$gte": start_date}
        elif end_date:
            filters["date"] = {"$lte": end_date}

        transactions = await transaction_collection.find(filters, {'_id': 0}).to_list(100)
        return {"transactions": transactions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving transactions: {e}")

@admin_router.get("/reports", summary="Generate transaction reports")
async def get_reports(
    start_date: Optional[datetime],
    end_date: Optional[datetime],
    dependencies=[Depends(role_required("admin"))]
):
    """
    Generates a summary report of transactions, grouping by type and calculating total amount and count for each type.
    
    Args:
        start_date (Optional[datetime]): The earliest transaction date to include in the report.
        end_date (Optional[datetime]): The latest transaction date to include in the report.
    
    Returns:
        Dict: A dictionary containing the aggregated report data for each transaction type.
    """
    try:
        match_stage = {}
        if start_date and end_date:
            match_stage = {"$match": {"date": {"$gte": start_date, "$lte": end_date}}}
        elif start_date:
            match_stage = {"$match": {"date": {"$gte": start_date}}}
        elif end_date:
            match_stage = {"$match": {"date": {"$lte": end_date}}}

        aggregation_pipeline = [
            match_stage,
            {
                "$group": {
                    "_id": "$type",
                    "total_amount": {"$sum": "$amount"},
                    "count": {"$sum": 1}
                }
            }
        ]
        report = await transaction_collection.aggregate(aggregation_pipeline).to_list(None)
        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {e}")
