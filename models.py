from sqlalchemy import create_engine, Column, String, Integer, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    carbs = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    diet_type = Column(JSON, nullable=False)

# Database setup
DATABASE_URI = "sqlite:///recipes.db"
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

# Session creation
Session = sessionmaker(bind=engine)
session = Session()
