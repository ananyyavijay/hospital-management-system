import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\KIIT0001\Desktop\python lab\hospital_management_system\.env")  # load .env file

# ✏️ Write get_connection()
def get_connection():
    """Returns a psycopg2 connection using environment variables."""
    # Your code starts here
    try:
        connection = psycopg2.connect(
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT"),
            database  = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
        )
        print("DB is successfully connected")
        return connection
        
    except OperationalError as err:
        print("DB connection failed")
        print(err)
        return None

  