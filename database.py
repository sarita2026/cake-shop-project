# import os
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # 1. Database URL fetch karna (Render/Railway se automatic uthayega)
# # Agar local mein chala rahe ho toh ye default URL use karega
# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# # Railway ki URL "mysql://" se shuru hoti hai, 
# # lekin SQLAlchemy ko "mysql+pymysql://" chahiye hota hai
# if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("mysql://"):
#     SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# # 2. Engine Create karna
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# # 3. Session aur Base setup
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # 4. Database Session helper
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Environment Variable se link uthana
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Railway URL fix (mysql:// ko mysql+pymysql:// banana)
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("mysql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# Fallback agar link na mile
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root123@localhost/cake_shop_db"

# 2. Engine aur Session setup
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()