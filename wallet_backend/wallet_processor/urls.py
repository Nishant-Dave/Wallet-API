from django.urls import path
from . import views

urlpatterns = [
    path('process_chunk/', views.ProcessChunkView.as_view()),
]
