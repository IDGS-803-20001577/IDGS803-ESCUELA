import os
from sqlalchemy import create_engine

import urllib

class Config(object):
    SECRET_KEY='SUPER_SECRET_KEY'
    SESSION_COOKIE_SECURITY=False

# Proceso de Configuracion a la BD

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:1234@127.0.0.1/escuela803"
    SQLALCHEMY__TRACK_MODIFICATION=False