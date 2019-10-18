from django.urls import path
from . import views

from .views import (PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView)


urlpatterns = [
    path('', views.dossiers, name='dossiers'),
    path('dossiers/<int:pk>/', PostDetailView.as_view(), name='dossiers-post-detail'),
    path('dossiers/new/', PostCreateView.as_view(), name='dossiers-post-create'),
    path('dossiers/<int:pk>/update', PostUpdateView.as_view(), name='dossiers-post-update'),
    path('dossiers/<int:pk>/delete', PostDeleteView.as_view(), name='dossiers-post-delete')
]
