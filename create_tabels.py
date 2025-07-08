# create_tables.py

from app.db.models import SQLModel
from app.db.session import engine

print("Connecting to DB...")

SQLModel.metadata.create_all(bind=engine)

print("DB connection successful!")
