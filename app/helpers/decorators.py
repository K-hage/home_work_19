import jwt

from flask import request, abort

from app.helpers.constants import JWT_SECRET, JWT_ALGORITHM, admin


def auth_required(func):
    """ Аутентификация пользователей """

    def wrapper(*args, **kwargs):

        # проверка на присутствие авторизации в заголовке
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]

        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    """ Аутентификация администраторов """

    def wrapper(*args, **kwargs):

        # проверка на присутствие авторизации в заголовке
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        role = None

        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            role = user.get('role', 'user')
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        # Проверка роли авторизованного пользователя
        if role not in admin:
            abort(403)
        return func(*args, **kwargs)

    return wrapper
