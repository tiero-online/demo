from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions as perms

from .models import Review
from .serializers import ReviewSerializer
from backend.utils.api import BlankGetAPIView
from backend.utils.decorators import permissions


class AddReview(APIView):
    """Добавление отзыва"""
    permission_classes = [perms.IsAuthenticated]

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"review": serializer.data}, status=200)
        return Response(serializer.errors, status=400)


class NotModeratedReviews(BlankGetAPIView):
    """Вывод немодерированных отзывов"""
    permission_classes = [perms.IsAuthenticated]
    model = Review
    serializer = ReviewSerializer
    filter_params = {'moderated': False}


class ModeratedReviews(BlankGetAPIView):
    """Вывод модерированных отзывов"""
    # permission_classes = [perms.IsAuthenticated]
    model = Review
    serializer = ReviewSerializer
    filter_params = {'moderated': True}

    @permissions(perms.IsAdminUser)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class AllReviews(BlankGetAPIView):
    """Вывод всех отзывов"""
    # permission_classes = [perms.IsAuthenticated]
    model = Review
    serializer = ReviewSerializer

    @permissions(perms.IsAdminUser)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
