from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-caveq*7llx2ds_fr=a0qi%&gpkdi&9mqy7$)svid4@omqnl7ko"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = INSTALLED_APPS + [  # noqa
    "debug_toolbar",
    "django_extensions",
]

MIDDLEWARE = MIDDLEWARE + [  # noqa
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ("127.0.0.1", "172.17.0.1")

try:
    from .local import *  # noqa
except ImportError:
    pass
