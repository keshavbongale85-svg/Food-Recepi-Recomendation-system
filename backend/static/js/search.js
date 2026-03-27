/**
 * Search JavaScript file
 * Handles recipe search and recommendation functionality
 */

// Array to store selected ingredients
let selectedIngredients = [];

// DOM Elements
const ingredientInput = document.getElementById('ingredientInput');
const addIngredientBtn = document.getElementById('addIngredientBtn');
const ingredientTags = document.getElementById('ingredientTags');
const searchForm = document.getElementById('searchForm');
const resultsSection = document.getElementById('resultsSection');
const resultsGrid = document.getElementById('resultsGrid');
const resultsCount = document.getElementById('resultsCount');

// Initialize search functionality
if (searchForm) {
    initializeSearch();
}

function initializeSearch() {
    // Add ingredient on button click
    if (addIngredientBtn) {
        addIngredientBtn.addEventListener('click', addIngredient);
    }
    
    // Add ingredient on Enter key
    if (ingredientInput) {
        ingredientInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                addIngredient();
            }
        });
    }
    
    // Handle form submission
    searchForm.addEventListener('submit', handleSearch);
}

// Add ingredient to the list
function addIngredient() {
    const ingredient = ingredientInput.value.trim();
    
    if (ingredient && !selectedIngredients.includes(ingredient.toLowerCase())) {
        selectedIngredients.push(ingredient.toLowerCase());
        renderIngredientTags();
        ingredientInput.value = '';
    }
}

// Remove ingredient from the list
function removeIngredient(ingredient) {
    selectedIngredients = selectedIngredients.filter(i => i !== ingredient);
    renderIngredientTags();
}

// Render ingredient tags
function renderIngredientTags() {
    ingredientTags.innerHTML = '';
    
    selectedIngredients.forEach(ingredient => {
        const tag = document.createElement('span');
        tag.className = 'ingredient-tag';
        tag.innerHTML = `
            ${ingredient}
            <button type="button" onclick="removeIngredient('${ingredient}')">&times;</button>
        `;
        ingredientTags.appendChild(tag);
    });
}

// Handle search form submission
async function handleSearch(e) {
    e.preventDefault();
    
    // Get form values
    const category = document.querySelector('input[name="category"]:checked').value;
    const cuisine = document.getElementById('cuisine').value;
    
    // Show loading state
    resultsGrid.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i><p>Searching recipes...</p></div>';
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    try {
        const response = await fetch('/api/recipes/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ingredients: selectedIngredients,
                category: category || null,
                cuisine: cuisine || null,
                limit: 12
            }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data.recipes);
        } else {
            resultsGrid.innerHTML = '<p class="error-message">Error searching recipes. Please try again.</p>';
        }
    } catch (error) {
        console.error('Search error:', error);
        resultsGrid.innerHTML = '<p class="error-message">An error occurred. Please check your connection.</p>';
    }
}

// Display search results
function displayResults(recipes) {
    if (!recipes || recipes.length === 0) {
        resultsGrid.innerHTML = `
            <div class="no-results">
                <i class="fas fa-utensils"></i>
                <h3>No recipes found</h3>
                <p>Try different ingredients or adjust your filters</p>
            </div>
        `;
        resultsCount.textContent = '0 recipes found';
        return;
    }
    
    resultsCount.textContent = `${recipes.length} recipes found`;
    
    resultsGrid.innerHTML = '';
    
    recipes.forEach(recipe => {
        const card = createRecipeCard(recipe);
        resultsGrid.innerHTML += card;
    });
}

// Create recipe card HTML
function createRecipeCard(recipe) {
    const categoryIcon = getCategoryIcon(recipe.category);
    const imageUrl = recipe.image_url || 'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=400';
    const score = recipe.recommendation_score ? Math.round(recipe.recommendation_score) : 0;
    
    return `
        <div class="recipe-card">
            <div class="recipe-image">
                <img src="${imageUrl}" alt="${recipe.name}" onerror="this.src='https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=400'">
                <span class="recipe-category ${recipe.category}">
                    ${categoryIcon} ${recipe.category}
                </span>
                ${score > 0 ? `<span class="recipe-score" title="Match Score">${score}% Match</span>` : ''}
            </div>
            <div class="recipe-content">
                <h3>${recipe.name}</h3>
                <div class="recipe-meta">
                    <span><i class="fas fa-globe"></i> ${recipe.cuisine}</span>
                    <span><i class="fas fa-clock"></i> ${recipe.cooking_time} min</span>
                    <span><i class="fas fa-signal"></i> ${recipe.difficulty}</span>
                </div>
                <div class="recipe-ingredients-preview">
                    <small>${recipe.ingredients.slice(0, 3).join(', ')}${recipe.ingredients.length > 3 ? '...' : ''}</small>
                </div>
                <a href="/recipe/${recipe._id}" class="btn btn-outline btn-sm">View Recipe</a>
            </div>
        </div>
    `;
}

// Get category icon
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

// Make functions globally available
window.removeIngredient = removeIngredient;
