function changeContent(url){
	deactivate(url);
	$.ajax({ 
        type: "POST",
        url: "/" + url,
        data: {},
        success:function(res){
			document.getElementById("content").innerHTML = res;
			if(url == "signup") hideTooltips();
			else if(url == "viewpublicphotos") gallery();
			if(document.getElementById("modal")){
				$('modal').modal({
					backdrop: 'static',
					keyboard: false,
					show: true
				});
				$('#modal').modal('show');
				$('#modal').on('hidden.bs.modal', function () {
					if(document.getElementById("sessionError")) window.setTimeout(closeAndRedirect(), 3000);
				});
			}
		},
		error:function(){
			document.getElementById("content").innerHTML = "<p>Han error has ocurred</p>";
		}
    });
}

function deactivate(option){
	document.getElementById("signin").className = "";
	document.getElementById("signup").className = "";
	document.getElementById("viewpublicphotos").className = "";
	document.getElementById(option).className = "active";
}

function closeAndRedirect(){
	window.location.replace("/");
}

function hideTooltips(){
	if (screen.width < 768){
		var p = "bottom";
	}
	else {
		p = "right";
	}
	$('[data-toggle="tooltip"]').tooltip({
		trigger: 'manual',
		placement: p
	});
}

function signUp(){
	var validUser = validateForm();
	if(validUser) {
		$.ajax({ 
        type: "POST",
        url: "/newUser",
        data: {
        	'user': document.getElementById("user").value,
        	'email': document.getElementById("email").value,
        	'password': document.getElementById("password").value,
        	'confirmPassword': document.getElementById("confirmPassword").value,
        },
        success:function(res){
			document.getElementById("res").innerHTML = res;
			if(document.getElementById("modal")){
				$('modal').modal({
					backdrop: 'static',
					keyboard: false,
					show: true
				});
				$('#modal').on('hidden.bs.modal', function () {
					close();
				});
				$('#modal').modal('show');
			}
		},
		error:function(){
			document.getElementById("content").innerHTML = "<p>Han error has ocurred</p>";
		}
    });
	}
}

function login(){
	$.ajax({ 
    type: "POST",
    url: "/login",
    data: {
    	'user': document.getElementById("user").value,
    	'password': document.getElementById("password").value,
    },
    success:function(res){
		if (res == "correctLogin") {
			document.location.href = "/main";
		}
		else {
			document.getElementById("res").innerHTML = res;
			if(document.getElementById("modal")){
				$('modal').modal({
					backdrop: 'static',
					keyboard: false,
					show: true
				});
				$('#modal').on('hidden.bs.modal', function () {
					close();
				});
				$('#modal').modal('show');
				}
		}
	},
	error:function(){
		document.getElementById("content").innerHTML = "<p>Han error has ocurred</p>";
	}
});
}

function close(){
	changeContent("signin");
}
