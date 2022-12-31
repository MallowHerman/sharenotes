from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('download_file/<str:filename>', views.download_file, name='download_file'),
    path('document/<slug:slug>/<str:pk>', views.documentDetailView, name='document_detail'),
    path('upload-document/', views.upload_document, name='upload_document'),

    path('document-like/<int:pk>', views.documentLike, name='document_like'),
]