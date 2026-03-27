"""
API Routes Module
This module defines all REST API endpoints for the Food Recipe Recommendation System.
"""

from flask import Blueprint, request, jsonify, session
from models import User, Recipe, UserPreference
from recommendation import RecommendationEngine
from bson import ObjectId
import json
import hashlib

# Create Blueprint for API routes
api = Blueprint('api', __name__)


def serialize_doc(doc):
    """
    Convert MongoDB document to JSON-serializable format.
    
    Args:
        doc: MongoDB document
        
    Returns:
        dict: JSON-serializable dictionary
    """
    if doc is None:
        return None
    
    result = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            result[key] = str(value)
        elif isinstance(value, list):
            result[key] = value
        elif hasattr(value, 'isoformat'):
            result[key] = value.isoformat()
        else:
            result[key] = value
    return result


# Initialize models (will be set in app.py)
db = None


def init_routes(database):
    """
    Initialize routes with database instance.
    
    Args:
        database: MongoDB database instance
    """
    global db
    db = database


# ==================== AUTH ROUTES ====================

@api.route('/api/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Request body:
        username: str
        email: str
        password: str
        
    Returns:
        JSON: Success message with user data or error
    """
    try:
        data = request.get_json()
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'error': 'All fields are required'}), 400
        
        user_model = User(db)
        
        # Check if user already exists
        if user_model.get_user_by_email(email):
            return jsonify({'error': 'Email already registered'}), 400
        
        if user_model.get_user_by_username(username):
            return jsonify({'error': 'Username already taken'}), 400
        
        # Hash password (simple SHA-256 for demo)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Create user
        user = user_model.create_user(username, email, hashed_password)
        
        if user:
            # Create default preferences
            pref_model = UserPreference(db)
            pref_model.create_preferences(str(user['_id']))
            
            return jsonify({
                'message': 'User registered successfully',
                'user': serialize_doc(user)
            }), 201
        else:
            return jsonify({'error': 'Failed to register user'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/api/login', methods=['POST'])
def login():
    """
    Login user.
    
    Request body:
        email: str
        password: str
        
    Returns:
        JSON: Success message with user data or error
    """
    try:
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user_model = User(db)
        user = user_model.get_user_by_email(email)
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if user['password'] != hashed_password:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Store user in session
        session['user_id'] = str(user['_id'])
        session['username'] = user['username']
        
        return jsonify({
            'message': 'Login successful',
            'user': serialize_doc(user)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/api/logout', methods=['POST'])
def logout():
    """
    Logout user.
    
    Returns:
        JSON: Success message
    """
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


@api.route('/api/check_session', methods=['GET'])
def check_session():
    """
    Check if user is logged in.
    
    Returns:
        JSON: User session data or error
    """
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user_id': session.get('user_id'),
            'username': session.get('username')
        }), 200
    else:
        return jsonify({'logged_in': False}), 200


# ==================== RECIPE ROUTES ====================

@api.route('/api/recipes', methods=['GET'])
def get_all_recipes():
    """
    Get all recipes.
    
    Query parameters:
        limit: int (optional)
        
    Returns:
        JSON: List of all recipes
    """
    try:
        recipe_model = Recipe(db)
        recipes = recipe_model.get_all_recipes()
        
        # Convert ObjectId to string for JSON
        serialized_recipes = [serialize_doc(r) for r in recipes]
        
        return jsonify({
            'recipes': serialized_recipes,
            'count': len(serialized_recipes)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/api/recipes/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """
    Get a specific recipe by ID.
    
    Args:
        recipe_id: Recipe's unique ID
        
    Returns:
        JSON: Recipe details or error
    """
    try:
        recipe_model = Recipe(db)
        recipe = recipe_model.get_recipe_by_id(recipe_id)
        
        if recipe:
            return jsonify(serialize_doc(recipe)), 200
        else:
            return jsonify({'error': 'Recipe not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/api/recipes/search', methods=['POST'])
def search_recipes():
    """
    Search recipes based on ingredients and filters.
    
    Request body:
        ingredients: list of strings (optional)
        category: str (optional) - veg/non-veg/vegan
        cuisine: str (optional)
        limit: int (optional)
        
    Returns:
        JSON: List of matching recipes with scores
    """
    try:
        data = request.get_json()
        
        ingredients = data.get('ingredients', [])
        category = data.get('category')
        cuisine = data.get('cuisine')
        limit = data.get('limit', 10)
        
        recommendation_engine = RecommendationEngine(db)
        
        recipes = recommendation_engine.get_recommendations(
            ingredients=ingredients,
            category=category,
            cuisine=cuisine,
            limit=limit
        )
        
        serialized_recipes = [serialize_doc(r) for r in recipes]
        
        return jsonify({
            'recipes': serialized_recipes,
            'count': len(serialized_recipes)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/api/recipes/category/<category>', methods=['GET'])
def get_recipes_by_category(category):
    """
    Get recipes by category.
    
    Args:
        category: Food category (veg/non-veg/vegan)
        
    Returns:
        JSON: List of recipes in that category
    """
    try:
        recipe_model = Recipe(db)
        recipes = recipe_model.get_recipes_by_category(category)
        
        serialized_recipes = [serialize_doc(r) for r in recipes]
        
        return jsonify({
            'recipes': serialized_recipes,
            'count': len(serialized_recipes)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/api/recipes/cuisine/<cuisine>', methods=['GET'])
def get_recipes_by_cuisine(cuisine):
    """
    Get recipes by cuisine type.
    
    Args:
        cuisine: Cuisine type
        
    Returns:
        JSON: List of recipes of that cuisine
    """
    try:
        recipe_model = Recipe(db)
        recipes = recipe_model.get_recipes_by_cuisine(cuisine)
        
        serialized_recipes = [serialize_doc(r) for r in recipes]
        
        return jsonify({
            'recipes': serialized_recipes,
            'count': len(serialized_recipes)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/api/recipes/<recipe_id>/similar', methods=['GET'])
def get_similar_recipes(recipe_id):
    """
    Get similar recipes to a given recipe.
    
    Args:
        recipe_id: Reference recipe ID
        
    Returns:
        JSON: List of similar recipes
    """
    try:
        recommendation_engine = RecommendationEngine(db)
        recipes = recommendation_engine.get_similar_recipes(recipe_id)
        
        serialized_recipes = [serialize_doc(r) for r in recipes]
        
        return jsonify({
            'recipes': serialized_recipes,
            'count': len(serialized_recipes)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== PREFERENCE ROUTES ====================

@api.route('/api/preferences', methods=['GET'])
def get_preferences():
    """
    Get current user's preferences.
    
    Returns:
        JSON: User preferences or error
    """
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        pref_model = UserPreference(db)
        preferences = pref_model.get_preferences(session['user_id'])
        
        if preferences:
            return jsonify(serialize_doc(preferences)), 200
        else:
            return jsonify({'error': 'Preferences not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/api/preferences', methods=['PUT'])
def update_preferences():
    """
    Update user preferences.
    
    Request body:
        dietary_preferences: list (optional)
        favorite_cuisines: list (optional)
        disliked_ingredients: list (optional)
        
    Returns:
        JSON: Success message or error
    """
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        
        pref_model = UserPreference(db)
        
        update_data = {}
        if 'dietary_preferences' in data:
            update_data['dietary_preferences'] = data['dietary_preferences']
        if 'favorite_cuisines' in data:
            update_data['favorite_cuisines'] = data['favorite_cuisines']
        if 'disliked_ingredients' in data:
            update_data['disliked_ingredients'] = data['disliked_ingredients']
        
        success = pref_model.update_preferences(session['user_id'], update_data)
        
        if success:
            return jsonify({'message': 'Preferences updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update preferences'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== RECIPE CREATION ROUTES ====================

@api.route('/api/recipes', methods=['POST'])
def create_recipe():
    """
    Create a new recipe (admin route).
    
    Request body:
        name: str
        ingredients: list
        steps: list
        category: str
        cuisine: str
        image_url: str (optional)
        cooking_time: int (optional)
        difficulty: str (optional)
        
    Returns:
        JSON: Created recipe or error
    """
    try:
        data = request.get_json()
        
        required_fields = ['name', 'ingredients', 'steps', 'category', 'cuisine']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        recipe_model = Recipe(db)
        recipe = recipe_model.create_recipe(
            name=data['name'],
            ingredients=data['ingredients'],
            steps=data['steps'],
            category=data['category'],
            cuisine=data['cuisine'],
            image_url=data.get('image_url', ''),
            cooking_time=data.get('cooking_time', 30),
            difficulty=data.get('difficulty', 'Medium')
        )
        
        if recipe:
            return jsonify(serialize_doc(recipe)), 201
        else:
            return jsonify({'error': 'Failed to create recipe'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/api/seed_recipes', methods=['POST'])
def seed_recipes():
    """
    Seed database with sample recipes from JSON file.
    
    Returns:
        JSON: Success message with number of recipes added
    """
    try:
        import os
        from datetime import datetime
        
        recipe_model = Recipe(db)
        
        # Load recipes from JSON file
        json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_recipes.json')
        
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            sample_recipes = data.get('recipes', [])
        
        # Add timestamps to each recipe
        for recipe in sample_recipes:
            recipe['created_at'] = datetime.utcnow()
            recipe['updated_at'] = datetime.utcnow()
        
        # Insert recipes
        ids = recipe_model.bulk_insert_recipes(sample_recipes)
        
        return jsonify({
            'message': 'Recipes seeded successfully',
            'count': len(ids)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
