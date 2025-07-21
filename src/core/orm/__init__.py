from .db import sync_engine
from .base import Base


def create_tables():
    Base.metadata.create_all(sync_engine)
