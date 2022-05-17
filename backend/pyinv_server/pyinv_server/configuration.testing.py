###################################################################
#  This file serves as a base configuration for testing purposes  #
#  only. It is not intended for production use.                   #
###################################################################

ALLOWED_HOSTS = ["*"]

DATABASE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'db.sqlite',
}

SECRET_KEY = 'django-insecure-rT1%IHNOY&jAn9b-7(uoOdlVKb(giEcBhMK$6+sGp3UO-X^FPe'

DEBUG = True
