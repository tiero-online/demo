from django.urls import path, include

urlpatterns = [
    # path('tst/', include('backend.api.v2.tst.urls')),
    path('forum/', include('backend.api.v2.forum.urls')),

]
