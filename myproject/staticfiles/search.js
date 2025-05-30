document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchButton = document.getElementById("search-btn");
    const resultsList = document.getElementById("results-list");
    const categoryDropdown = document.querySelector(".category-dropdown");
    const darkModeToggle = document.querySelector(".toggle-dark-mode");
    
    // Function to toggle dark mode
    function toggleDarkMode() {
        document.body.classList.toggle("dark-mode");
        const isDarkMode = document.body.classList.contains("dark-mode");
        localStorage.setItem("darkMode", isDarkMode);
        darkModeToggle.textContent = isDarkMode ? "☀️" : "🌙";
    }

    // Check and apply dark mode from localStorage
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark-mode");
        darkModeToggle.textContent = "☀️";
    }

    // Add event listener for dark mode toggle
    darkModeToggle.addEventListener("click", toggleDarkMode);

    searchButton.addEventListener("click", function () {
        const query = searchInput.value.toLowerCase().trim();
        const selectedCategory = categoryDropdown.value;

        resultsList.innerHTML = ""; // Clear previous results

        // Retrieve stored posts
        let posts = JSON.parse(localStorage.getItem("posts")) || [];

        // Filter by category
        let filteredPosts = posts.filter(post => selectedCategory === "all" || post.category === selectedCategory);

        // Filter by search term (hashtags or words)
        if (query) {
            filteredPosts = filteredPosts.filter(post => post.text.toLowerCase().includes(query));
        }

        // Display results
        if (filteredPosts.length > 0) {
            filteredPosts.forEach(post => {
                const li = document.createElement("li");
                li.textContent = post.text;
                resultsList.appendChild(li);
            });
        } else {
            const li = document.createElement("li");
            li.textContent = "No results found.";
            resultsList.appendChild(li);
        }
    });
});
