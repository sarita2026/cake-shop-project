import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Database URL fetch karna
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Agar link "mysql://" hai toh replace karo
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("mysql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# AGAR URL NAHI MILA (Local testing ke liye fallback)
if not SQLALCHEMY_DATABASE_URL:
    # Yahan apna local database ka password dalo agar computer par chala rahe ho
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost/cake_shop"

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
