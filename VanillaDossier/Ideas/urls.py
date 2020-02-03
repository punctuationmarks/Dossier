from django.urls import path
from . import views

from .views import (PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView)


urlpatterns = [
    path('', views.ideas, name='ideas'),
    path('<int:pk>/', PostDetailView.as_view(), name='ideas-detail'),
    path('new/', PostCreateView.as_view(), name='ideas-create'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='ideas-update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='ideas-delete')
]
