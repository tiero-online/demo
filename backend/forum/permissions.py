from rest_framework.permissions import BasePermission

# from .models import MinimalForumBannedUsers, MaximalForumBannedUsers
from backend.moderation.models import BannedUser


# from utils.blacklist import get_or_create_blacklist


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsModerator(BasePermission):
    """Доступ модератору"""

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.profile.is_forum_moderator
        )


# class NotMinimalBanned(BasePermission):
#     """Доступ юзеру, у которого нет минимального бана"""
#     def has_permission(self, request, view):
#         blacklist = get_or_create_blacklist(MinimalForumBannedUsers).blacklist.all()
#         return request.user not in blacklist
#
#
# class NotMaximalBanned(BasePermission):
#     """Доступ юзеру, у которого нет максимального бана"""
#     def has_permission(self, request, view):
#         blacklist = get_or_create_blacklist(MaximalForumBannedUsers).blacklist.all()
#         return request.user not in blacklist
#
#
# class NotBanned(BasePermission):
#     """Доступ юзеру, у которого нет никакого бана"""
#     def has_permission(self, request, view):
#         blacklist = get_or_create_blacklist(MinimalForumBannedUsers).blacklist.all()
#         blacklist2 = get_or_create_blacklist(MaximalForumBannedUsers).blacklist.all()
#         # blacklist.union(blacklist2)
#         return request.user not in blacklist and request.user not in blacklist2


class CanWriteComments(BasePermission):
    """
    Доступ юзеру, у которого
    нет бана на комментирование
    """

    def has_permission(self, request, view):
        return not BannedUser.objects.filter(user=request.user, ban_action=1).exists()


class CanCreateTopics(BasePermission):
    """
    Доступ юзеру, у которого
    нет бана на создание топиков
    """

    def has_permission(self, request, view):
        return not BannedUser.objects.filter(user=request.user, ban_action=2).exists()


class HaveAccessToForum(BasePermission):
    """
    Доступ анонимному юзеру или юзеру,
    у которого нет бана на доступ к форуму
    """

    def has_permission(self, request, view):
        return request.user.is_anonymous or (
            not BannedUser.objects.filter(user=request.user, ban_action=3).exists()
        )


class IsAuthorOrModeratorTopics(BasePermission):
    """

    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.user or (
                request.user.profile.is_forum_moderator and (
                    0 in request.user.moderator_rights.rights.all() or
                    4 in request.user.moderator_rights.rights.all()
                )
            )
        )
