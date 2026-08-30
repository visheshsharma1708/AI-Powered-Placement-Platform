import app.models
from app.db.database import Base, engine


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)