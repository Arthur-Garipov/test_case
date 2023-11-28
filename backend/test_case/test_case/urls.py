from api import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path('list_bookmarks/', views.list_bookmarks, name='list_bookmarks'),
    path('list_bookmarks/delete/<int:bookmark_id>/', views.delete_bookmark, name='delete_bookmark'),
    path(
        'list_bookmarks/delete/<int:bookmark_id>/',
        views.delete_bookmark,
        name='delete_bookmark',
    ),
]
