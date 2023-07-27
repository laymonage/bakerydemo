from bakerydemo.settings.dev import *  # noqa

# Always enable Django Debug Toolbar.
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda r: True}
