import os
from psycopg import connect
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """
    Get a connection to the PostgreSQL database.
    """
    return connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
