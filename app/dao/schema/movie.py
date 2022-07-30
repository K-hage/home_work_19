from marshmallow import Schema, fields


class MovieSchema(Schema):
    """ Схема для сериализации фильмов """

    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre = fields.Pluck('GenreSchema', 'name')  # берем данные из жанров
    director = fields.Pluck('DirectorSchema', 'name')  # берем данные из режиссеров