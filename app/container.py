from app.dao.directors import DirectorsDAO
from app.dao.genres import GenresDAO
from app.dao.movies import MoviesDAO
from app.dao.users import UsersDAO
from app.service.auth import AuthService
from app.service.directors import DirectorsService
from app.service.genres import GenresService
from app.service.movies import MoviesService
from app.service.users import UsersService
from app.setup_db import db

movies_dao = MoviesDAO(db.session)  # создаем экземпляр DAO фильмов
movies_service = MoviesService(movies_dao)  # создаем экземпляр сервиса фильмов

genres_dao = GenresDAO(db.session)  # создаем экземпляр DAO жанров
genres_service = GenresService(genres_dao)  # создаем экземпляр сервиса жанров

directors_dao = DirectorsDAO(db.session)  # создаем экземпляр DAO режиссеров
directors_service = DirectorsService(directors_dao)  # создаем экземпляр сервиса режиссеров

users_dao = UsersDAO(db.session)  # создаем экземпляр DAO пользователя
users_service = UsersService(users_dao)  # создаем экземпляр сервиса пользователя

auth_service = AuthService(users_service)  # создаем экземпляр сервиса авторизации
