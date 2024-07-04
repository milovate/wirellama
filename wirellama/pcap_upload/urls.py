from django.urls import path
from .views import PCAPUploadView

urlpatterns = [
    path('upload/', PCAPUploadView.as_view(), name='pcap-upload'),
]
