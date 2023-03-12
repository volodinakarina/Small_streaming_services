from flask_restx import Namespace, Resource

from project.container import director_service
from project.setup.api.models import director_model
from project.setup.api.parsers import page_parser

api = Namespace('directors')


@api.route('/')
class DirectorsView(Resource):
    @api.expect(page_parser)
    @api.marshal_with(director_model, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all directors.
        """
        return director_service.get_all(**page_parser.parse_args())


@api.route('/<int:director_id>/', doc={'params': {'director_id': 'Director ID'}})
class DirectorView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(director_model, code=200, description='OK')
    def get(self, director_id: int):
        """
        Get director by id.
        """
        return director_service.get_item(director_id)