import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))

# Use Chroma’s default embedding function for simplicity
embedding_func = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(name="transactions", embedding_function=embedding_func)

def add_transaction_to_vector_store(transaction_id: str, note: str):
    collection.add(
        documents=[note],
        ids=[transaction_id]
    )

def query_transactions_by_note(query: str):
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
    return results
