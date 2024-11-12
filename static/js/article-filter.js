/**
 * Article filter by Andrew C.
 * Gets all the checkboxes in the search page, and listens if they are clicked.
 * If they are clicked, sort the articles based on the filters pressed.
 */

// Function to filter articles based on selected categories
function filterArticles() {
    // Get all checked checkboxes
    const checkboxes = document.querySelectorAll('input[name="category"]:checked');
    // Extract the values of checked checkboxes
    //Removing spaces for matching
    const selectedCategories = Array.from(checkboxes).map(cb => cb.value).join(",").split(" ").join("").split(",");
    // Get all articles
    const articles = document.querySelectorAll('.news-article');
    // Loop through the articles and display/hide them based on the selected categories
    articles.forEach(article => {
        article.style.display = 'none'; // Hide the article
        //Removing spaces for matching
        const articleCategory = article.getAttribute('keywords').split(" ").join("").split("|");
        //alert(articleCategory)
        // If the article category matches one of the selected categories, show it, otherwise hide it
        articleCategory.forEach(keyword => {
            if (selectedCategories.includes(keyword)) {
                article.style.display = 'block'; // Show the article
            }
        })
        if(selectedCategories[0] === ''){
            article.style.display = 'block';
        }
    });
}

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Add event listeners to checkboxes to trigger the filter function
    const checkboxes = document.querySelectorAll('input[name="category"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', filterArticles);
    });
});
