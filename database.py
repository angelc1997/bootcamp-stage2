from dotenv import load_dotenv
from mysql.connector import pooling
import os




load_dotenv()

dbconfig = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "pool_name": os.getenv("DB_POOL_NAME"),
    "pool_size": 5,
}

