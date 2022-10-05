import os

import environ

from .base import *  # noqa

env = environ.Env()
environ.Env.read_env((os.path.join(BASE_DIR, ".env.local")))  # noqa

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

# Recaptcha settings
# This key only allows localhost. For production, you'll want your own API keys.
# You can get Recaptcha API key from google.com/recaptcha
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")
NOCAPTCHA = True


# Uncomment this line to enable template caching
# Dont forget to change the LOCATION path
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.environ.get("CACHE_DIR"),
    }
}


try:
    from .local import *  # noqa
except ImportError:
    pass
