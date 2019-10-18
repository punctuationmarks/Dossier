from django.urls import path
from . import views

from .views import (PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView)


urlpatterns = [
    path('', views.thoughts, name='thoughts'),
    path('<int:pk>/', PostDetailView.as_view(), name='thoughts-post-detail'),
    path('new/', PostCreateView.as_view(), name='thoughts-post-create'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='thoughts-post-update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='thoughts-post-delete')
]
