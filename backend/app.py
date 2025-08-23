from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from services.spoonacular import SpoonacularClient, to_macro
from services.nutrition import sum_macros, aggregate_ingredients
from services.planner import daily_targets, build_week_plan
from models.db import db
from models.grocery_list import GroceryList
import json

# Mock data for testing
INDIAN_RECIPES = [
    {
        "id": 1,
        "title": "Aloo Gobi",
        "image": "aloo_gobi.jpg",
        "usedIngredientCount": 3,
        "missedIngredientCount": 2,
        "likes": 150
    },
    {
        "id": 2,
        "title": "Chole (Chickpea Curry)",
        "image": "chole.jpg",
        "usedIngredientCount": 4,
        "missedIngredientCount": 1,
        "likes": 200
    },
    {
        "id": 3,
        "title": "Paneer Butter Masala",
        "image": "paneer_butter_masala.jpg",
        "usedIngredientCount": 5,
        "missedIngredientCount": 0,
        "likes": 250
    },
    {
        "id": 4,
        "title": "Dal Tadka",
        "image": "dal_tadka.jpg",
        "usedIngredientCount": 2,
        "missedIngredientCount": 3,
        "likes": 180
    },
    {
        "id": 5,
        "title": "Chicken Biryani",
        "image": "chicken_biryani.jpg",
        "usedIngredientCount": 4,
        "missedIngredientCount": 2,
        "likes": 300
    },
     
    # American
    {"id": 6, "title": "American Cheeseburger", "image": "cheeseburger.jpg", "usedIngredientCount": 3, "missedIngredientCount": 3, "likes": 400},
    {"id": 7, "title": "BBQ Ribs", "image": "bbq_ribs.jpg", "usedIngredientCount": 2, "missedIngredientCount": 4, "likes": 350},
    {"id": 8, "title": "Caesar Salad", "image": "caesar_salad.jpg", "usedIngredientCount": 3, "missedIngredientCount": 2, "likes": 220},
    {"id": 9, "title": "Mac and Cheese", "image": "mac_and_cheese.jpg", "usedIngredientCount": 5, "missedIngredientCount": 1, "likes": 370},
    {"id": 10, "title": "Pulled Pork Sandwich", "image": "pulled_pork.jpg", "usedIngredientCount": 4, "missedIngredientCount": 3, "likes": 280},
    
    # Chinese
    {"id": 11, "title": "Kung Pao Chicken", "image": "kung_pao_chicken.jpg", "usedIngredientCount": 4, "missedIngredientCount": 2, "likes": 310},
    {"id": 12, "title": "Sweet and Sour Pork", "image": "sweet_and_sour_pork.jpg", "usedIngredientCount": 5, "missedIngredientCount": 1, "likes": 290},
    {"id": 13, "title": "Spring Rolls", "image": "spring_rolls.jpg", "usedIngredientCount": 3, "missedIngredientCount": 2, "likes": 240},
    {"id": 14, "title": "Fried Rice", "image": "fried_rice.jpg", "usedIngredientCount": 2, "missedIngredientCount": 3, "likes": 270},
    {"id": 15, "title": "Dumplings", "image": "dumplings.jpg", "usedIngredientCount": 4, "missedIngredientCount": 2, "likes": 320},
    
    # Additional Recipes
    {"id": 16, "title": "chicken Tacos", "image": "chicken_tacos.jpg", "usedIngredientCount": 3, "missedIngredientCount": 2, "likes": 330},
    {"id": 17, "title": "Margherita Pizza", "image": "margherita_pizza.jpg", "usedIngredientCount": 5, "missedIngredientCount": 1, "likes": 410},
    {"id": 18, "title": "Tandoori Chicken", "image": "tandoori_chicken.jpg", "usedIngredientCount": 4, "missedIngredientCount": 2, "likes": 380},
    {"id": 19, "title": "Paneer Tikka", "image": "paneer_tikka.jpg", "usedIngredientCount": 3, "missedIngredientCount": 3, "likes": 260},
    {"id": 20, "title": "Egg Fried Rice", "image": "egg_fried_rice.jpg", "usedIngredientCount": 4, "missedIngredientCount": 2, "likes": 310},
    {"id": 21, "title": "Veggie Burger", "image": "veggie_burger.jpg", "usedIngredientCount": 3, "missedIngredientCount": 2, "likes": 230},
    {"id": 22, "title": "Pasta Primavera", "image": "pasta_primavera.jpg", "usedIngredientCount": 4, "missedIngredientCount": 2, "likes": 350},
    {"id": 23, "title": "Fish Tacos", "image": "fish_tacos.jpg", "usedIngredientCount": 3, "missedIngredientCount": 3, "likes": 280},
    {"id": 24, "title": "General Tso's Chicken", "image": "general_tsos_chicken.jpg", "usedIngredientCount": 4, "missedIngredientCount": 2, "likes": 360},
    {"id": 25, "title": "Tom Yum Soup", "image": "tom_yum_soup.jpg", "usedIngredientCount": 5, "missedIngredientCount": 1, "likes": 300},
]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": app.config["ALLOWED_ORIGINS"].split(",")}})

    # DB initialization
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    with app.app_context():
        db.create_all()

    spoon = SpoonacularClient(Config.SPOONACULAR_API_KEY)

    @app.route("/api/search", methods=["GET"])
    def search():
        # Extract query parameters
        ingredients = request.args.get("ingredients", "")
        data = spoon.find_by_ingredients(ingredients)
        
        # Simple filter to match some mock recipes
        filtered_recipes = [
            r for r in INDIAN_RECIPES if any(ing.lower() in r.get("title", "").lower() for ing in ingredients)
        ]
        
        return jsonify(filtered_recipes)
    
    @app.route("/api/recipes/<int:recipe_id>", methods=["GET"])
    def recipe_info(recipe_id):
        data = spoon.get_recipe_information(recipe_id, include_nutrition=True)
        return jsonify(data)

    @app.route("/api/grocery", methods=["POST"])
    def grocery():
        body = request.get_json()
        recipe_ids = body.get("recipeIds", [])
        recipes = [spoon.get_recipe_information(rid, include_nutrition=False) for rid in recipe_ids]
        items = aggregate_ingredients(recipes)
        return jsonify({"items": items, "deduped": True})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5001)
