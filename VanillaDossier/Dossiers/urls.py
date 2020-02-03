from django.urls import path
from . import views

from .views import (PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView)


urlpatterns = [
    path('', views.dossiers, name='dossiers'),
    path('<int:pk>/', PostDetailView.as_view(), name='dossiers-detail'),
    path('new/', PostCreateView.as_view(), name='dossiers-create'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='dossiers-update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='dossiers-delete')
]
