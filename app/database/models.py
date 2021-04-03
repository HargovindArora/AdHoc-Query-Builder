from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
from mongoengine.queryset import DoesNotExist
from datetime import datetime

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    sql = db.ListField(db.StringField())

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)


class TokenBlocklist(db.Document):
    jti = db.StringField()
    date_created = db.DateTimeField(default=datetime.utcnow)

    @classmethod
    def is_jti_blacklisted(cls, jti):
        try:
            token = cls.objects(jti=jti).get()
        except DoesNotExist:
            return None
        return bool(token)
