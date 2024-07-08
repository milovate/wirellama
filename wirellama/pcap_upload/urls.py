from django.urls import path
from .views import PCAPUploadView , CHATView

urlpatterns = [
    path('upload/', PCAPUploadView.as_view(), name='pcap-upload'),
    path('chat/', CHATView.as_view(), name='pcap-chat'),
]
