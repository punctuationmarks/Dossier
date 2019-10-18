from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # need to update and make these
    # path('dossiers-upload-csv/', views.dossiers_upload_csv_file, name='dossiers_upload_csv'),
    # path('blog-upload-csv/', views.blog_upload_csv_file, name='blog_upload_csv'),
    # path('workIdeas-upload-csv/', views.workIdeas_upload_csv_file, name='workIdeas_upload_csv')
]
