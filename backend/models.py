"""
MongoDB Models Module
This module defines the data models for Users, Recipes, and User Preferences.
"""

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import json


class User:
    """
    User model for handling user-related database operations.
    """
    
    def __init__(self, db):
        self.collection = db['users']
    
    def create_user(self, username, email, password):
        """
        Create a new user in the database.
        
        Args:
            username: User's username
            email: User's email address
            password: User's password (should be hashed)
            
        Returns:
            dict: Created user document or None if error
        """
        user_data = {
            'username': username,
            'email': email,
            'password': password,  # In production, hash this!
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        try:
            result = self.collection.insert_one(user_data)
            user_data['_id'] = result.inserted_id
            return user_data
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user_by_email(self, email):
        """
        Get user by email address.
        
        Args:
            email: User's email address
            
        Returns:
            dict: User document or None
        """
        return self.collection.find_one({'email': email})
    
    def get_user_by_id(self, user_id):
        """
        Get user by ID.
        
        Args:
            user_id: User's unique ID
            
        Returns:
            dict: User document or None
        """
        return self.collection.find_one({'_id': ObjectId(user_id)})
    
    def get_user_by_username(self, username):
        """
        Get user by username.
        
        Args:
            username: User's username
            
        Returns:
            dict: User document or None
        """
        return self.collection.find_one({'username': username})


class Recipe:
    """
    Recipe model for handling recipe-related database operations.
    """
    
    def __init__(self, db):
        self.collection = db['recipes']
    
    def create_recipe(self, name, ingredients, steps, category, cuisine, image_url='', cooking_time=30, difficulty='Medium'):
        """
        Create a new recipe in the database.
        
        Args:
            name: Recipe name
            ingredients: List of ingredients
            steps: List of cooking steps
            category: Food category (veg/non-veg/vegan)
            cuisine: Cuisine type
            image_url: URL to recipe image
            cooking_time: Cooking time in minutes
            difficulty: Difficulty level
            
        Returns:
            dict: Created recipe document or None if error
        """
        recipe_data = {
            'name': name,
            'ingredients': ingredients,
            'steps': steps,
            'category': category.lower(),
            'cuisine': cuisine,
            'image_url': image_url,
            'cooking_time': cooking_time,
            'difficulty': difficulty,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        try:
            result = self.collection.insert_one(recipe_data)
            recipe_data['_id'] = result.inserted_id
            return recipe_data
        except Exception as e:
            print(f"Error creating recipe: {e}")
            return None
    
    def get_all_recipes(self):
        """
        Get all recipes from the database.
        
        Returns:
            list: List of all recipe documents
        """
        return list(self.collection.find())
    
    def get_recipe_by_id(self, recipe_id):
        """
        Get recipe by ID.
        
        Args:
            recipe_id: Recipe's unique ID
            
        Returns:
            dict: Recipe document or None
        """
        try:
            return self.collection.find_one({'_id': ObjectId(recipe_id)})
        except Exception:
            return None
    
    def search_by_ingredients(self, ingredients, category=None, cuisine=None):
        """
        Search recipes by ingredients.
        
        Args:
            ingredients: List of ingredients to search
            category: Optional food category filter
            cuisine: Optional cuisine type filter
            
        Returns:
            list: List of matching recipes
        """
        # Create case-insensitive regex for each ingredient
        query = {
            'ingredients': {
                '$regex': '|'.join(ingredients),
                '$options': 'i'
            }
        }
        
        # Add category filter if provided
        if category:
            query['category'] = category.lower()
        
        # Add cuisine filter if provided
        if cuisine:
            query['cuisine'] = {'$regex': cuisine, '$options': 'i'}
        
        return list(self.collection.find(query))
    
    def get_recipes_by_category(self, category):
        """
        Get all recipes by category.
        
        Args:
            category: Food category (veg/non-veg/vegan)
            
        Returns:
            list: List of recipes in that category
        """
        return list(self.collection.find({'category': category.lower()}))
    
    def get_recipes_by_cuisine(self, cuisine):
        """
        Get all recipes by cuisine type.
        
        Args:
            cuisine: Cuisine type
            
        Returns:
            list: List of recipes of that cuisine
        """
        return list(self.collection.find({'cuisine': {'$regex': cuisine, '$options': 'i'}}))
    
    def get_similar_recipes(self, recipe_id, limit=5):
        """
        Get similar recipes based on ingredients and cuisine.
        
        Args:
            recipe_id: Reference recipe ID
            limit: Maximum number of similar recipes to return
            
        Returns:
            list: List of similar recipes
        """
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return []
        
        # Find recipes with similar ingredients
        ingredients = recipe.get('ingredients', [])
        if ingredients:
            # Get recipes with overlapping ingredients
            similar = self.collection.find({
                '_id': {'$ne': ObjectId(recipe_id)},
                '$or': [
                    {'ingredients': {'$in': ingredients}},
                    {'cuisine': recipe.get('cuisine', '')}
                ]
            }).limit(limit)
            return list(similar)
        
        return []
    
    def bulk_insert_recipes(self, recipes):
        """
        Insert multiple recipes at once.
        
        Args:
            recipes: List of recipe dictionaries
            
        Returns:
            list: List of inserted recipe IDs
        """
        try:
            result = self.collection.insert_many(recipes)
            return result.inserted_ids
        except Exception as e:
            print(f"Error bulk inserting recipes: {e}")
            return []


class UserPreference:
    """
    User Preference model for storing user food preferences.
    """
    
    def __init__(self, db):
        self.collection = db['user_preferences']
    
    def create_preferences(self, user_id, dietary_preferences=None, favorite_cuisines=None, disliked_ingredients=None):
        """
        Create user preferences.
        
        Args:
            user_id: User's unique ID
            dietary_preferences: List of dietary preferences (veg, non-veg, vegan)
            favorite_cuisines: List of favorite cuisine types
            disliked_ingredients: List of ingredients user dislikes
            
        Returns:
            dict: Created preferences document or None
        """
        preference_data = {
            'user_id': ObjectId(user_id),
            'dietary_preferences': dietary_preferences or [],
            'favorite_cuisines': favorite_cuisines or [],
            'disliked_ingredients': disliked_ingredients or [],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        try:
            result = self.collection.insert_one(preference_data)
            preference_data['_id'] = result.inserted_id
            return preference_data
        except Exception as e:
            print(f"Error creating preferences: {e}")
            return None
    
    def get_preferences(self, user_id):
        """
        Get user preferences.
        
        Args:
            user_id: User's unique ID
            
        Returns:
            dict: Preferences document or None
        """
        try:
            return self.collection.find_one({'user_id': ObjectId(user_id)})
        except Exception:
            return None
    
    def update_preferences(self, user_id, update_data):
        """
        Update user preferences.
        
        Args:
            user_id: User's unique ID
            update_data: Dictionary of fields to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'user_id': ObjectId(user_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating preferences: {e}")
            return False
