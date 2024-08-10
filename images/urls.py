# urls.py
from django.urls import path
from .views import GenerateImagesView

urlpatterns = [
    path('generate-images/', GenerateImagesView.as_view(), name='generate_images'),
    # path('generate/status/', RetrieveImagesView.as_view(), name='retrieve-images-status'),
]
