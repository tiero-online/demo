import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname("../" + __file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'DS.settings'

import django
django.setup()

from .models import UserProfile
from djoser.urls.base import User


def add_profiles():
    users = User.objects.all()
    for user in users:
        UserProfile.objects.create(user=user, id=user.id)
        print(user)
    print('завершено')


if __name__ == '__main__':
    add_profiles()
