from django.urls import path
from . import views

from .views import (PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView)


urlpatterns = [
    path('', views.dossiers, name='dossiers'),
    path('<int:pk>/', PostDetailView.as_view(), name='dossiers-post-detail'),
    path('new/', PostCreateView.as_view(), name='dossiers-post-create'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='dossiers-post-update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='dossiers-post-delete')
]
