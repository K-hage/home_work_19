from flask import request, jsonify
from flask_restx import Resource, Namespace

from app.container import users_service
from app.dao.schema.user import UserSchema

user_ns = Namespace('users')  # создаем namespace пользователя

user_schema = UserSchema()  # схема для сериализации одного пользователя в словарь
users_schema = UserSchema(many=True)  # схема для сериализации нескольких пользователей в список словарей


@user_ns.route('/')
class UsersView(Resource):
    """
    CBV пользователя
    GET - получение данных всех пользователей
    POST - добавление данных нового пользователя
    """

    def get(self):
        users = users_service.get_all()
        return users_schema.dump(users), 200

    def post(self):
        new_user_json = request.json
        try:
            new_user = users_service.create(new_user_json)
        except TypeError as e:
            return str(e), 400
        response = jsonify(user_schema.dump(new_user))
        response.status_code = 201
        response.headers['location'] = new_user.id
        return response


@user_ns.route('/<int:user_id>/')
class UserView(Resource):
    """
    CBV пользователя
    GET - получение данных пользователя по id
    PUT - обновление данных пользователя по id
    PATCH - частичное обновление данных по id
    DELETE - удаление пользователя по id
    """

    def get(self, user_id):
        user = users_service.get_one(user_id)
        return user_schema.dump(user), 200

    def put(self, user_id):
        update_json = request.json

        try:
            users_service.check_is_dict(update_json)
            if not update_json.get('id'):
                update_json['id'] = user_id
            user = users_service.update(user_id, update_json)
        except TypeError as e:
            return str(e), 400

        return user_schema.dump(user), 201

    def patch(self, user_id):
        update_json = request.json

        try:
            users_service.check_is_dict(update_json)
            if not update_json.get('id'):
                update_json['id'] = user_id
            user = users_service.update_partial(user_id, update_json)
        except TypeError as e:
            return str(e), 400

        return user_schema.dump(user), 201

    def delete(self, user_id):
        users_service.delete(user_id)
        return '', 204
