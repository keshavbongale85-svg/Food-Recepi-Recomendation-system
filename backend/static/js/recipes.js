/**
 * Recipes JavaScript file
 * Handles displaying and filtering all recipes
 */

// Store all recipes globally
let allRecipes = [];

// DOM Elements
const recipesGrid = document.getElementById('recipesGrid');
const loadingState = document.getElementById('loadingState');
const noResults = document.getElementById('noResults');
const categoryFilter = document.getElementById('categoryFilter');
const cuisineFilter = document.getElementById('cuisineFilter');

// Load recipes on page load
if (recipesGrid) {
    loadRecipes();
}

async function loadRecipes() {
    try {
        const response = await fetch('/api/recipes');
        const data = await response.json();
        
        loadingState.style.display = 'none';
        
        if (data.recipes && data.recipes.length > 0) {
            allRecipes = data.recipes;
            displayRecipes(allRecipes);
        } else {
            noResults.style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading recipes:', error);
        loadingState.innerHTML = '<p>Error loading recipes. Please try again later.</p>';
    }
}

function displayRecipes(recipes) {
    recipesGrid.innerHTML = '';
    
    if (recipes.length === 0) {
        noResults.style.display = 'block';
        return;
    }
    
    noResults.style.display = 'none';
    
    recipes.forEach(recipe => {
        const card = createRecipeCard(recipe);
        recipesGrid.innerHTML += card;
    });
}

function createRecipeCard(recipe) {
    const categoryIcon = getCategoryIcon(recipe.category);
    const imageUrl = recipe.image_url || 'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=400';
    
    return `
        <div class="recipe-card">
            <div class="recipe-image">
                <img src="${imageUrl}" alt="${recipe.name}" onerror="this.src='https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=400'">
                <span class="recipe-category ${recipe.category}">
                    ${categoryIcon} ${recipe.category}
                </span>
            </div>
            <div class="recipe-content">
                <h3>${recipe.name}</h3>
                <div class="recipe-meta">
                    <span><i class="fas fa-globe"></i> ${recipe.cuisine}</span>
                    <span><i class="fas fa-clock"></i> ${recipe.cooking_time} min</span>
                    <span><i class="fas fa-signal"></i> ${recipe.difficulty}</span>
                </div>
                <a href="/recipe/${recipe._id}" class="btn btn-outline btn-sm">View Recipe</a>
            </div>
        </div>
    `;
}

function getCategoryIcon(category) {
    switch (category) {
        case 'veg':
            return '<i class="fas fa-leaf"></i>';
        case 'non-veg':
            return '<i class="fas fa-drumstick-bite"></i>';
        case 'vegan':
            return '<i class="fas fa-seedling"></i>';
        default:
            return '<i class="fas fa-utensils"></i>';
    }
}

// Filter recipes based on selected options
function filterRecipes() {
    const category = categoryFilter ? categoryFilter.value : '';
    const cuisine = cuisineFilter ? cuisineFilter.value : '';
    
    let filtered = allRecipes;
    
    // Filter by category
    if (category) {
        filtered = filtered.filter(recipe => recipe.category === category);
    }
    
    // Filter by cuisine
    if (cuisine) {
        filtered = filtered.filter(recipe => 
            recipe.cuisine.toLowerCase() === cuisine.toLowerCase()
        );
    }
    
    displayRecipes(filtered);
}

// Make function globally available
window.filterRecipes = filterRecipes;
