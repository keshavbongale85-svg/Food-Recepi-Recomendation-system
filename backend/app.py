"""
Food Recipe Recommendation System - Main Application
This is the main Flask application file that sets up the server and routes.
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from pymongo import MongoClient
import os

# Import modules
from database import init_db
from models import User, Recipe, UserPreference
from recommendation import RecommendationEngine
from routes import api, init_routes

# Create Flask app
# app = Flask(__name__)
app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

# Configuration
app.config['SECRET_KEY'] = 'food-recipe-secret-key-2024'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
app.config['MONGO_DB'] = 'food_recipe_db'

# Enable CORS for frontend-backend communication
CORS(app)

# Initialize database
client, db = init_db(app)

# Initialize routes with database
init_routes(db)

# Register Blueprint
app.register_blueprint(api)


# ==================== FRONTEND ROUTES ====================

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')


@app.route('/login')
def login_page():
    """Render the login page."""
    return render_template('login.html')


@app.route('/register')
def register_page():
    """Render the registration page."""
    return render_template('register.html')


@app.route('/search')
def search_page():
    """Render the recipe search page."""
    return render_template('search.html')


@app.route('/recipes')
def recipes_page():
    """Render the recipes listing page."""
    return render_template('recipes.html')


@app.route('/recipe/<recipe_id>')
def recipe_detail_page(recipe_id):
    """Render the recipe detail page."""
    return render_template('recipe_detail.html', recipe_id=recipe_id)


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


# ==================== MAIN ENTRY POINT ====================

if __name__ == '__main__':
    # Run the Flask application
    print("=" * 50)
    print("Food Recipe Recommendation System")
    print("=" * 50)
    print("\nServer running on: http://127.0.0.1:5000")
    print("\nAvailable API endpoints:")
    print("  - POST /api/register")
    print("  - POST /api/login")
    print("  - POST /api/logout")
    print("  - GET  /api/check_session")
    print("  - GET  /api/recipes")
    print("  - GET  /api/recipes/<id>")
    print("  - POST /api/recipes/search")
    print("  - GET  /api/recipes/category/<category>")
    print("  - GET  /api/recipes/cuisine/<cuisine>")
    print("  - GET  /api/recipes/<id>/similar")
    print("  - GET  /api/preferences")
    print("  - PUT  /api/preferences")
    print("  - POST /api/seed_recipes")
    print("\n Frontend pages:")
    print("  - http://127.0.0.1:5000/")
    print("  - http://127.0.0.1:5000/login")
    print("  - http://127.0.0.1:5000/register")
    print("  - http://127.0.0.1:5000/search")
    print("  - http://127.0.0.1:5000/recipes")
    print("  - http://127.0.0.1:5000/recipe/<id>")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
