from sqlalchemy.exc import IntegrityError

from app.dao.model.user import User


class UsersDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, user_id):
        """
        Возвращает данные режиссера по id или ошибку 404
        """

        return self.session.query(User). \
            filter(User.id == user_id). \
            first_or_404(description='User not found')

    def get_all(self):
        """
        Возвращает данные всех фильмов
        """

        return self.session.query(User).all()

    def check_id(self, user_id):
        """
        Проверка есть ли данные по id
        """

        if self.session.query(User).get(user_id):
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

        user = User(**data)
        self.session.add(user)
        self.get_commit()
        return user

    def update(self, user):
        """
        Обновление данных режиссера
        """

        self.session.add(user)
        self.get_commit()
        return user

    def delete(self, user_id):
        """
        Удаление данных режиссера по id
        """

        user = self.get_one(user_id)

        self.session.delete(user)
        self.session.commit()

    def get_by_username(self, name):
        """
        Поиск по имени пользователя
        """

        return self.session.query(User). \
            filter(User.username == name). \
            first_or_404(description='Not Found')
