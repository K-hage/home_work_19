from flask import request
from flask_restx import Resource, Namespace

from app.container import auth_service

auth_ns = Namespace('auth')  # создаем namespace аутентификации


@auth_ns.route('/')
class AuthView(Resource):
    """
    CBV аутентификации
    POST - получение токенов пользователя
    PUT - обновление токенов пользователя
    """

    def post(self):
        new_user_json = request.json

        username = new_user_json.get('username', None)
        password = new_user_json.get('password', None)

        if None in [username, password]:
            return '', 400

        tokens = auth_service.generate_tokens(username, password)

        return tokens

    def put(self):
        data = request.json
        token = data.get('refresh_token')

        tokens = auth_service.approve_refresh_token(token)
        return tokens
