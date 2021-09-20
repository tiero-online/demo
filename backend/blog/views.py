from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from backend.utils.decorators import permissions as perm

from backend.blog.models import Category, Post, Comments
from backend.blog.serializers import (CategorySerializer,
                                      PostSerializer,
                                      PostSingleSerializer,
                                      CommentsSerializer,
                                      CommentsPostSerializer,
                                      CommentsPUTSerializer)


class CategoriesList(APIView):
    """Список категорий"""
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        categories = Category.objects.filter(active=True)
        serializer = CategorySerializer(categories, many=True)
        return Response({"categories": serializer.data})


class PostList(APIView):
    """Список статей"""
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request):
        post = Post.objects.filter(published=True)
        serializer = PostSerializer(post, many=True)
        return Response({"post_list": serializer.data})

    def post(self, request):
        category = request.data.get("pk")
        post = Post.objects.filter(category=pk)
        serializer = PostSerializer(post, many=True)
        return Response({"post_list": serializer.data})


class PostSingle(APIView):
    """Полная статья, коментарии статьи"""
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        pk = request.GET.get("pk")
        post = Post.objects.get(id=pk)
        post.viewed += 1
        post.save()
        serializer = PostSingleSerializer(post)

        comments = Comments.objects.filter(post=post)
        ser_comments = CommentsSerializer(comments, many=True)

        news = Post.objects.order_by("-id")[:2]
        ser_news = PostSerializer(news, many=True)

        return Response({"post_single": serializer.data, "news": ser_news.data, "comments": ser_comments.data})

    @perm(permissions.IsAuthenticated)
    def post(self, request):
        comment = CommentsPostSerializer(data=request.data)
        if comment.is_valid():
            comment.save(user=request.user)
            return Response(status=201)
        else:
            return Response(status=400)

    @perm(permissions.IsAuthenticated)
    def put(self, request):
        instance = Comments.objects.get(id=request.data.get("id"))
        comment = CommentsPUTSerializer(instance=instance, data=request.data)
        if instance.user != request.user:
            return Response(status=403)

        if comment.is_valid():
            comment.save()
            return Response(status=201)
        else:
            return Response(comment.errors, status=400)