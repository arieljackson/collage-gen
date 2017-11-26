# urls.py
from django.conf.urls import url
from django.views.generic import TemplateView
from app import views
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^get_screenshot', views.get_screenshot, name='get_screenshot'),
]