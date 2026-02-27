from django.urls import include, path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("", include("django.contrib.auth.urls")),
]
