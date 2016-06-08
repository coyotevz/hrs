# -*- coding: utf-8 -*-

from os import path

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '<must be secret>' # use os.random(24) to generate this
    CRSF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
        path.join(path.abspath(path.curdir), 'data_hrs.db'))


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://' # in memory database
