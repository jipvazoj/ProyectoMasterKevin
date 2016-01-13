function changeContent(url){
	deactivate(url);
	$.ajax({ 
        type: "POST",
        url: "/" + url,
        data: { },
        success:function(res){
			document.getElementById("content").innerHTML = res;
			if(url == "myprofile") hideTooltips();
			if(url = "uploadphoto"){
				$('#file-es').fileinput({
        			language: 'en',
					maxFileSize: 1000,
        			minFileCount: 1,
        			maxFileCount: 10,
        			showUpload: false,
        			allowedFileExtensions : ['jpg', 'png','gif', 'JPG', 'PNG', 'GIF'],
    			});
			}
			if(document.getElementById("modal")){
				$('modal').modal({
					backdrop: 'static',
					keyboard: false,
					show: true
				});
				$('#modal').modal('show');
				$('#modal').on('hidden.bs.modal', function () {
					window.setTimeout(closeAndRedirect(), 3000);
				});
			}
		},
		error:function(){
			document.getElementById("content").innerHTML = "<p>Han error has ocurred</p>";
		}
    });
}

function closeAndRedirect(){
	window.location.replace("/");
}

function backToMain(){
	window.location.replace("/main");
}

function checkPhotos(){
	var n = 0;
	var upload = true;
	jQuery.each(jQuery('#file-es')[0].files, function(i, file) {
    	n++;
		var name = file.name;
		var extension = name.substring(name.lastIndexOf('.') + 1).toLowerCase();
		if((extension != "jpg") && (extension != "png") && (extension != "gif")) {
			upload = false;
		}
    	var size = file.size;
    	size = size/1024;
    	if(size > 1000) {
    		upload = false;
    	}
	});
	if(n == 0 || n > 10) upload = false;
	return upload;
}

function deactivate(option){
	document.getElementById("viewphotos").className = "";
	document.getElementById("uploadphoto").className = "";
	document.getElementById("myprofile").className = "";
	document.getElementById(option).className = "active";
}

function changePassword(){
	var validUser = validateChangePassword();
	if(validUser) {
		$.ajax({ 
        type: "POST",
        url: "/changepassword",
        data: {
        	'password': document.getElementById("password").value,
        	'newPassword': document.getElementById("newPassword").value,
        	'confirmPassword': document.getElementById("confirmPassword").value,
        },
        success:function(res){
			document.getElementById("res").innerHTML = res;
			if(document.getElementById("changePasswordModal")){
				$('modal').modal({
					backdrop: 'static',
					keyboard: false,
					show: true
				});
				$('#changePasswordModal').modal('show');
				$('#changePasswordModal').on('hidden.bs.modal', function () {
					window.setTimeout(backToMain(), 3000);
				});
			}
		},
		error:function(){
			document.getElementById("content").innerHTML = "<p>Han error has ocurred</p>";
		}
    });
	}
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