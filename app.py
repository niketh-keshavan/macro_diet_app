import itertools
from flask import Flask, request, jsonify, send_from_directory, render_template
from models import Recipe, session
from recipes_data import populate_recipes

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_recipes", methods=["POST"])
def get_recipes():
    data = request.json
    target_macros = data.get("macros")
    diet_type = data.get("diet_type")
    
    # Fetch all recipes or filter by diet type
    if diet_type is None or diet_type == "":  # Handle "Any" diet type
        all_recipes = session.query(Recipe).all()
    else:
        all_recipes = session.query(Recipe).filter(Recipe.diet_type.contains(diet_type)).all()
    
    # Generate all combinations of 3 meals
    meal_combinations = itertools.combinations(all_recipes, 3)
    best_combination = None
    closest_combination = None
    best_score = float("inf")  # Lower score is better for closest match
    closest_score = float("inf")  # Tracks the closest match
    total_macros = {"carbs": 0, "protein": 0, "fat": 0}

    for combination in meal_combinations:
        total_carbs = sum(meal.carbs for meal in combination)
        total_protein = sum(meal.protein for meal in combination)
        total_fat = sum(meal.fat for meal in combination)
        
        # Check constraints
        carb_ok = total_carbs <= target_macros["carbs"]
        protein_ok = total_protein >= target_macros["protein"]
        fat_ok = total_fat <= target_macros["fat"]

        # Calculate the score for fallback (closest match)
        carb_diff = abs(total_carbs - target_macros["carbs"])
        protein_diff = abs(total_protein - target_macros["protein"])
        fat_diff = abs(total_fat - target_macros["fat"])
        score = carb_diff + protein_diff + fat_diff

        # Track the closest match
        if score < closest_score:
            closest_score = score
            closest_combination = combination

        # If all constraints are satisfied, check if this is the best match
        if carb_ok and protein_ok and fat_ok and score < best_score:
            best_score = score
            best_combination = combination
            total_macros = {  # Ensure this dictionary is properly defined
                "carbs": total_carbs,
                "protein": total_protein,
                "fat": total_fat,
            }

    # Use the closest combination if no valid combination is found
    if not best_combination:
        best_combination = closest_combination
        total_macros = {
            "carbs": sum(meal.carbs for meal in best_combination),
            "protein": sum(meal.protein for meal in best_combination),
            "fat": sum(meal.fat for meal in best_combination),
        }

    # Format the result
    result = [
        {
            "name": meal.name,
            "macros": {
                "carbs": meal.carbs,
                "protein": meal.protein,
                "fat": meal.fat,
            },
        }
        for meal in best_combination
    ]

    return jsonify({"meals": result, "total_macros": total_macros, "score": best_score})


if __name__ == "__main__":
    app.run(debug=True)
