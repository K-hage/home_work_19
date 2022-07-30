from flask import request, jsonify
from flask_restx import Resource, Namespace

from app.container import genres_service
from app.dao.schema.genre import GenreSchema
from app.helpers.decorators import auth_required, admin_required

genre_ns = Namespace('genres')  # создаем namespace жанров

genre_schema = GenreSchema()  # схема для сериализации одного жанра в словарь
genres_schema = GenreSchema(many=True)  # схема для сериализации нескольких жанров в список словарей


@genre_ns.route('/')
class GenresView(Resource):
    """
    CBV жанров
    GET - получение данных всех жанров
    POST - добавление данных нового жанра
    """

    @auth_required
    def get(self):
        genres = genres_service.get_all()
        return genres_schema.dump(genres), 200

    @admin_required
    def post(self):
        new_genre_json = request.json
        try:
            new_genre = genres_service.create(new_genre_json)
        except TypeError as e:
            return str(e), 400
        response = jsonify(genre_schema.dump(new_genre))
        response.status_code = 201
        response.headers['location'] = new_genre.id
        return genre_schema.dump(new_genre), 201


@genre_ns.route('/<int:genre_id>/')
class GenreView(Resource):
    """
    CBV жанра
    GET - получение данных жанра по id
    PUT - обновление данных жанра по id
    PATCH - частичное обновление данных по id
    DELETE - удаление жанра по id
    """

    @auth_required
    def get(self, genre_id):
        genre = genres_service.get_one(genre_id)
        return genre_schema.dump(genre), 200

    @admin_required
    def put(self, genre_id):

        update_json = request.json

        try:
            genres_service.check_is_dict(update_json)
            if not update_json.get('id'):
                update_json['id'] = genre_id
            genre = genres_service.update(genre_id, update_json)
        except TypeError as e:
            return str(e), 400
        return genre_schema.dump(genre), 201

    @admin_required
    def patch(self, genre_id):

        update_json = request.json

        try:
            genres_service.check_is_dict(update_json)
            if not update_json.get('id'):
                update_json['id'] = genre_id
            genre = genres_service.update_partial(genre_id, update_json)
        except TypeError as e:
            return str(e), 400
        return genre_schema.dump(genre), 201

    @admin_required
    def delete(self, genre_id):
        genres_service.delete(genre_id)
        return '', 204
