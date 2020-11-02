# vi /usr/local/victolee/Channels_test/Channels_test_project/asgi.py
"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from channels.routing import get_default_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "signup.settings")
django.setup()
application = get_default_application()
