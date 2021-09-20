from django.core.exceptions import ObjectDoesNotExist
from djoser.urls.base import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from backend.authorize.models import EmailChangeKey
from backend.utils.send_mail import send_email


class SendChangeEmailCode(APIView):
    """Отправка кода подтверждения при смене email"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        new_email = request.data.get('new_email', None)

        if not new_email:
            return Response('Не указан новый email', status=400)

        if User.objects.filter(email=new_email).exists():
            return Response('Этот email уже используется', status=400)

        entry = EmailChangeKey(user=request.user, new_email=new_email)
        entry.save()

        if send_email(request.user.email, entry.key):
            return Response('Код подтверждения успешно отправлен')
        return Response('Неудача', status=400)


class ChangeEmail(APIView):
    """Изменение email"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        key = request.data.get('key', None)

        if not key:
            return Response('Не указан ключ', status=400)

        try:
            entry = EmailChangeKey.objects.get(key=key)
        except ObjectDoesNotExist:
            return Response('Не найдено записи с таким ключом', status=404)

        user = request.user
        user.email = entry.new_email
        user.save()
        entry.delete()
        return Response('Ваш email успешно изменен')
