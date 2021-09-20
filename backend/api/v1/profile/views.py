from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import DynamicProfileSerializer

from backend.moderation.views import AboutModerator


class MyProfile(APIView):
    """Получение/редактирование профиля"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = DynamicProfileSerializer(
            request.user.profile,
            fields=(
                'username',
                'email',
                'image',
                'completed_courses'
            )
        )
        return Response({'profile': serializer.data})

    def post(self, request):
        serializer = DynamicProfileSerializer(
            request.user.profile,
            data=request.data,
            fields=('image',)
        )
        if serializer.is_valid() and 'img' in request.FILES:
            serializer.save(image=request.FILES['img'])
            return Response({"image": serializer.data}, status=200)
        return Response(serializer.errors, status=400)


class AboutMe(APIView):
    """
    Возвращает инфо о текущем юзере:
    id, username, модератор или нет, права модератора
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            'id': request.user.id,
            'username': request.user.username,
            'moder_info': AboutModerator().about_moderator(request.user)
        }
        return Response(data)
