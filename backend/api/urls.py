from django.urls import path, include

urlpatterns = [
    path('v1/', include('backend.api.v1.urls')),
    path('v2/', include('backend.api.v2.urls'))
]
