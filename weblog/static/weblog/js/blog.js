const likeBtn = document.getElementById("like-btn");
const unlikeBtn = document.getElementById("unlike-btn");
const blogId = document.getElementById("blog-id").value;
const lNumber = document.getElementById("l-number");
const unlNumber = document.getElementById("unl-number");

function getCookie(name){
	let cookieValue = null;
	if(document.cookie && document.cookie !== ""){
		const cookies = document.cookie.split(";");
		for(let i=0; i<cookies.length; i++){
			const cookie = cookies[i].trim();
			if(cookie.substring(0, name.length +1) ===(name + "=")){
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}

	}
	return cookieValue;
}

const csrfToken = getCookie("csrftoken");

likeBtn.addEventListener("click", () => {
	//alert("liked")
	likeUnlike("likes", "unlikes", blogId)
})

unlikeBtn.addEventListener("click", () => {
	//alert("unliked")
    likeUnlike("unlikes", "likes", blogId)
 })

 document.getElementById("comment-form").addEventListener("submit", (e) => {
 	e.preventDefault();
 	const text = document.getElementById("comment-text").value;
 	if(text.trim() !== ""){
 		const formData = new FormData();
 		formData.append("comment", text)
 		comment(blogId, formData)
 	}

 })


function likeUnlike(like, other, id){
	fetch(`/${like}/${other}/${id}/`, {
		method : "POST",
		headers : {
			"X-CSRFToken" : csrfToken,
		}
	})
	.then(response => {
		if(!response.ok){
			alert("network error")
		}
		return response.json();
	})
	.then(data => {
		if(data.status === "ok"){
			const likes = data.likes;
			const unlikes = data.unlikes;
			lNumber.innerHTML = likes;
			unlNumber.innerHTML = unlikes;

		}
		else if(data.error){
			alert(data.error);
		}
	})
}


function comment(profile, data){
	fetch(`/comment/${profile}/`, {
		method: "POST",
		headers : {
			"X-CSRFToken":csrfToken,
		},
		body: data
	})
	.then(response => {
		if(!response.ok){
			alert("server error")
		}
		return response.json()
	})
	.then(data => {
		if(data.status === "ok"){

			const li = document.createElement("li")
			li.innerHTML = `<a href="/weblog/profile/${data.id}/">${data.writer}</a><br/><p>${data.new_comment}</p>`
			const combox = document.getElementById("comment-box")
			if(combox.firstChild){

				combox.insertBefore(li, combox.firstChild)
				document.getElementById("comment-text").value = "";
			}
			else{

				combox.appendChild(li);

				document.getElementById("comment-text").value = "";
			}

		}
	})
}