class GenresService:
    def __init__(self, dao):
        self.dao = dao

    def get_one(self, genre_id):
        """
        Возвращает данные жанра по id
        """
        return self.dao.get_one(genre_id)

    def get_all(self):
        """
        Возвращает данные всех жанров
        """
        return self.dao.get_all()

    def check_is_dict(self, data):
        """
        Проверка: являются ли данные словарем
        """
        return self.dao.check_is_dict(data)

    def create(self, data):
        """
        Создание данных нового жанра
        """
        return self.dao.create(data)

    def update(self, genre_id, data):
        """
        Обновление данных жанра по id
        """
        genre = self.dao.get_one(genre_id)

        genre.id = data.get('id')
        genre.name = data.get('name')

        return self.dao.update(genre)

    def update_partial(self, genre_id, data):
        """
        Частичное обновление данных жанра по id
        """
        genre = self.dao.get_one(genre_id)

        if 'id' in data:
            genre.id = data.get('id')
        if 'name' in data:
            genre.name = data.get('name')

        return self.dao.update(genre)

    def delete(self, genre_id):
        """
        Удаление данных жанра
        """
        self.dao.delete(genre_id)
