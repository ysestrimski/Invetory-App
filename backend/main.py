import os, uuid
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional
from models import Base, Item

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://invuser:invpass@db:5432/inventory")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Refurbished Inventory API")

origins = [
    "http://192.168.88.31:3000",  # your frontend
    "http://localhost:3000",      # local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ItemIn(BaseModel):
    sku: str
    model: Optional[str]
    brand: Optional[str]
    condition: Optional[str] = "refurbished"
    price: Optional[float] = 0.0
    quantity: Optional[int] = 0
    notes: Optional[str] = None

class ItemOut(ItemIn):
    id: int
    image_path: Optional[str]
    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/items", response_model=List[ItemOut])
def list_items(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return db.query(Item).offset(skip).limit(limit).all()

@app.post("/items", response_model=ItemOut)
def create_item(item: ItemIn, db=Depends(get_db)):
    if db.query(Item).filter(Item.sku == item.sku).first():
        raise HTTPException(status_code=400, detail="SKU already exists")
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.post("/items/{item_id}/upload-image")
def upload_image(item_id: int, file: UploadFile = File(...), db=Depends(get_db)):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    os.makedirs("uploads", exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    fname = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join("uploads", fname)
    with open(path, "wb") as f:
        f.write(file.file.read())
    item.image_path = f"/uploads/{fname}"
    db.add(item)
    db.commit()
    return {"image_path": item.image_path}
