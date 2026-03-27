"""
Recipe Recommendation Engine Module
This module implements the recipe recommendation logic based on:
- Ingredients entered by user
- Food category (veg/non-veg/vegan)
- Cuisine type
"""

from models import Recipe, UserPreference
from bson import ObjectId
import math


class RecommendationEngine:
    """
    Recommendation engine for suggesting recipes based on user preferences.
    """
    
    def __init__(self, db):
        self.recipe_model = Recipe(db)
        self.preference_model = UserPreference(db)
    
    def get_recommendations(self, user_id=None, ingredients=None, category=None, cuisine=None, limit=10):
        """
        Get recipe recommendations based on various criteria.
        
        Args:
            user_id: Optional user ID for personalized recommendations
            ingredients: List of ingredients user has
            category: Food category preference (veg/non-veg/vegan)
            cuisine: Cuisine type preference
            limit: Maximum number of recipes to return
            
        Returns:
            list: List of recommended recipes with scores
        """
        # Get user preferences if user_id is provided
        user_preferences = None
        if user_id:
            user_preferences = self.preference_model.get_preferences(user_id)
        
        # Get all recipes
        all_recipes = self.recipe_model.get_all_recipes()
        
        # Score and filter recipes
        scored_recipes = []
        
        for recipe in all_recipes:
            score = self._calculate_recipe_score(
                recipe, 
                ingredients, 
                category, 
                cuisine, 
                user_preferences
            )
            
            # Only include recipes with positive scores
            if score > 0:
                recipe['recommendation_score'] = score
                scored_recipes.append(recipe)
        
        # Sort by score (descending)
        scored_recipes.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        # Return top results
        return scored_recipes[:limit]
    
    def _calculate_recipe_score(self, recipe, ingredients, category, cuisine, user_preferences):
        """
        Calculate recommendation score for a recipe.
        
        Scoring Logic:
        - Base score starts at 0
        - +30 points for each matching ingredient
        - +25 points for matching category
        - +20 points for matching cuisine
        - -50 points if recipe contains disliked ingredients
        - Bonus points for user's favorite cuisines
        
        Args:
            recipe: Recipe document
            ingredients: List of ingredients user has
            category: Category preference
            cuisine: Cuisine preference
            user_preferences: User's preference document
            
        Returns:
            float: Recommendation score
        """
        score = 0.0
        
        # Ingredient matching score
        if ingredients:
            recipe_ingredients = [ing.lower() for ing in recipe.get('ingredients', [])]
            matched_ingredients = 0
            
            for user_ing in ingredients:
                user_ing_lower = user_ing.lower().strip()
                for recipe_ing in recipe_ingredients:
                    if user_ing_lower in recipe_ing or recipe_ing in user_ing_lower:
                        matched_ingredients += 1
                        break
            
            # Calculate ingredient score (max 30 points per ingredient, up to 50 total)
            ingredient_score = min(matched_ingredients * 30, 50)
            score += ingredient_score
        
        # Category matching score (+25 points)
        if category and recipe.get('category', '').lower() == category.lower():
            score += 25
        
        # Cuisine matching score (+20 points)
        if cuisine and recipe.get('cuisine', '').lower() == cuisine.lower():
            score += 20
        
        # Check for user's favorite cuisines bonus (+15 points)
        if user_preferences and cuisine:
            favorite_cuisines = user_preferences.get('favorite_cuisines', [])
            if cuisine.lower() in [c.lower() for c in favorite_cuisines]:
                score += 15
        
        # Penalty for disliked ingredients
        if user_preferences:
            disliked = user_preferences.get('disliked_ingredients', [])
            recipe_ingredients = [ing.lower() for ing in recipe.get('ingredients', [])]
            
            for disliked_ing in disliked:
                disliked_lower = disliked_ing.lower()
                for recipe_ing in recipe_ingredients:
                    if disliked_lower in recipe_ing:
                        score -= 50
                        break
        
        # Category filtering (if user specifies category, heavily penalize wrong category)
        if category and recipe.get('category', '').lower() != category.lower():
            score -= 30
        
        return max(0, score)  # Return 0 if negative
    
    def get_recommendations_by_ingredients(self, ingredients, category=None, cuisine=None, limit=10):
        """
        Get recipe recommendations primarily based on ingredients.
        
        Args:
            ingredients: List of ingredients
            category: Optional category filter
            cuisine: Optional cuisine filter
            limit: Maximum recipes to return
            
        Returns:
            list: Recommended recipes
        """
        return self.get_recommendations(
            ingredients=ingredients,
            category=category,
            cuisine=cuisine,
            limit=limit
        )
    
    def get_similar_recipes(self, recipe_id, limit=5):
        """
        Get recipes similar to a given recipe.
        
        Similarity is based on:
        - Common ingredients
        - Same cuisine
        - Same category
        
        Args:
            recipe_id: Reference recipe ID
            limit: Number of similar recipes to return
            
        Returns:
            list: Similar recipes
        """
        return self.recipe_model.get_similar_recipes(recipe_id, limit)
    
    def get_recipes_by_category(self, category, limit=10):
        """
        Get recipes by category.
        
        Args:
            category: Food category
            limit: Maximum recipes to return
            
        Returns:
            list: Recipes in that category
        """
        recipes = self.recipe_model.get_recipes_by_category(category)
        return recipes[:limit]
    
    def get_recipes_by_cuisine(self, cuisine, limit=10):
        """
        Get recipes by cuisine type.
        
        Args:
            cuisine: Cuisine type
            limit: Maximum recipes to return
            
        Returns:
            list: Recipes of that cuisine
        """
        recipes = self.recipe_model.get_recipes_by_cuisine(cuisine)
        return recipes[:limit]
    
    def get_personalized_recommendations(self, user_id, limit=10):
        """
        Get personalized recommendations based on user preferences.
        
        Args:
            user_id: User's unique ID
            limit: Maximum recipes to return
            
        Returns:
            list: Personalized recommendations
        """
        user_preferences = self.preference_model.get_preferences(user_id)
        
        if not user_preferences:
            # If no preferences, return popular recipes
            return self.recipe_model.get_all_recipes()[:limit]
        
        dietary = user_preferences.get('dietary_preferences', [])
        favorite_cuisines = user_preferences.get('favorite_cuisines', [])
        
        # Use first dietary preference as category
        category = dietary[0] if dietary else None
        cuisine = favorite_cuisines[0] if favorite_cuisines else None
        
        return self.get_recommendations(
            user_id=user_id,
            category=category,
            cuisine=cuisine,
            limit=limit
        )


def calculate_relevance_score(user_ingredients, recipe_ingredients):
    """
    Calculate relevance score between user ingredients and recipe ingredients.
    
    Uses cosine similarity approach for ingredient matching.
    
    Args:
        user_ingredients: List of ingredients user has
        recipe_ingredients: List of recipe ingredients
        
    Returns:
        float: Relevance score (0 to 1)
    """
    if not user_ingredients or not recipe_ingredients:
        return 0.0
    
    # Normalize ingredients
    user_ings = set(ing.lower().strip() for ing in user_ingredients)
    recipe_ings = set(ing.lower().strip() for ing in recipe_ingredients)
    
    # Find intersection
    matching = user_ings.intersection(recipe_ings)
    
    # Calculate Jaccard similarity
    union = user_ings.union(recipe_ings)
    
    if not union:
        return 0.0
    
    return len(matching) / len(union)
