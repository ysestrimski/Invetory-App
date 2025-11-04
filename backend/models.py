from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    model = Column(String, index=True)
    brand = Column(String, index=True)
    condition = Column(String, default="refurbished")
    price = Column(Float, default=0.0)
    quantity = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    image_path = Column(String, nullable=True)
