from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime
import os

app = FastAPI(title="Ledger Service")

class Transaction(BaseModel):
    account_id: str
    amount: float
    transaction_type: str  # "debit" or "credit"

@app.get("/healthz")
def health_check():
    return {
        "status": "HEALTHY",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "service": "ledger-service"
    }

@app.get("/readyz")
def readiness_check():
    return {"status": "READY"}

@app.post("/api/v1/ledger/transaction")
def process_transaction(txn: Transaction):
    if txn.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    
    return {
        "transaction_id": "txn_89432712983",
        "status": "PROCESSED",
        "account_id": txn.account_id,
        "amount": txn.amount,
        "type": txn.transaction_type,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8081))
    uvicorn.run(app, host="0.0.0.0", port=port)
