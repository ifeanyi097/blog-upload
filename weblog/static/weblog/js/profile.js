 const followBtn  = document.getElementById("follow-btn");
 const followers = document.getElementById("followers");
function getCookie(name){
	let cookieValue =null;
	if(document.cookie && document.cookie !== ""){
		const cookies = document.cookie.split(";");
		for(let i=0; i<cookies.length; i++){
			const cookie = cookies[i].trim();
			if(cookie.substring(0,name.length + 1) === (name + "=")){
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
			}
		}
	}
	return cookieValue;
}

const csrfToken = getCookie("csrftoken");

followBtn.addEventListener("click", () => {

	profile = followBtn.dataset.profileId;
//	alert("follow?")
	follow(profile);
})

 function follow(profile){
 	fetch(`/follow/${profile}/`,{
 		method: "POST",
 		headers: {
 			"X-CSRFToken":csrfToken
 		},

 	})
 	.then(response => {
 		if(!response.ok){
 			alert("server error")
 		}
 		return response.json();
 	})
 	.then(data => {
 		if(data.status === "ok"){
 			followers.innerHTML = data.followers;
 		}
 		else if(data.error){
 			alert(data.error)
 		}
 	})
 }