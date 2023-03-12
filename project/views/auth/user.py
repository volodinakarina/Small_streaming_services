from flask import request
from flask_restx import Resource, Namespace

from project.helpers.helpers import get_user_email_from_token
from project.helpers.decorators import auth_required
from project.setup.api.models import user_model
from project.container import user_service

api = Namespace('user')


@api.route('/')
class UserView(Resource):

    @auth_required
    @api.marshal_with(user_model, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get user's information (profile)
        """
        user_email = get_user_email_from_token()
        return user_service.get_by_email(user_email)

    @auth_required
    def patch(self):
        """
        Change user data (name, surname, favorite genre).
        """
        req_json = request.json
        req_json['email'] = get_user_email_from_token()
        user_service.patch(req_json)
        return '', 204


@api.route('/password/')
class PasswordView(Resource):

    @auth_required
    def put(self):
        """
        Update user password
        """
        req_json = request.json
        req_json['email'] = get_user_email_from_token()
        user_service.update(req_json)
        return '', 204