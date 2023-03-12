from flask_restx import Api

api = Api(
    authorizations={
        "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
    title="Flask Course Project 4",
    description='Movies catalog REST API',
    doc="/docs",
)
