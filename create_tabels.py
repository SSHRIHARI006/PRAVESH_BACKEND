from app.db.session import engine
from app.db.base import Base

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")
