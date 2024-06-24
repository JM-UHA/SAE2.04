from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.root),
    path("all/", views.donnee_all, name="donnee.all"),
    path("filter/", views.donnee_filter, name="donnee.filter"),

    path("capteurs/", views.capteur_all, name="capteur.all"),
    path("capteurs/<int:id>/", views.capteur_view, name="capteur.view"),
    path("capteurs/<int:id>/edit/", views.capteur_edit, name="capteur.edit")
]
