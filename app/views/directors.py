from flask import request, jsonify
from flask_restx import Resource, Namespace

from app.container import directors_service
from app.dao.schema.director import DirectorSchema
from app.helpers.decorators import auth_required, admin_required

director_ns = Namespace('directors')  # создаем namespace режиссеров

director_schema = DirectorSchema()  # схема для сериализации одного режиссера в словарь
directors_schema = DirectorSchema(many=True)  # схема для сериализации нескольких режиссеров в список словарей


@director_ns.route('/')
class DirectorsView(Resource):
    """
    CBV режиссеров
    GET - получение данных всех режиссеров
    POST - добавление данных нового режиссера
    """

    @auth_required
    def get(self):
        directors = directors_service.get_all()
        return directors_schema.dump(directors), 200

    @admin_required
    def post(self):
        new_director_json = request.json
        try:
            new_director = directors_service.create(new_director_json)
        except TypeError as e:
            return str(e), 400
        response = jsonify(director_schema.dump(new_director))
        response.status_code = 201
        response.headers['location'] = new_director.id
        return response


@director_ns.route('/<int:director_id>/')
class DirectorView(Resource):
    """
    CBV режиссера
    GET - получение данных режиссера по id
    PUT - обновление данных режиссера по id
    PATCH - частичное обновление данных по id
    DELETE - удаление режиссера по id
    """

    @auth_required
    def get(self, director_id):
        director = directors_service.get_one(director_id)
        return director_schema.dump(director), 200

    @admin_required
    def put(self, director_id):
        update_json = request.json

        try:
            directors_service.check_is_dict(update_json)
            if not update_json.get('id'):
                update_json['id'] = director_id
            director = directors_service.update(director_id, update_json)
        except TypeError as e:
            return str(e), 400

        return director_schema.dump(director), 201

    @admin_required
    def patch(self, director_id):
        update_json = request.json

        try:
            directors_service.check_is_dict(update_json)
            if not update_json.get('id'):
                update_json['id'] = director_id
            director = directors_service.update_partial(director_id, update_json)
        except TypeError as e:
            return str(e), 400

        return director_schema.dump(director), 201

    @admin_required
    def delete(self, director_id):
        directors_service.delete(director_id)
        return '', 204
