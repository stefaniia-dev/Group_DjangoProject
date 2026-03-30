from django.apps import AppConfig
import json
import _json

from django.template.context_processors import request


class SchoolmanagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SchoolManager'

# def SchoolManager():
#     output = request.get_json()
#     print(output)