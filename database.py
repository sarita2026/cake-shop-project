# import mysql.connector

# def get_db_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="root123", # Update this!
#         database="cake_db"
#     )

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Database URL fetch karna (Render/Railway se automatic uthayega)
# Agar local mein chala rahe ho toh ye default URL use karega
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Railway ki URL "mysql://" se shuru hoti hai, 
# lekin SQLAlchemy ko "mysql+pymysql://" chahiye hota hai
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("mysql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# 2. Engine Create karna
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Session aur Base setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 4. Database Session helper
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()