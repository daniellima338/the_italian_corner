from django.apps import AppConfig


class BlogConfig(AppConfig):
    """ Configuration of the blog"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
