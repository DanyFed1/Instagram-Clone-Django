document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    document.body.addEventListener('click', function(event) {
        if (event.target.classList.contains('follow-btn')) {
            event.preventDefault();
            const userId = event.target.getAttribute('data-user-id');
            fetch(`/accounts/subscribe/${userId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'subscribed') {
                    event.target.textContent = 'Unfollow';
                    event.target.classList.remove('follow-btn');
                    event.target.classList.add('unfollow-btn');
                }
            })
            .catch(error => console.error("Error:", error));
        } else if (event.target.classList.contains('unfollow-btn')) {
            event.preventDefault();
            const userId = event.target.getAttribute('data-user-id');
            fetch(`/accounts/unsubscribe/${userId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'unsubscribed') {
                    event.target.textContent = 'Follow';
                    event.target.classList.remove('unfollow-btn');
                    event.target.classList.add('follow-btn');
                }
            })
            .catch(error => console.error("Error:", error));
        }
    });
});
