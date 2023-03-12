import calendar
import datetime
import jwt

from flask import current_app, abort
from project.services.user_service import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, email, password, is_refresh=False):
        user = self.user_service.get_by_email(email)

        if user is None:
            abort(404)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):  # user_password - hash from the db
                abort(400)

        data = {
            "email": user.email
        }

        delta_min = datetime.datetime.now() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
        delta_max = datetime.datetime.now() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])

        data['exp'] = calendar.timegm(delta_min.timetuple())
        access_token = jwt.encode(data, current_app.config['SECRET_KEY'], algorithm='HS256')

        data['exp'] = calendar.timegm(delta_max.timetuple())
        refresh_token = jwt.encode(data, current_app.config['SECRET_KEY'], algorithm='HS256')

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms='HS256')
        email = data.get('email')

        return self.generate_tokens(email, None, is_refresh=True)