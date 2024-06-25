import base64
import csv
from io import BytesIO, StringIO

import matplotlib.pyplot as plt
import pandas as pd
from django.db.models.manager import BaseManager
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from .forms import CapteurForm, DonneeForm
from .models import Capteur, Donnee

# Create your views here.


def generate_graph(donnees: BaseManager[Donnee]):
    # Transformation des données en DataFrame pandas
    ds = donnees.values("capteur__capteur_id", "date", "heure", "temperature")

    # Transformation des données en DataFrame pandas
    df = pd.DataFrame(ds)
    df["datetime"] = pd.to_datetime(
        df["date"].astype(str) + " " + df["heure"].astype(str)
    )
    df.set_index("datetime", inplace=True)

    # Création du graphique
    plt.figure(figsize=(10, 6))

    # Groupement des données par capteur
    grouped = df.groupby("capteur__capteur_id")
    for capteur_id, group in grouped:
        plt.plot(group.index, group["temperature"], label=f"Capteur {capteur_id}")

    plt.xlabel("Temps")
    plt.ylabel("Température (°C)")
    plt.title("Température au fil du temps par Capteur")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    data = base64.b64encode(image_png).decode("utf-8")
    print(data)
    return data


def root(request: HttpRequest):
    return render(request, "skeleton/main.jinja")


def donnee_all(request: HttpRequest):
    donnees = Donnee.objects.all()
    graph = generate_graph(donnees)
    return render(
        request,
        "donnees/view.jinja",
        {
            "donnees": donnees,
            "donnees_ids": [donnee.pk for donnee in donnees],
            "graph": graph,
        },
    )


def donnee_filter(request: HttpRequest):
    if request.method == "GET":
        return render(
            request, "donnees/filter.jinja", {"form": DonneeForm(request.GET)}
        )
    elif request.method == "POST":
        form = DonneeForm(request.POST)
        donnees = Donnee.objects
        if form.is_valid():
            if capteur_id := form.cleaned_data["capteur_id"]:
                donnees = donnees.filter(capteur=capteur_id)
            if date_min := form.cleaned_data["date_min"]:
                donnees = donnees.filter(date__gte=date_min)
            if date_max := form.cleaned_data["date_max"]:
                donnees = donnees.filter(date__lte=date_max)
            if heure_min := form.cleaned_data["heure_min"]:
                donnees = donnees.filter(heure__gte=heure_min)
            if heure_max := form.cleaned_data["heure_max"]:
                donnees = donnees.filter(heure__lte=heure_max)
            if temperature_min := form.cleaned_data["temperature_min"]:
                donnees = donnees.filter(temperature__gte=temperature_min)
            if temperature_max := form.cleaned_data["temperature_max"]:
                donnees = donnees.filter(temperature__lte=temperature_max)
        graph = generate_graph(donnees)
        return render(
            request,
            "donnees/view.jinja",
            {
                "donnees": donnees,
                "donnees_ids": [donnee.pk for donnee in donnees],
                "graph": graph,
            },
        )
    else:
        return HttpResponseBadRequest("Unknown method.")


def donnee_export(request: HttpRequest):
    id_list = [int(id_str) for id_str in request.GET["ids"].split(",")]  # type: ignore

    donnees = Donnee.objects.filter(id__in=id_list)

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Capteur", "Date", "Heure", "Température"])

    for donnee in donnees:
        writer.writerow(
            [donnee.capteur.capteur_id, donnee.date, donnee.heure, donnee.temperature]
        )

    output.seek(0)
    response = HttpResponse(output, content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=donnees.csv"
    return response


def capteur_all(request: HttpRequest):
    capteurs = Capteur.objects.all()
    return render(request, "capteurs/all.jinja", {"capteurs": capteurs})


def capteur_view(request: HttpRequest, id: int):
    capteur = Capteur.objects.get(id=id)
    return render(request, "capteurs/view.jinja", {"capteur": capteur})


def capteur_edit(request: HttpRequest, id: int):
    capteur = Capteur.objects.get(id=id)

    if request.method == "GET":
        return render(
            request, "capteurs/edit.jinja", {"capteur": capteur, "form": CapteurForm()}
        )

    elif request.method == "POST":
        print(id)
        form = CapteurForm(request.POST, instance=capteur)
        print(form.data)

        if form.is_valid():
            form.save(True)

        return capteur_view(request, id)
    else:
        return HttpResponseBadRequest("Unknown method.")
