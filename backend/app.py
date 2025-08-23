from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from services.spoonacular import SpoonacularClient, to_macro
from services.nutrition import sum_macros, aggregate_ingredients
from services.planner import daily_targets, build_week_plan
from models.db import db
from models.grocery_list import GroceryList
import json

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
        ingredients = request.args.get("ingredients", "")
        data = spoon.find_by_ingredients(ingredients)
        return jsonify(data)
    
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
    app.run(port=Config.PORT)
