from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class CategoryKeyword(Base):
    __tablename__ = "category_keywords"
    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="keywords")

    def __repr__(self):
        return f'Keyword {self.keyword} (id={self.id})'