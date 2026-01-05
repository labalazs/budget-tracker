from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    is_parent = Column(Boolean, default=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    parent = relationship("Category", remote_side=[id], back_populates="children", uselist=False)
    children = relationship("Category", back_populates="parent", cascade="all, delete-orphan")

    keywords = relationship("CategoryKeyword", back_populates="category", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="category")

    def __repr__(self):
        return f'Catogery {self.name} (id={self.id})'