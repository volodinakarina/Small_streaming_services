from flask_restx import fields, Model

from project.setup.api import api

movie_model: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Название фильма'),
    'description': fields.String(max_length=5000, example='Описание фильма'),
    'trailer': fields.String(max_length=200, example='Комедия'),
    'year': fields.Integer(example=2022),
    'rating': fields.Float(example=4.8),
    'genre_id': fields.Integer(example=1),
    'director_id': fields.Integer(example=2),
    'genre': fields.Nested({'id': fields.Integer, 'name': fields.String}),
    'director': fields.Nested({'id': fields.Integer, 'name': fields.String})
})

director_model: Model = api.model('Режиссёр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Квентин Тарантино'),
})

genre_model: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

user_model: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=200, example='user@email.me'),
    'password': fields.String(required=True, max_length=200),
    'name': fields.String(max_length=100),
    'surname': fields.String(max_length=200),
    'favourite_genre': fields.Integer(example=1)
})