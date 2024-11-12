/*
Search bar funtion by Evin S.
with Andrew C. article filter impelement together
type in key word and the article will sorted to it 
*/ 
// Function to filter articles based on selected categories and search input
function filterArticles() {
    const searchInput = document.getElementById('search').value.trim().toLowerCase();
    const checkboxes = document.querySelectorAll('input[name="category"]:checked');
    
    // Get the selected categories
    const selectedCategories = Array.from(checkboxes).map(cb => cb.value.trim().toLowerCase());
    
    // Get all articles
    const articles = document.querySelectorAll('.news-article');
    
    // Loop through the articles and display/hide them based on both search and selected categories
    articles.forEach(article => {
        let showArticle = true;

        // Check for search input match
        if (searchInput !== '') {
            const articleKeywords = article.getAttribute('keywords').split(" ").join("").split("|");
            const matchesSearch = articleKeywords.some(keyword => keyword.toLowerCase().includes(searchInput));
            if (!matchesSearch) {
                showArticle = false;
            }
        }

        // Check for category match
        if (selectedCategories.length > 0) {
            const articleCategories = article.getAttribute('keywords').split("|").map(cat => cat.trim().toLowerCase());
            const matchesCategory = articleCategories.some(category => selectedCategories.includes(category));
            if (!matchesCategory) {
                showArticle = false;
            }
        }

        // Show or hide the article based on both search and category filters
        article.style.display = showArticle ? 'block' : 'none';
    });
}

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Add event listener for search button
    document.getElementById('searchBtn').addEventListener('click', function(event) {
        event.preventDefault();
        filterArticles(); // Trigger filtering on search
    });
    
    // Add event listeners to category checkboxes
    const checkboxes = document.querySelectorAll('input[name="category"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', filterArticles); // Trigger filtering on category change
    });
    
    // Add event listener for clear button
    document.getElementById('clear').addEventListener('click', function() {
        // Clear the search input field
        document.getElementById('search').value = '';
        
        // Clear all checkboxes
        checkboxes.forEach(input => input.checked = false);
        
        // Show all articles
        document.querySelectorAll('.news-article').forEach(article => article.style.display = 'block');
    });
});