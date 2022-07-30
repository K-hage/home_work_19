from flask import request, jsonify
from flask_restx import Resource, Namespace, fields

from app.container import movies_service
from app.dao.schema.movie import MovieSchema
from app.helpers.decorators import auth_required, admin_required

movie_ns = Namespace('movies')  # создаем namespace фильмов

movie_schema = MovieSchema()  # схема для сериализации одного фильма в словарь
movies_schema = MovieSchema(many=True)  # схема для сериализации нескольких фильмов в список словарей


@movie_ns.route('/')
class MoviesView(Resource):
    """
    CBV фильмов
    GET - получение данных всех фильмов,
    фильмов по жанрам, режиссерам или году выпуска
    POST - добавление данных нового фильма
    """

    @auth_required
    # создаем документацию и параметры для GET
    @movie_ns.doc(
        description='Оставьте поля пустыми для вывода всех данных\n'
                    'при заполнения id режиссера выведутся данные фильмов по id режиссера\n'
                    'при заполнения id жанра выведутся данные фильмов по id жанра\n'
                    'при заполнения года выпуска выведутся данные фильмов по году выпуска\n',
        params={
            'director_id': 'id режиссера',
            'genre_id': 'id жанра',
            'year': 'год выпуска'
        }
    )
    def get(self):

        req_args = request.args
        if len(req_args) > 1:  # Если параметров больше одного выдаст сообщение об этом
            return "Заполните только одно поле"

        if req_args:
            movies = movies_service.get_find(req_args)  # Поиск по параметрам

        else:
            movies = movies_service.get_all()
        if not movies:
            return "NotFound", 404
        return movies_schema.dump(movies), 200

    @admin_required
    def post(self):

        new_movie_json = request.json
        try:
            new_movie = movies_service.create(new_movie_json)
        except TypeError as e:
            return str(e), 400
        response = jsonify(movie_schema.dump(new_movie))
        response.status_code = 201
        response.headers['location'] = new_movie.id  # добавляем location в заголовок
        return response


@movie_ns.route('/<int:movie_id>/')
class MovieView(Resource):
    """
    CBV фильма
    GET - получение данных фильма по id
    PUT - обновление данных фильма по id
    PATCH - частичное обновление данных по id
    DELETE - удаление фильма по id
    """

    @auth_required
    def get(self, movie_id):
        movie = movies_service.get_one(movie_id)
        return movie_schema.dump(movie), 200

    @admin_required
    def put(self, movie_id):
        update_json = request.json

        try:
            movies_service.check_is_dict(update_json)
            if not update_json.get('id'):
                update_json['id'] = movie_id
            movie = movies_service.update(movie_id, update_json)
        except TypeError as e:
            return str(e), 400

        return movie_schema.dump(movie), 201

    @admin_required
    def patch(self, movie_id):
        update_json = request.json

        try:
            movies_service.check_is_dict(update_json)
            if not update_json.get('id'):
                update_json['id'] = movie_id
            movie = movies_service.update_partial(movie_id, update_json)
        except TypeError as e:
            return str(e), 400

        return movie_schema.dump(movie), 201

    @admin_required
    def delete(self, movie_id):
        movies_service.delete(movie_id)
        return '', 204
