import jwt
from flask import request, current_app, abort


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception:
            abort(401)

        return func(*args, **kwargs)

    return wrapper