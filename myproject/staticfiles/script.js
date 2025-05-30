// Home page
// JavaScript to Handle Posts & Dark Mode
document.addEventListener("DOMContentLoaded", function () {
    let posts = JSON.parse(localStorage.getItem("posts")) || [];
    let postFeed = document.getElementById("postFeed");

    posts.forEach((post, index) => {
        let postElement = `
            <div class="post-card">
                <div class="post-header">
                    <img alt="User profile picture" class="user-avatar" src="https://placehold.co/40x40"/>
                    <div>
                        <h3 class="user-name">User Name</h3>
                        <p class="post-time">${post.time}</p>
                    </div>
                </div>
                <img alt="Uploaded media" class="post-image" src="${post.imageUrl}"/>
                <p class="post-caption">${post.caption} <span class="post-category">#${post.category}</span></p>
                <div class="post-actions">
                    <button class="like-btn" onclick="toggleLike(${index})" id="like-btn-${index}">
                        <i class="far fa-heart" id="like-icon-${index}"></i> <span id="likes-count-${index}">${post.likes}</span>
                    </button>
                    <button class="save-btn" onclick="toggleSave(${index})" id="save-btn-${index}">
                        <i class="far fa-bookmark" id="save-icon-${index}"></i>
                    </button>
                </div>
            </div>`;
        postFeed.innerHTML += postElement;
    });
});

function toggleLike(index) {
    let posts = JSON.parse(localStorage.getItem("posts")) || [];
    let likeBtn = document.getElementById(`like-btn-${index}`);
    let likeIcon = document.getElementById(`like-icon-${index}`);
    let likesCount = document.getElementById(`likes-count-${index}`);

    if (likeBtn.classList.contains('liked')) {
        // Unlike
        posts[index].likes--;
        likeIcon.classList.replace('fas', 'far');
        likeIcon.style.color = 'black';
    } else {
        // Like
        posts[index].likes++;
        likeIcon.classList.replace('far', 'fas');
        likeIcon.style.color = '#e63946'; // Red color for liked
    }

    likeBtn.classList.toggle('liked');
    likesCount.textContent = posts[index].likes;
    localStorage.setItem("posts", JSON.stringify(posts));
}

function toggleSave(index) {
    let saveIcon = document.getElementById(`save-icon-${index}`);
    saveIcon.classList.toggle('fas');
    saveIcon.style.color = saveIcon.classList.contains('fas') ? '#007bff' : 'black'; // Blue for saved
}

// Dark Mode Toggle
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const icon = document.querySelector(".toggle-dark-mode");
    icon.textContent = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
}        

