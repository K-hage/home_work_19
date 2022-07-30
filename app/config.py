class Config:
    DEBUG = True  # режим debug
    SECRET_HERE = '249y823r9v8238r9u'
    JSON_AS_ASCII = False  # использование ASCII
    JSON_SORT_KEYS = False  # сортировка ключей json
    SQLALCHEMY_DATABASE_URI = 'sqlite:///movies.db'  # путь к базе данных sqllite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSONIFY_PRETTYPRINT_REGULAR = True  # построчное отображение json данных
    RESTX_JSON = {'ensure_ascii': False}

