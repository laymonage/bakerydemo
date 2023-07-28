from bakerydemo.settings.dev import *  # noqa

DEBUG_TOOLBAR_CONFIG = {
    # Always enable Django Debug Toolbar.
    "SHOW_TOOLBAR_CALLBACK": lambda r: True,
    # https://github.com/jazzband/django-debug-toolbar/issues/750
    "RESULTS_CACHE_SIZE": 100,
}

# Disable debug mode to simulate production environment.
DEBUG = False

# Use whitenoise to serve static files.
MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
