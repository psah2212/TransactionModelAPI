from fastapi import FastAPI, HTTPException
from models.schemas import Account, AccountCreate, Transaction, TransactionCreate
from uuid import UUID
from typing import List
from db.chroma import add_transaction_to_vector_store, query_transactions_by_note

app = FastAPI()

# In-memory "DB"
accounts_db = {}
transactions_db = {}

@app.post("/accounts", response_model=Account)
def create_account(account_data: AccountCreate):
    account = Account(name=account_data.name)
    accounts_db[account.id] = account
    return account

@app.get("/accounts", response_model=List[Account])
def get_accounts():
    return list(accounts_db.values())

@app.post("/transactions", response_model=Transaction)
def create_transaction(txn_data: TransactionCreate):
    if txn_data.from_account not in accounts_db or txn_data.to_account not in accounts_db:
        raise HTTPException(status_code=404, detail="One or both accounts not found.")

    from_acc = accounts_db[txn_data.from_account]
    to_acc = accounts_db[txn_data.to_account]

    if from_acc.balance < txn_data.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds.")

    # Perform transfer
    from_acc.balance -= txn_data.amount
    to_acc.balance += txn_data.amount

    txn = Transaction(**txn_data.dict())
    transactions_db[txn.id] = txn

    # Store in ChromaDB if there's a note
    if txn.note:
        add_transaction_to_vector_store(str(txn.id), txn.note)

    return txn

@app.get("/transactions", response_model=List[Transaction])
def list_transactions():
    return list(transactions_db.values())

@app.get("/transactions/search/")
def search_transactions(query: str):
    results = query_transactions_by_note(query)
    ids = results.get("ids", [[]])[0]
    matches = [transactions_db[UUID(tid)] for tid in ids if UUID(tid) in transactions_db]
    return matches
