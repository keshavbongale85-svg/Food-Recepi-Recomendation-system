/**
 * Main JavaScript file for Food Recipe Recommendation System
 * Contains common utility functions used across the application
 */

// API Base URL - Change this if backend runs on different port
const API_BASE_URL = '';

// Helper function to make API calls
async function apiCall(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const config = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'An error occurred');
        }
        
        return data;
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

// Helper function to display notifications
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles dynamically
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        background-color: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#004e89'};
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Helper function to format cooking time
function formatCookingTime(minutes) {
    if (minutes < 60) {
        return `${minutes} min`;
    }
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`;
}

// Helper function to get category icon
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

// Helper function to create recipe card HTML
function createRecipeCardHTML(recipe) {
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

// Helper function to get URL parameters
function getURLParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

// Helper function to debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add CSS animation for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

// Check if user is logged in (utility function)
async function checkAuth() {
    try {
        const response = await fetch('/api/check_session');
        const data = await response.json();
        return data.logged_in;
    } catch (error) {
        return false;
    }
}

// Get current user info
async function getCurrentUser() {
    try {
        const response = await fetch('/api/check_session');
        return await response.json();
    } catch (error) {
        return { logged_in: false };
    }
}
