# Smart-Recipe-Grocery-Planner
The Smart Recipe &amp; Grocery Planner is a full-stack application designed to help users manage their meals efficiently. By entering available ingredients, users can find recipes, generate grocery lists, track nutritional information, and create customized weekly meal plans.

### Features
1. Recipe Suggestions
Description: Enter ingredients you have on hand, and the application suggests matching recipes using the Spoonacular API.
Tech: Uses the /api/search endpoint to fetch recipes based on ingredients.
2. Grocery List Generation
Description: Select recipes to automatically create a grocery shopping list, aggregating all necessary ingredients.
Tech: Uses the /api/grocery endpoint to collect ingredients from selected recipes, deduplicating them.
3. Nutrition Tracking
Description: View detailed nutritional information such as calories, proteins, fats, and carbohydrates for each recipe.
Tech: Utilizes the /api/nutrition/aggregate endpoint to summarize nutritional information from selected recipes.
4. AI Diet Planner
Description: Generate a 7-day meal plan based on user-specific goals such as weight loss, maintenance, or muscle gain.
Tech: Uses the /api/plan endpoint, considering user inputs for age, sex, activity level, and dietary preferences.

---

### Architecture
# Frontend
-Framework: React with Vite
-State Management: Zustand
-Routing: React Router
-Styling: TailwindCSS
-Structure:
-Pages: Search, Planner, Grocery, Recipe
-Components: IngredientInput, RecipeCard, RecipeList, NutritionPanel, -GroceryList

---

# Backend
-Framework: Flask
-Database: Optional SQLite (via SQLAlchemy)
-Validation: Marshmallow
-External API: Spoonacular

# Services:
  -Spoonacular API client
  -Nutrition helpers
  -Meal planner logic

**Setup Instructions**
-Prerequisites
  -Node.js
  -Python 3.10+
  -Spoonacular API Key

Backend Setup
--
-Clone the repository and navigate to the backend directory.
-Create a .env file with the following:
  -plaintext
  -FLASK_ENV=development
  -PORT=5001
  -SPOONACULAR_API_KEY=your_api_key_here
  -ALLOWED_ORIGINS=http://localhost:5173
  -DATABASE_URL=sqlite:///app.db

# Install Python dependencies:
  -bash
  -pip install -r requirements.txt
-Start the Flask server:
-bash
  -python app.py
-**Frontend Setup**
  -Navigate to the frontend directory.
  -Install frontend dependencies:
    -bash
    -npm install
  -Start the React development server:
    -bash
    -npm run dev
    
Deployment
--
-Refer to the deployment section in the project documentation for instructions on deploying using Docker or other services.

Contribution Guidelines
--
-Fork the repository
-Create a new branch (git checkout -b feature/YourFeature)
-Commit your changes (git commit -m 'Add some feature')
-Push to the branch (git push origin feature/YourFeature)
-Create a new Pull Request

License
--
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
--
For further inquiries, reach out via email or open an issue in the GitHub repository.
