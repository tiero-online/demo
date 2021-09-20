from django.core.management.base import BaseCommand
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Command(BaseCommand):
    help = 'Add superuser'

    def handle(self, *args, **options):
        User.objects.create_user(username="DJWOMS",
                            password='Djwoms25',
                            email="socanime@gmail.com",
                            is_superuser=True,
                            is_staff=True)
        # User.objects.create_user(username=79686677771,
        #                     password='gEvgOnsalez787',
        #                     email="djgonsalez@ya.ru",
        #                     is_superuser=True,
        #                     is_staff=True)
        self.stdout.write('Success')
