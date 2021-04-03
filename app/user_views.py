from flask import request, Response
from app.database.models import User, TokenBlocklist
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

import datetime


class SignupApi(Resource):

    def post(self):
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        user.save()
        id = user.id

        return {'id': str(id)}, 200


class LoginApi(Resource):

    def post(self):
        body = request.get_json()
        user = User.objects.get(username=body.get('username'))
        authorized = user.check_password_hash(body.get('password'))

        if not authorized:
            return {'message': 'Username or password is invalid'}, 401

        expires = datetime.timedelta(hours=7)
        access_token = create_access_token(
            identity=str(user.id), expires_delta=expires)

        return {'token': access_token}, 200


class LogoutApi(Resource):

    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        revoked_token = TokenBlocklist(jti=jti)
        revoked_token.save()

        return {"message": "Logged Out!"}, 200
