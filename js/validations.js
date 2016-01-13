function checkUsedEmail(){
checkEmail = document.getElementById("email").value;
var unusedEmail = true;
$.ajax({ 
        type: "POST",
        url: "/checkEmail",
        data: {
        	email: checkEmail
        },
        async: false,
        success:function(datos){
			if(datos == "NotValidEmail"){
				unusedEmail = false;
			}
		},
		error:function(){
			document.getElementById("content").innerHTML = "<p>Lo sentimos se ha producido un error</p>";
			unusedEmail = false;
		}
    });
    return unusedEmail;
}

function checkUsedUser(){
checkUser = document.getElementById("user").value;
var unusedUser = true;
$.ajax({ 
        type: "POST",
        url: "/checkUser",
        data: {
        	user: checkUser
        },
        async: false,
        success:function(datos){
			if(datos == "NotValidUser"){
				unusedUser = false;
			}
		},
		error:function(){
			document.getElementById("content").innerHTML = "<p>Lo sentimos se ha producido un error</p>";
			unusedUser = false;
		}
    });
 return unusedUser;
}

function validateUser(){
	var validUser = false;
	var e = document.getElementById("user").value;
	var patron = /^[\w]+$/;
	if(e.search(patron)!=0 || (e.length>50)){
		$("#user").attr('data-original-title', "Invalid username");
	}
	else {
		var unusedUser = checkUsedUser();
		if(unusedUser){
			validUser = true;
		}
		else {
			$("#user").attr('data-original-title', "Username already exists");
		}
	}
	if(!validUser){
		$("#user").tooltip('show');
	}
	else {
		$("#user").tooltip('hide');
	}
	return validUser;
}

function validateEmail(){
	var validEmail = false;
	var e = document.getElementById("email").value;
	var patron = /^[A-Za-z0-9_\.-]+@[a-z]+(\.[a-z]+)?\.([a-z]{2,3})$/;
	if(e.search(patron)!=0 || (e.length>50)){
		$("#email").attr('data-original-title', "Invalid email");
	}
	else{
		var unusedEmail = checkUsedEmail();
		if(unusedEmail){
			validEmail = true;
		}
		else {
			$("#email").attr('data-original-title', "Email already exists");
		}
	}
	if(!validEmail){
		$("#email").tooltip('show');
	}
	else {
		$("#email").tooltip('hide');
	}
	return validEmail;
}

function validatePassword(){
	var e = document.getElementById("password").value;
	var patron = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
	if(e.search(patron)!=0){
		 $("#password").tooltip('show');
		return false;
	}
	else{
		 $("#password").tooltip('hide');
		return true;
	}
}

function validateNewPassword(){
	var e = document.getElementById("newPassword").value;
	var patron = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
	if(e.search(patron)!=0){
		 $("#newPassword").tooltip('show');
		return false;
	}
	else{
		 $("#newPassword").tooltip('hide');
		return true;
	}
}

function validatePasswords(){
	var password = document.getElementById("password").value;
	var confirmPassword = document.getElementById("confirmPassword").value;
	
	if(password == confirmPassword) {
		 $("#confirmPassword").tooltip('hide');
		 return true;
	}
	else {
		 $("#confirmPassword").tooltip('show');
		 return false;
	}
}

function validateNewConfirmPasswords(){
	var password = document.getElementById("password").value;
	var newpassword = document.getElementById("newPassword").value;
	var confirmPassword = document.getElementById("confirmPassword").value;
	
	if(newpassword == confirmPassword && newpassword != password) {
		 $("#confirmPassword").tooltip('hide');
		 return true;
	}
	else {
		 $("#confirmPassword").tooltip('show');
		 return false;
	}
}


function validateForm(){
	var validUser = validateUser();
	var validPassword = validatePassword();
	var validConfirm = validatePasswords();
	var validEmail = validateEmail();
	var res = validUser && validPassword && validConfirm && validEmail;
	return res;
}

function validateChangePassword(){
	var validPassword = validatePassword();
	var validNewPassword = validateNewPassword();
	var validConfirm = validateNewConfirmPasswords();
	var res = validPassword && validNewPassword && validConfirm;
	return res;
}

/*function search(){
	searchDir = document.getElementById("direction").value;
	$.ajax({ 
        type: "POST",
        url: "/dir",
        data: {
        	dir: searchDir
        },
        dataType: "json",
        success:function(datos){
        	if(datos['code'] == "0"){
        		initMap(datos['lat'], datos['lng'])
        	}
			else {
				document.getElementById("map").innerHTML = "<p>Dirección no valida</p>";
			}
		},
		error:function(){
			document.getElementById("error").innerHTML = "<p>Lo sentimos se ha producido un error</p>";
		}
    });
}*/

/*
var map;
function initMap(latitude, longitude) {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: latitude, lng: longitude},
    zoom: 8
  });
}*/
