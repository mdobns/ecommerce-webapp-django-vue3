"""
apps.py
"""
from django.apps import AppConfig


class CartConfig(AppConfig):
    '''
    Config to show the table in django admin
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cart'
