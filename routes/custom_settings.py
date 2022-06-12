"""
custom settings
"""

# from gpsfun.settings import *


DEBUG = True

ADMINS = (
    ('kostin', 'kostin@halogen-dg.com'),
)

MANAGERS = ADMINS

DATABASE_NAME = 'mountain_routes'             # Or path to database file if using sqlite3.
DATABASE_USER = 'climber'             # Not used with sqlite3.
DATABASE_PASSWORD = 'lotofroutes'         # Not used with sqlite3.
# DATABASE_USER = 'root'             # Not used with sqlite3.
# DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

DATABASES = {
    "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": DATABASE_NAME,
            "USER": DATABASE_USER,
            "PASSWORD": DATABASE_PASSWORD,
            "HOST": DATABASE_HOST,
            "PORT": DATABASE_PORT,
    }
}


SAFE_EMAILS = [ADMINS[0][1]]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'nmail.ua2web.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'kostin@halogen.kharkov.ua'
EMAIL_HOST_PASSWORD = 'WuktuletOd'
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
