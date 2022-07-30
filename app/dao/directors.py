from sqlalchemy.exc import IntegrityError

from app.dao.model.director import Director


class DirectorsDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, director_id):
        """
        Возвращает данные режиссера по id или ошибку 404
        """
        return self.session.query(Director). \
            filter(Director.id == director_id). \
            first_or_404(description='Director not found')

    def get_all(self):
        """
        Возвращает данные всех фильмов
        """
        return self.session.query(Director).all()

    def check_id(self, director_id):
        """
        Проверка есть ли данные по id
        """

        if self.session.query(Director).get(director_id):
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

        director = Director(**data)
        self.session.add(director)
        self.get_commit()
        return director

    def update(self, director):
        """ Обновление данных режиссера"""
        self.session.add(director)
        self.get_commit()
        return director

    def delete(self, director_id):
        """
        Удаление данных режиссера по id
        """
        director = self.get_one(director_id)

        self.session.delete(director)
        self.session.commit()
