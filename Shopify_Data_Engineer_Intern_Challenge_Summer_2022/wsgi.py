"""
WSGI config for Shopify_Data_Engineer_Intern_Challenge_Summer_2022 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Shopify_Data_Engineer_Intern_Challenge_Summer_2022.settings')

application = get_wsgi_application()
