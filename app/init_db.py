from app.database import Base, engine, SessionLocal
from app.models.category import Category

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    default_parents = ["Income", "Expense", "Saving"]
    for name in default_parents:
        exists = db.query(Category).filter(Category.name == name).first()
        if not exists:
            db.add(Category(name=name, is_parent=True))
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")