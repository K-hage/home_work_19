import base64
import hashlib
import hmac

from app.helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UsersService:
    def __init__(self, dao):
        self.dao = dao

    def get_one(self, user_id):
        """
        Возвращает данные пользователя по id
        """
        return self.dao.get_one(user_id)

    def get_all(self):
        """
        Возвращает данные всех пользователей
        """
        return self.dao.get_all()

    def check_is_dict(self, data):
        """
        Проверка: являются ли данные словарем
        """
        return self.dao.check_is_dict(data)

    def create(self, data):
        """
        Создание данных нового пользователя
        """
        data['password'] = self.get_hash(data['password'])
        return self.dao.create(data)

    def update(self, user_id, data):
        """
        Обновление данных пользователя по id
        """
        user = self.dao.get_one(user_id)

        user.id = data.get('id')
        user.username = data.get('name')
        user.password = self.get_hash(data.get('password'))
        user.role = data.get('role')

        return self.dao.update(user)

    def update_partial(self, user_id, data):
        """
        Частичное обновление данных пользователя по id
        """
        user = self.dao.get_one(user_id)

        if 'id' in data:
            user.id = data.get('id')
        if 'username' in data:
            user.name = data.get('username')
        if 'password' in data:
            user.password = self.get_hash(data.get('password'))
        if 'role' in data:
            user.role = data.get('role')

        return self.dao.update(user)

    def delete(self, user_id):
        """
        Удаление данных пользователя
        """
        self.dao.delete(user_id)

    def get_hash(self, password):
        """
        Метод хэширования пароля
        """

        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def compare_passwords(self, pass_hash, other_pass):
        """
        Метод проверки хэшированных паролей на совпадение
        """
        decoded_digest = base64.b64decode(pass_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_pass.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(decoded_digest, hash_digest)

    def get_by_username(self, name):
        """
        Поиск по имени пользователя
        """

        return self.dao.get_by_username(name)


