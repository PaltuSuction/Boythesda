"""
WSGI config for boythesda project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from io import StringIO
from dotenv import dotenv_values
filelike = StringIO('SPAM=EGGS\n')
filelike.seek(0)
parsed = dotenv_values(stream=filelike)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boythesda.settings')

application = get_wsgi_application()
