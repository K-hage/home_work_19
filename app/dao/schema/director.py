from marshmallow import Schema, fields


class DirectorSchema(Schema):
    """ Схема для сериализации режиссеров """

    id = fields.Int(dump_only=True)
    name = fields.Str()
