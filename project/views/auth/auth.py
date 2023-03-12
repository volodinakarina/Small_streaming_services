from flask import request, abort
from flask_restx import Resource, Namespace

from project.container import auth_service, user_service

api = Namespace('auth')


@api.route('/login/')
class AuthsView(Resource):
    def post(self):
        data = request.json

        email = data.get('email', None)
        password = data.get('password', None)

        if None in [email, password]:
            abort(400)

        tokens = auth_service.generate_tokens(email, password)

        return tokens, 201

    def put(self):
        data = request.json

        token = data.get('refresh_token', None)

        if not token:
            abort(400)

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201


@api.route('/register/')
class RegisterView(Resource):
    def post(self):
        data = request.json

        email = data.get('email', None)
        password = data.get('password', None)

        if None in [email, password]:
            abort(400)

        user_data = {
            'email': email,
            'password': password
        }

        new_user = user_service.create(user_data)

        if not new_user:
            return f'Error! {email} already exists!', 409

        return '', 201