from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r"^message/\$process-message$", views.process_message),
    path("message/", views.MensajeList.as_view()),
    path("message/<pk>", views.MensajeItem.as_view())
]