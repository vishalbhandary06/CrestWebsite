from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"), 
    path("careers", views.careers, name="careers"),
    path("contact", views.contact, name="contact"), 
    path("industries", views.industries, name="industries"),
    path("technologies", views.technologies, name="technologies"),
    path("services", views.services, name="services"),
    path("aboutus", views.aboutus, name="aboutus"), 
    path("sitemap", views.sitemap, name="sitemap"), 
]