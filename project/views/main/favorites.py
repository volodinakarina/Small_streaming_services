from flask_restx import Namespace, Resource

from project.helpers.helpers import get_user_email_from_token
from project.container import user_service
from project.helpers.decorators import auth_required
from project.setup.api.models import movie_model

api = Namespace('favorites')


@api.route('/movies/')
class FavoritesView(Resource):

    @auth_required
    @api.marshal_with(movie_model, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get favorites movies.
        """
        email = get_user_email_from_token()
        movies = user_service.get_favorites(email)
        return movies


@api.route('/movies/<int:mid>', doc={'params': {'mid': 'Movie ID'}})
class FavoriteView(Resource):

    @auth_required
    def post(self, mid):
        """
        Add movie to favorites
        """
        email = get_user_email_from_token()
        user_service.add_favorire(email, mid)
        return '', 204

    @auth_required
    def delete(self, mid):
        """
        Delete movie from favorites
        """
        email = get_user_email_from_token()
        user_service.delete_favorite(email, mid)
        return '', 204