from .settings import *

# from .settings import BASE_DIR, DATABASES, SECRET_KEY, DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
