from django.urls import path, include

urlpatterns = [
    path('authorize/', include('backend.api.v1.authorize.urls')),
    path('blog/', include('backend.api.v1.blog.urls')),
    path('courses/', include('backend.api.v1.courses.urls')),
    path('forum/', include('backend.api.v1.forum.urls')),
    path('moderation/', include('backend.api.v1.moderation.urls')),
    path('profile/', include('backend.api.v1.profile.urls')),
    path('reviews/', include('backend.api.v1.reviews.urls')),
    path('tests/', include('backend.api.v1.tests.urls')),

]
