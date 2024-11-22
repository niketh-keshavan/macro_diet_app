from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///recipes.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Recipe Model
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    carbs = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    diet_type = Column(JSON, nullable=False)  # Stores diet types as a JSON array

# Create the database schema
Base.metadata.create_all(engine)

# Function to populate the database with sample recipes
def populate_recipes():
    sample_recipes = [
        {"name": "Avocado Salad", "carbs": 10, "protein": 2, "fat": 15, "diet_type": ["vegan", "veggie"]},
        {"name": "Grilled Chicken", "carbs": 0, "protein": 25, "fat": 5, "diet_type": ["keto"]},
        {"name": "Quinoa Bowl", "carbs": 20, "protein": 10, "fat": 8, "diet_type": ["vegan", "veggie"]},
        {"name": "Tofu Stir Fry", "carbs": 15, "protein": 10, "fat": 5, "diet_type": ["vegan", "veggie"]},
        {"name": "Cauliflower Rice", "carbs": 5, "protein": 2, "fat": 2, "diet_type": ["keto", "veggie"]},
        {"name": "Egg Salad", "carbs": 2, "protein": 15, "fat": 10, "diet_type": ["keto"]},
        {"name": "Chickpea Curry", "carbs": 30, "protein": 10, "fat": 12, "diet_type": ["vegan", "veggie"]},
        {"name": "Beef Stir Fry", "carbs": 5, "protein": 20, "fat": 15, "diet_type": ["keto"]},
        {"name": "Lentil Soup", "carbs": 25, "protein": 15, "fat": 5, "diet_type": ["vegan", "veggie"]},
        {"name": "Zucchini Noodles", "carbs": 5, "protein": 3, "fat": 2, "diet_type": ["keto", "veggie"]},
        {"name": "Greek Salad", "carbs": 8, "protein": 5, "fat": 7, "diet_type": ["veggie"]},
        {"name": "Spinach Smoothie", "carbs": 15, "protein": 5, "fat": 2, "diet_type": ["vegan", "veggie"]},
        {"name": "Baked Salmon", "carbs": 0, "protein": 25, "fat": 12, "diet_type": ["keto"]},
        {"name": "Veggie Wrap", "carbs": 30, "protein": 8, "fat": 10, "diet_type": ["vegan", "veggie"]},
        {"name": "Chicken Caesar Salad", "carbs": 5, "protein": 20, "fat": 15, "diet_type": ["keto"]},
        {"name": "Tomato Soup", "carbs": 18, "protein": 4, "fat": 5, "diet_type": ["veggie"]},
        {"name": "Black Bean Burger", "carbs": 20, "protein": 10, "fat": 8, "diet_type": ["vegan"]},
        {"name": "Shrimp Skewers", "carbs": 0, "protein": 22, "fat": 8, "diet_type": ["keto"]},
        {"name": "Stuffed Bell Peppers", "carbs": 25, "protein": 8, "fat": 7, "diet_type": ["vegan", "veggie"]},
        {"name": "Mushroom Risotto", "carbs": 30, "protein": 6, "fat": 10, "diet_type": ["veggie"]}
    ]
    # Add recipes to the database
    for recipe in sample_recipes:
        new_recipe = Recipe(
            name=recipe["name"],
            carbs=recipe["carbs"],
            protein=recipe["protein"],
            fat=recipe["fat"],
            diet_type=recipe["diet_type"]
        )
        session.add(new_recipe)
    session.commit()

# Populate the database if running this file directly
if __name__ == "__main__":
    populate_recipes()
    print("Database populated with sample recipes.")
