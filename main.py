#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import os 
from google.appengine.ext.webapp import template
import jinja2
import methods
from webapp2_extras import sessions
import session_module
from google.appengine.ext import blobstore
import models
from google.appengine.ext.webapp import blobstore_handlers
import pdb
import re
from datetime import datetime
import time
import urllib

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), extensions=['jinja2.ext.autoescape'], autoescape=True)
max_expire_age = 180

class Index(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template("/templates/index.html")
        self.response.write(template.render(template_values))

class SignIn(webapp2.RequestHandler):
    def post(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template("/templates/signIn.html")
        self.response.write(template.render(template_values))

class SignUp(webapp2.RequestHandler):
    def post(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template("/templates/signUp.html")
        self.response.write(template.render(template_values))

class NewUser(webapp2.RequestHandler):
    def post(self):
        template_values = methods.validateUser(self.request)
        if not template_values:
            template_values = methods.insertUser(self.request)
            if template_values == True:
                template_values = {
                    'user': re.escape(self.request.POST.get('user'))
                }
                template = JINJA_ENVIRONMENT.get_template("/templates/modal.html")
                self.response.write(template.render(template_values))
            else:
                template_values['title'] = "An error ocurred"
                template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
                self.response.write(template.render(template_values))
        else:
            template_values['title'] = "An error ocurred"
            template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
            self.response.write(template.render(template_values))

class CheckUser(webapp2.RequestHandler):
    def post(self):
        validUser = methods.checkValidUser(self.request)
        if  validUser:
            self.response.write("ValidUser")
        else:
            self.response.write("NotValidUser")

class CheckEmail(webapp2.RequestHandler):
    def post(self):
        validEmail = methods.checkValidEmail(self.request)
        if validEmail:
            self.response.write("ValidEmail")
        else:
            self.response.write("NotValidEmail")

class Login(session_module.BaseSessionHandler):
    def post(self):
        login = methods.login(self.request)
        if (login == 1):
            user = re.escape(self.request.POST.get('user'))
            self.session['user'] = user
            now = datetime.now()
            self.session['last_activity'] = time.mktime(now.timetuple())
            self.response.write("correctLogin")
        else:
            if(login == 2):
                attempts = methods.getAttempts(self.request)
                attempts = 3 - attempts
                template_values = {
                                   'title': "Invalid credentials",
                                   'errors': ["Invalid user or password", "Remaining attempts: " + str(attempts)]
                                   }
            if(login == 0):
                template_values = {
                                   'title': "Locked account",
                                   'errors': ["This account has been locked, please contact the administrator of the site"]
                                   }
            if(login == 3):
                template_values = {
                                   'title': "Invalid credentials",
                                   'errors': ["Invalid user or password"]
                                   }
            if(login == 4):
                template_values = {
                                   'title': "Unactivated account",
                                   'errors': ["Please check your email and activate your account"]
                                   }
            template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
            self.response.write(template.render(template_values))

class ValidateAccount(webapp2.RequestHandler):
    def get(self, url):
        user = re.escape(self.request.get('user'))
        code = re.escape(self.request.get('code'))
        methods.activateAccount(user, code)
        self.redirect('/')

class Logout(session_module.BaseSessionHandler):
    def get(self):
        if self.session.get('user'):
            del self.session['user']
            if self.session.get('last_activity'): del self.session['last_activity']
            self.redirect('/')
        else :
            self.redirect('/')

class MainHandler(session_module.BaseSessionHandler):
    def get(self):
        now = datetime.now()
        seconds = time.mktime(now.timetuple())
        if (self.session.get('user') and self.session.get('last_activity') and (seconds - self.session.get('last_activity'))  <= max_expire_age):
            self.session['last_activity'] = seconds
            users = methods.getUsers()
            template_values = {
                'users': users
            }
            template = JINJA_ENVIRONMENT.get_template("/templates/main.html")
            self.response.write(template.render(template_values))
        else :
            self.redirect('/')

class UploadPhoto(session_module.BaseSessionHandler):
    def post(self):
        if (self.session.get('user')):
            now = datetime.now()
            seconds = time.mktime(now.timetuple())
            if(self.session.get('last_activity') and (seconds - self.session.get('last_activity'))  <= max_expire_age):
                self.session['last_activity'] = seconds
                upload_url = blobstore.create_upload_url('/upload')
                template_values = {'upload_url': upload_url }
                template = JINJA_ENVIRONMENT.get_template("/templates/uploadPhoto.html")
                self.response.write(template.render(template_values))
            else :
                template_values = {
                    'title': "Session expired",
                    'errors': ["Your session has been expired, you will be redirected to login page"]
                }
                template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
                self.response.write(template.render(template_values))
        else :
            template_values = {
                    'title': "Unauthorized access",
                    'errors': ["Unauthorized access, you will be redirected to login page"],
                    'sessionError': "Session expired"
                }
            template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
            self.response.write(template.render(template_values))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler, session_module.BaseSessionHandler):
    def post(self):
        if self.session.get('user'):
            now = datetime.now()
            seconds = time.mktime(now.timetuple())
            if(self.session.get('last_activity') and (seconds - self.session.get('last_activity'))  <= max_expire_age):
                self.session['last_activity'] = seconds
                upload_files = self.get_uploads('file-es[]')
                n = 0
                while n < len(upload_files):           
                    blob_info = upload_files[n]
                    validImage = methods.validateImage(blob_info)
                    if (n <= 10 and validImage):
                        img = models.Image(user=self.session.get('user'), public=self.request.POST.get("optradio")=="public", blob_key=blob_info.key())
                        img.put()
                    n = n+1
                self.redirect('/main')
            else :
                template_values = {
                    'title': "Session expired",
                    'errors': ["Your session has been expired, you will be redirected to login page"]
                }
                template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
                self.response.write(template.render(template_values))
        else :
            template_values = {
                    'title': "Unauthorized access",
                    'errors': ["Unauthorized access, you will be redirected to login page"],
                    'sessionError': "Session expired"
                }
            template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
            self.response.write(template.render(template_values))

class ViewPublicPhotos(webapp2.RequestHandler):
    def post(self):
        p = methods.getPublicPhotos()
        photos = []
        for photo in p:
            photos.append(photo.blob_key)
        template_values = {'photos': photos,
                           'lastIndex': len(photos)}
        template = JINJA_ENVIRONMENT.get_template("/templates/viewPhotos.html")
        self.response.write(template.render(template_values))

class ViewPhotos(session_module.BaseSessionHandler):
    def post(self):
        if (self.session.get('user')):
            now = datetime.now()
            seconds = time.mktime(now.timetuple())
            if(self.session.get('last_activity') and (seconds - self.session.get('last_activity'))  <= max_expire_age):
                self.session['last_activity'] = seconds
                p = methods.getUsersPhotos(self.session.get('user'))
                photos = []
                for photo in p:
                    photos.append(photo.blob_key)
                template_values = {'photos': photos,
                                    'user':  self.session.get('user'),
                                    'lastIndex': len(photos)}
                template = JINJA_ENVIRONMENT.get_template("/templates/viewPhotos.html")
                self.response.write(template.render(template_values))
            else :
                template_values = {
                    'title': "Session expired",
                    'errors': ["Your session has been expired, you will be redirected to login page"]
                }
                template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
                self.response.write(template.render(template_values))
        else:
            template_values = {
                'title': "Unauthorized access",
                'errors': ["Unauthorized access, you will be redirected to login page"],
                'sessionError': "Session expired"
            }
            template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
            self.response.write(template.render(template_values))

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
      def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

class MyProfile(session_module.BaseSessionHandler):
    def post(self):
        if self.session.get('user'):
            now = datetime.now()
            seconds = time.mktime(now.timetuple())
            if(self.session.get('last_activity') and (seconds - self.session.get('last_activity'))  <= max_expire_age):
                self.session['last_activity'] = seconds
                template_values = {
                    'user': self.session.get('user'),
                    'email': methods.getEmail(self.session.get('user'))
                }
                template = JINJA_ENVIRONMENT.get_template("/templates/myprofile.html")
                self.response.write(template.render(template_values))
            else :
                template_values = {
                    'title': "Session expired",
                    'errors': ["Your session has been expired, you will be redirected to login page"]
                }
                template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
                self.response.write(template.render(template_values))
        else :
            template_values = {
                    'title': "Unauthorized access",
                    'errors': ["Unauthorized access, you will be redirected to login page"],
                    'sessionError': "Session expired"
                }
            template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
            self.response.write(template.render(template_values))

class ChangePassword(session_module.BaseSessionHandler):
    def post(self):
        if self.session.get('user'):
            now = datetime.now()
            seconds = time.mktime(now.timetuple())
            if(self.session.get('last_activity') and (seconds - self.session.get('last_activity'))  <= max_expire_age):
                self.session['last_activity'] = seconds
                template_values = methods.validateNewPass(self.request, self.session.get('user'))
                if not template_values:
                        template_values = methods.changePassword(self.request, self.session.get('user'))
                        if not template_values:
                            template_values = {}
                            template = JINJA_ENVIRONMENT.get_template("/templates/changePasswordModal.html")
                            self.response.write(template.render(template_values))
                        else:
                            template_values['title'] = "An error ocurred"
                            template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
                            self.response.write(template.render(template_values))
                else:
                    template_values['title'] = "An error ocurred"
                    template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
                    self.response.write(template.render(template_values))
            else :
                template_values = {
                    'title': "Session expired",
                    'errors': ["Your session has been expired, you will be redirected to login page"]
                }
                template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
                self.response.write(template.render(template_values))
        else :
            template_values = {
                    'title': "Unauthorized access",
                    'errors': ["Unauthorized access, you will be redirected to login page"],
                    'sessionError': "Session expired"
                }
            template = JINJA_ENVIRONMENT.get_template("/templates/alert.html")
            self.response.write(template.render(template_values))

class ConfirmChange(webapp2.RequestHandler):
    def get(self, url):
        user = re.escape(self.request.get('user'))
        code = re.escape(self.request.get('code'))
        methods.confirmChange(user, code)
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/checkUser', CheckUser),
    ('/checkEmail', CheckEmail),
    ('/main', MainHandler),
    ('/login', Login),
    ('/logout', Logout),
    ('/', Index),
    ('/signin', SignIn),
    ('/signup', SignUp),
    ('/uploadphoto', UploadPhoto),
    ('/upload', UploadHandler),
    ('/newUser', NewUser),
    ('/viewphotos', ViewPhotos),
    ('/myprofile', MyProfile),
    ('/viewpublicphotos', ViewPublicPhotos),
    ('/validateaccount([.]+)?', ValidateAccount),
    ('/confirmchange([.]+)?', ConfirmChange),
    ('/changepassword', ChangePassword),
    ('/serve/([^/]+)?', ServeHandler)
    ], 
    config=session_module.myconfig_dict,
    debug=True)