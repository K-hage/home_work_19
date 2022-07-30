from sqlalchemy.exc import IntegrityError

from app.dao.model.movie import Movie


class MoviesDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, movie_id):
        """
        Возвращает данные режиссера по id или ошибку 404
        """
        return self.session.query(Movie). \
            filter(Movie.id == movie_id). \
            first_or_404(description='Movie not found')

    def get_by_directors(self, director_id: int):
        """
        Возвращает данные фильмов по id режиссера
        """
        return self.session.query(Movie). \
            filter(Movie.director_id == director_id). \
            all()

    def get_by_genres(self, genre_id: int):
        """
        Возвращает данные фильмов по id жанра
        """
        return self.session.query(Movie). \
            filter(Movie.genre_id == genre_id). \
            all()

    def get_by_years(self, year: int):
        """
        Возвращает данные фильмов по году выпуска
        """
        return self.session.query(Movie). \
            filter(Movie.year == year). \
            all()

    def get_all(self):
        """
        Возвращает данные всех фильмов
        """
        return self.session.query(Movie).all()

    def check_id(self, movie_id):
        """
        Проверка есть ли данные по id
        """
        if self.session.query(Movie).get(movie_id):
            raise TypeError('id занят')

    def get_commit(self):
        """
        сommit через проверку соответствия полученных данных
        """
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise TypeError('Данные не соответствуют или уже существуют')

    def check_is_dict(self, data):
        """
        Проверка на то что данные являются словарем
        """
        if not isinstance(data, dict):
            raise TypeError('Не верный формат данных')

    def create(self, data):
        """
        Создание данных нового режиссера
        """
        self.check_is_dict(data)
        self.check_id(data.get('id', None))

        movie = Movie(**data)
        self.session.add(movie)
        self.get_commit()
        return movie

    def update(self, movie):
        """
        Обновление данных режиссера
        """
        self.session.add(movie)
        self.get_commit()
        return movie

    def delete(self, movie_id):
        """
        Удаление данных режиссера по id
        """
        movie = self.get_one(movie_id)

        self.session.delete(movie)
        self.session.commit()
