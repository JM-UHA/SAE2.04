from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render

from .models import Donnee, Capteur
from .forms import CapteurForm, DonneeForm


# Create your views here.


def root(request: HttpRequest):
    return render(request, "skeleton/main.jinja")


def donnee_all(request: HttpRequest):
    donnees = Donnee.objects.all()
    return render(request, "view.jinja", {"donnees": donnees})


def donnee_filter(request: HttpRequest):
    if request.method == "GET":
        return render(request, "donnees/filter.jinja", {"form": DonneeForm(request.GET)})
    elif request.method == "POST":
        donnees = Donnee.objects
        if form.is_valid():
            if capteur_id := form.cleaned_data['capteur_id']:
                donnees = donnees.filter(capteur=capteur_id)
            if date_min := form.cleaned_data['date_min']:
                donnees = donnees.filter(date__gte=date_min)
            if date_max := form.cleaned_data['date_max']:
                donnees = donnees.filter(date__lte=date_max)
            if heure_min := form.cleaned_data['heure_min']:
                donnees = donnees.filter(heure__gte=heure_min)
            if heure_max := form.cleaned_data['heure_max']:
                donnees = donnees.filter(heure__lte=heure_max)
            if temperature_min := form.cleaned_data['temperature_min']:
                donnees = donnees.filter(temperature__gte=temperature_min)
            if temperature_max := form.cleaned_data['temperature_max']:
                donnees = donnees.filter(temperature__lte=temperature_max)
        return render(request, "donnee/view.jinja", {"donnees": donnees})
    else:
        return HttpResponseBadRequest("Unknown method.")

def capteur_all(request: HttpRequest):
    capteurs = Capteur.objects.all()
    return render(request, "capteurs/all.jinja", {"capteurs": capteurs})


def capteur_view(request: HttpRequest, id: int):
    capteur = Capteur.objects.get(id=id)
    return render(request, "capteurs/view.jinja", {"capteur": capteur})


def capteur_edit(request: HttpRequest, id: int):
    capteur = Capteur.objects.get(id=id)

    if request.method == "GET":
        return render(request, "capteurs/edit.jinja", {"capteur": capteur, "form": CapteurForm()})

    elif request.method == "POST":
        form = CapteurForm(request.POST)

        if form.is_valid():
            form.save(True)

        return capteur_view(request, id)
    else:
        return HttpResponseBadRequest("Unknown method.")

