import json


class DevelopmentConfig(object):

    DEBUG = True
    TESTING = False

    SECRET_KEY = "akjwerht9834hgpaofjgn38rn"

    MYSQL_USER = "root"
    MYSQL_PASSWORD = "password"
    MYSQL_DATABASE = "companydb"

    # UPLOADS = "/home/username/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = False

    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost/users'
    }

    JWT_SECRET_KEY = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'

    JWT_BLACKLIST_ENABLED = True
