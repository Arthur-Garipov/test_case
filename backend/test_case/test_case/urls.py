from api import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path('users/', include('users.urls')),
    path('add_bookmark/', views.add_bookmark, name='add_bookmark'),
    path('list_bookmarks/', views.list_bookmarks, name='list_bookmarks'),
]
