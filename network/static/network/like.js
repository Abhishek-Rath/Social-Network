document.addEventListener('DOMContentLoaded', function() {
    likes = document.querySelectorAll('.like-post');
    likes.forEach((like) => {
        updateLikes(like);
    });   
});

function updateLikes(like) {
    console.log(like);
    like.addEventListener('click', () => {
        const id = like.getAttribute('data-id'); 
        let like_status = like.getAttribute('data-like-status');
        let heart_icon = like.i
        let likes_count = document.querySelector(`#post-likes-count-${id}`)

        console.log(typeof(id), id);
        console.log(typeof(like_status), like_status);
        console.log(heart_icon);
        console.log("like button clicked");

        let form = new FormData();
        form.append("id", id);
        form.append("like_status", like_status);
        console.log(...form);
        fetch(`/like/`, {
            method: "POST",
            body: form
        }).then((response) => {
            if (!response.ok) {
                // error processing
                throw 'Error';
            }
            return response.json()
        })
        .then((data) => {
            console.log(data);
            // console.log(data.post_liked);
            if(data.status == 201 && data.post_liked == "liked") {
                like.innerHTML = `<i class="em em-heart" aria-role="presentation" aria-label="HEAVY BLACK HEART"></i>`;
                like.setAttribute('data-like-status', "liked")
            } else {
               like.innerHTML = `&#129293;`;
               like.setAttribute('data-like-status', "unliked")
            }
            likes_count.textContent = data.likes_count
        })
        .catch((e) => {
            console.log(e)
        }) 
            
    
    })
}