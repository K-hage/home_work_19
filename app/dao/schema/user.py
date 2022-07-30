from marshmallow import Schema, fields


class UserSchema(Schema):
    """ Модель пользователя """

    __tablename__ = 'user'
    id = fields.Int(dump_only=True)
    username = fields.Str()
    password = fields.Str()
    role = fields.Str()
