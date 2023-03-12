import jwt
from flask import request, abort, current_app


def get_user_email_from_token():
    if 'Authorization' not in request.headers:
        abort(401)

    data = request.headers['Authorization']
    token = data.split('Bearer ')[-1]

    if not token:
        return {'message': 'Token is missing!'}, 401

    user = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    email = user.get('email')

    if not email:
        return {'message': 'Token is wrong!'}, 401

    return email