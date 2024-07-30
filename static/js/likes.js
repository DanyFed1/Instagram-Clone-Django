document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-btn');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    likeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.getAttribute('data-post-id');

            fetch(`/posts/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                this.textContent = data.liked ? 'Unlike' : 'Like';
                const likesCounter = this.nextElementSibling;
                if (likesCounter) {
                    likesCounter.textContent = `${data.total_likes} Likes`;
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
