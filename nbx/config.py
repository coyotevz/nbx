# -*- coding: utf-8 -*-

from os import path

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '<must be secret>' # use os.urandom(24) to generate this
    ASSETS_OUTPUT_DIR = 'assets'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://nobix:nobix@localhost/nbx'

class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' %\
            path.join(path.abspath(path.curdir), 'data_nbx.db')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_UIR = 'sqlite://'
