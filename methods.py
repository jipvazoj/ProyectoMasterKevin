#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import re
from models import User
from models import Image
from google.appengine.ext import ndb
import urllib
import json
import hashlib
import uuid
import pdb
import os
from google.appengine.api import mail

def validateUser(request):
    user = re.escape(request.POST.get('user'))
    #email = re.escape(request.POST.get('email'))
    email = request.POST.get('email')
    password = re.escape(request.POST.get('password'))
    confirm = re.escape(request.POST.get('confirmPassword'))
        
    valid_user = re.match(re.compile("^[\w]+$"), user)
    valid_email = re.match(re.compile("^[A-Za-z0-9_\.-]+@[a-z]+(\.[a-z]+)?\.([a-z]{2,3})$"), email)
    #valid_email = re.escape(valid_email)
    valid_password = re.match(re.compile("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"), password)
    valid_confirm = re.match(re.compile("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"), confirm)
    
    error = False
    errors = []
     
    if not valid_user:
        user_error = "Invalid username"
        errors.append(user_error)
        error = True
    if not valid_email:
        email_error = "Invalid email"
        errors.append(email_error)
        error = True
    if not valid_password:
        password_error = "Password length must be >= 8 and it must contain a number, a lowercase and a uppercase letter"
        errors.append(password_error)
        error = True
    if not valid_confirm:
        confirm_error = "Password length must be >= 8 and it must contain a number, a lowercase and a uppercase letter"
        errors.append(confirm_error)
        error = True   
    if password != confirm:
        error = True
        check_error = "Passwords doesn´t match"
        errors.append(check_error)
    if error:
        template_values = {
            'errors': errors
            }
        return template_values
    else:
        return False

def insertUser(request):
    errors = []
    u = User()
    u.user = re.escape(request.POST.get('user'))
    u.email = request.POST.get('email')
    
    password = re.escape(request.POST.get('password'))
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    
    u.password = hashed_password
    u.salt = salt
    u.locked = False
    u.activated = False
    u.attempts = 0
    
    num_users = u.query(User.user==u.user).count()
    num_emails = u.query(User.email==u.email).count()
    if num_users == 0 and num_emails == 0:
        code = hashlib.sha512(u.user + salt).hexdigest()
        u.code = re.escape(code)
        u.put()
        params = { 'user' : u.user, 'code': code}
        sendEmail(u.email, "Account verification url: http://dsswkvn.appspot.com/validateaccount?" + urllib.urlencode(params))
        return True
    else:
        message = "No se ha podido insertar el usuario"
        if (num_users != 0):
            errors.append("User already exists")
        if (num_emails != 0):
            errors.append("Email already exists")
        template_values = {
            'errors': errors
            }
        return template_values

def checkValidEmail(request):
    u = User()
    u.email = re.escape(request.POST.get('email'))
    num_emails = u.query(User.email==u.email).count()
    if (num_emails == 0):
        return True
    else:
        return False

def checkValidUser(request):
    u = User()
    u.user = re.escape(request.POST.get('user'))
    num_users = u.query(User.user==u.user).count()
    if (num_users == 0):
        return True
    else:
        return False

def login(request):
    u = User()
    u.user = re.escape(request.POST.get('user'))
    password = re.escape(request.POST.get('password'))
    
    user = u.query(User.user==u.user).fetch()
    if(len(user)>0):
        salt = user[0].salt
    else:
        return 3
    
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    u.password = hashed_password
    num_users = u.query(ndb.AND(User.user==u.user, User.password == u.password)).count()
    if (num_users > 0):
        user = User()
        user = u.query(User.user==u.user).fetch()
        if (user[0].activated == False):
            return 4
        else:
            if(user[0].locked == False):
                user[0].attempts = 0
                user[0].put()
                return 1
            else:
                return 0
    else:
        num_users = u.query(User.user==u.user).count()
        if (num_users > 0):
            user = User()
            user = u.query(User.user==u.user).fetch()
            attempts = user[0].attempts
            if (attempts < 3):
                attempts = attempts + 1
            if (attempts >= 3):
                user[0].locked = True
            user[0].attempts = attempts
            user[0].put()
            return 2
        else:
            return 3
           
def getUsers():
    users = ndb.gql("SELECT user, email FROM User")
    return users

def getAttempts(request):
    u = User()
    u.user = re.escape(request.POST.get('user'))
    users = u.query(User.user==u.user).fetch()
    return users[0].attempts

def getEmail(user):
    u = User()
    u.user = user
    users = u.query(User.user==u.user).fetch()
    return users[0].email

def getUsersPhotos(user):
    u = User()
    u.user = user
    i = Image()
    photos = i.query(Image.user==u.user).fetch()
    return photos

def getPublicPhotos():
    i = Image()
    photos = i.query(Image.public==True).fetch()
    return photos

def activateAccount(user, code):
    u = User()
    u.user = user
    u.code = code
    users = u.query(ndb.AND(User.user==u.user, User.code == u.code)).fetch()
    if(len(users)>0):
        users[0].activated = True
        users[0].put()
        
def confirmChange(user, code):
    u = User()
    u.user = user
    u.code = code
    users = u.query(ndb.AND(User.user==u.user, User.code == u.code)).fetch()
    if(len(users)>0):
        users[0].password = users[0].new_password
        users[0].new_password = ''
        users[0].put()



def changePassword(request, user): 
    password = re.escape(request.POST.get('password'))
    newpassword = re.escape(request.POST.get('newPassword'))
    confirm = re.escape(request.POST.get('confirmPassword'))
    
    error = False
    errors = []
    
    u = User()
    u.user = user
    u.password = password
    u.new_password = newpassword
    
    
    users = u.query(User.user==u.user).fetch()
    if(len(users)>0):
        salt = users[0].salt
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        hashed_newpassword = hashlib.sha512(newpassword + salt).hexdigest()
        users = u.query(ndb.AND(User.user==u.user, User.password == hashed_password)).fetch()
        if(len(users)>0):
            if(users[0].password != hashed_newpassword):
                users[0].new_password = hashed_newpassword
                users[0].put()
                params = { 'user' : users[0].user, 'code': users[0].code}
                sendEmail(users[0].email, "Change password url: http://dsswkvn.appspot.com/confirmchange?" + urllib.urlencode(params)) 
            else:
                error = True
                password_error = "New password must be different from the last one"
                errors.append(password_error)
        else:
            error = True
            password_error = "Wrong password"
            errors.append(password_error)
    else :
        error = True
        user_error = "Wrong user"
        errors.append(user_error)
    if error:
        template_values = {
            'errors': errors
            }
        return template_values
    else:
        return False

def validateNewPass(request, user):
    password = re.escape(request.POST.get('password'))
    newpassword = re.escape(request.POST.get('newPassword'))
    confirm = re.escape(request.POST.get('confirmPassword'))
    
    valid_password = re.match(re.compile("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"), password)
    valid_newpassword = re.match(re.compile("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"), newpassword)
    valid_confirm = re.match(re.compile("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"), confirm)
    
    error = False
    errors = []
     
    if not valid_password:
        password_error = "Password length must be >= 8 and it must contain a number, a lowercase and a uppercase letter"
        errors.append(password_error)
        error = True
    if not valid_newpassword:
        password_error = "New password length must be >= 8 and it must contain a number, a lowercase and a uppercase letter"
        errors.append(password_error)
        error = True
    if not valid_confirm:
        confirm_error = "Password length must be >= 8 and it must contain a number, a lowercase and a uppercase letter"
        errors.append(confirm_error)
        error = True   
    if newpassword != confirm:
        error = True
        check_error = "Passwords doesn´t match"
        errors.append(check_error)
    if error:
        template_values = {
            'errors': errors
            }
        return template_values
    else:
        return False

def validateImage(blob_info):
    size = blob_info.size/1024
    name = blob_info.filename
    filename, file_extension = os.path.splitext(name)
    if((file_extension != ".jpg") and (file_extension != ".png") and (file_extension != ".gif")):
        return False
    else:
        if (size > 1000):
            return False
        else:
            return True

def sendEmail(to, msg):
    message = mail.EmailMessage(sender="dsswkvn@appspot.gserviceaccount.com",
                            subject="DSSWKVN")
    message.to = to
    message.body = msg
    message.send()