from models import Recipe, session

expanded_recipes = [
    {"name": "Avocado Salad", "macros": {"carbs": 10, "protein": 2, "fat": 15}, "diet_type": ["vegan", "veggie"]},
    {"name": "Grilled Chicken", "macros": {"carbs": 0, "protein": 25, "fat": 5}, "diet_type": ["keto"]},
    # Add the remaining 18 recipes here (use the list from the earlier example)...
]

def populate_recipes():
    for r in expanded_recipes:
        recipe = Recipe(
            name=r["name"],
            carbs=r["macros"]["carbs"],
            protein=r["macros"]["protein"],
            fat=r["macros"]["fat"],
            diet_type=r["diet_type"],
        )
        session.add(recipe)
    session.commit()

def find_matching_recipes_from_db(target_macros, diet_type):
    all_recipes = session.query(Recipe).all()
    matching_recipes = []
    for recipe in all_recipes:
        if diet_type in recipe.diet_type:
            carb_diff = abs(recipe.carbs - target_macros["carbs"])
            protein_diff = abs(recipe.protein - target_macros["protein"])
            fat_diff = abs(recipe.fat - target_macros["fat"])
            score = carb_diff + protein_diff + fat_diff
            matching_recipes.append({"recipe": recipe.name, "score": score})
    return sorted(matching_recipes, key=lambda x: x["score"])

# Uncomment to populate the database (only run once)
populate_recipes()
