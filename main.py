import requests
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# --- 1. CONFIGURATION ---
DATABASE_URL = "mysql+pymysql://root:root123@localhost/cake_shop_db"

# Aapka Naya Token aur Chat ID jo aapne abhi diya
TELEGRAM_TOKEN = "8582688729:AAHu02DbbjHLgHbK48TL-LQ16RGAXqNFIbU"
CHAT_ID = "5104607858" 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. DATABASE MODEL ---
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100))
    phone = Column(String(20))
    address = Column(Text)
    items = Column(Text)
    total_price = Column(Integer)
    message = Column(String(255))
    payment_type = Column(String(50))

Base.metadata.create_all(bind=engine)

# --- 3. PYDANTIC SCHEMA ---
class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    address: str
    items: str
    total_price: int
    message: str = ""
    payment_type: str

# --- 4. FASTAPI APP INIT ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 5. TELEGRAM FUNCTION ---
def send_telegram_msg(order_details):
    try:
        msg = (f"🎂 *NAYA ORDER AAYA HAI!* 🎂\n\n"
               f"👤 *Customer:* {order_details.customer_name}\n"
               f"📞 *Phone:* {order_details.phone}\n"
               f"🏠 *Address:* {order_details.address}\n"
               f"🍰 *Items:* {order_details.items}\n"
               f"💰 *Total:* ₹{order_details.total_price}\n"
               f"📝 *Note:* {order_details.message}\n"
               f"💳 *Payment:* {order_details.payment_type}")
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        response = requests.post(url, json=payload)
        
        # Ye line terminal mein status dikhayegi debugging ke liye
        print(f"Telegram Response: {response.json()}") 
    except Exception as e:
        print(f"Telegram Error: {e}")

# --- 6. ROUTES ---
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

@app.get("/")
def home():
    return {"message": "CakeHouse Backend is Live!"}

@app.post("/api/orders")
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    try:
        # 1. Database mein save karo
        new_order = Order(**order_data.dict())
        db.add(new_order)
        db.commit() 
        db.refresh(new_order)
        
        # 2. Telegram Notification bhejo
        send_telegram_msg(order_data)
        
        return {"status": "success", "order_id": new_order.id}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orders")
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()