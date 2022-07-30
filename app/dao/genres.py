from sqlalchemy.exc import IntegrityError

from app.dao.model.genre import Genre


class GenresDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, genre_id):
        """
        Возвращает данные режиссера по id или ошибку 404
        """
        return self.session.query(Genre).\
            filter(Genre.id == genre_id).\
            first_or_404(description='Genre not found')

    def get_all(self):
        """
        Возвращает данные всех фильмов
        """
        return self.session.query(Genre).all()

    def check_id(self, genre_id):
        """
        Проверка есть ли данные по id
        """
        if self.session.query(Genre).get(genre_id):
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

        genre = Genre(**data)
        self.session.add(genre)
        self.get_commit()
        return genre

    def update(self, genre):
        """
        Обновление данных режиссера
        """
        self.session.add(genre)
        self.get_commit()
        return genre

    def delete(self, genre_id):
        """
        Удаление данных режиссера по id
        """
        genre = self.get_one(genre_id)

        self.session.delete(genre)
        self.session.commit()
