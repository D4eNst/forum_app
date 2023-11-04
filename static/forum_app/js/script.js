document.addEventListener('DOMContentLoaded', function() {


    const likeButtons = document.querySelectorAll('.like-link');
    const likesCounts = document.querySelectorAll('.likes-count');

    likeButtons.forEach(function(likeButton) {
        likeButton.addEventListener('click', function() {
            const postId = likeButton.getAttribute('data-com-id');
            const userLiked = likeButton.getAttribute('data-liked');
            const likesCount = Array.from(likesCounts).find(element => element.getAttribute('data-com-id') === postId);
            // console.log(userLiked)

            // Отправляем AJAX-запрос на сервер для добавления/удаления лайка
            fetch(`/toggle-comment-like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrf_token,  // csrf_token должен быть доступен в шаблоне/**/
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ liked: userLiked,  likes_count: likesCount.textContent}),
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    likeButton.setAttribute('data-liked', 'true');
                    likeButton.textContent = 'Отменить';
                } else {
                    likeButton.setAttribute('data-liked', 'false');
                    likeButton.textContent = 'Лайк';
                }

                likesCount.textContent = "likes: " + data.likes_count;
            })
            .catch(error => console.error(error));
        });
    });


    const likePostButton = document.getElementById('like-post');
    const likesPostCount = document.getElementById('post-likes-count');

    likePostButton.addEventListener('click', function() {
        const postId = likePostButton.getAttribute('data-post-id');
        const userLiked = likePostButton.getAttribute('data-liked');

        // Отправляем AJAX-запрос на сервер для добавления/удаления лайка
        fetch(`/toggle-post-like/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token,  // csrf_token должен быть доступен в шаблоне/**/
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ liked: userLiked, likes_count: likesPostCount.textContent }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.liked) {
                likePostButton.setAttribute('data-liked', 'true');
                likePostButton.textContent = 'Отменить';
            } else {
                likePostButton.setAttribute('data-liked', 'false');
                likePostButton.textContent = 'Лайк';
            }
            likesPostCount.textContent = "Лайки: " + data.likes_count;
        })
        .catch(error => console.error(error));
    });



});

