# importing everything from the settings file

from .settings import *

# overriding the database and making sure it's local for the tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "memory",
    }
}


# just in case we send some emails, so when testing it won't send any emails
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


