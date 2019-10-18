from django.urls import path
from . import views

from .views import (PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView)


urlpatterns = [
    path('', views.workIdeas, name='workIdeas'),
    path('<int:pk>/', PostDetailView.as_view(), name='workIdeas-post-detail'),
    path('new/', PostCreateView.as_view(), name='workIdeas-post-create'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='workIdeas-post-update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='workIdeas-post-delete')
]
