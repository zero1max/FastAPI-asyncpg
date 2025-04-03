from dotenv import load_dotenv
import os
load_dotenv(".env")


DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

# SQLITE_DB = os.getenv("SQLITE_DB", "database.db")

DATABASE_URL = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# DATABASE_URL = f"sqlite:///{SQLITE_DB}"