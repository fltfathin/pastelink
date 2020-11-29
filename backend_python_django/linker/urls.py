from django.urls import path
from django.views.generic import TemplateView
from .views import shortlink_view, LoginView, logout_fn, Links, delete_link, oauth_callback

urlpatterns = [
    path("", TemplateView.as_view(template_name="linker/index.html"), name="index"),
    path("about/", TemplateView.as_view(template_name="linker/about.html"), name="about"),
    path("l/<slug:shortlink>", shortlink_view),
    path("login/", LoginView.as_view(), name="login"),
    path("login/oauth_callback", oauth_callback),
    path("logout/", logout_fn, name="logout"),
    path("shortlinks/", Links.as_view(), name="links"),
    path("shortlinks/<int:id>/delete", delete_link, name="delete_link")
]
