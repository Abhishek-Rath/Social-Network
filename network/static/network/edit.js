import { getCookie } from './csrf.js';

document.addEventListener('DOMContentLoaded', function() {
    const editBtn = document.querySelectorAll('.edit-post');
    editBtn.forEach((edit) => {
        edit.addEventListener('click', () => {
            Edit(edit);
        })
    })    
})

function Edit(edit) {
    console.log(edit);
    
    const id = edit.dataset.id; 
    console.log(typeof(id), id);

    const post = document.querySelector(`#post-id-${id}`);
    post.style.display = 'none';

    const textarea = document.querySelector(`#post-edit-${id}`);
    textarea.style.display = 'block';

    const save = document.querySelector(`#edit-btn-${id}`);
    save.style.display = 'block';
    save.addEventListener('click', () => {
        editPost(id, textarea.value);
        save.style.display = 'none';
    })
    // save.style.display = 'none';
}

function editPost(id, post) {
    let form = new FormData();
    form.append("id", id);
    form.append("newPost", post.trim());

    let csrftoken = getCookie('csrftoken');
  
    fetch("/edit/", {
      method: "POST",
      body: form,
      headers: {'X-CSRFToken': csrftoken }
    }).then((res) => {
      document.querySelector(`#post-id-${id}`).textContent = post;
      document.querySelector(`#post-id-${id}`).style.display = 'block';
      document.querySelector(`#post-edit-${id}`).style.display = 'none';
      document.querySelector(`#post-edit-${id}`).value = post.trim();
    });
}