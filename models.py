from google.appengine.ext import ndb

class User(ndb.Model):
    user = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    salt = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    locked = ndb.BooleanProperty()
    attempts = ndb.IntegerProperty()
    code = ndb.StringProperty()
    activated = ndb.BooleanProperty()
    new_password = ndb.StringProperty()

class Image(ndb.Model):
    user = ndb.StringProperty()
    public = ndb.BooleanProperty()
    blob_key = ndb.BlobKeyProperty()