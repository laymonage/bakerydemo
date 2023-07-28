from bakerydemo.settings.dev import *  # noqa

# Always enable Django Debug Toolbar.
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda r: True}

# Disable debug mode to simulate production environment.
DEBUG = False

# Use whitenoise to serve static files.
MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
