# Code de récupération des données MQTT

from paho.mqtt.client import MQTTMessage, CallbackAPIVersion, Client, ConnectFlags, ReasonCode, Properties
import typing
import mysql.connector
from datetime import datetime, date, time


temp_save = []
WHITELIST_CAPTEURS = ["B8A5F3569EFF", "A72E3F6B79BB"]

db_config = {
    "host": "db.grp11.local",
    "user": "toto",
    "password": "toto",
    "database": "dbcapteurs"
}

INSERT_CAPTEUR = "INSERT IGNORE INTO Capteurs (capteur_id, piece, lieu, emplacement) VALUES (%(id)s, %(piece)s, %(lieu)s, NULL)"
INSERT_DONNEES = "INSERT INTO Donnees (capteur_id, date, heure, temperature) VALUES (%(id)s, %(date)s, %(time)s, %(temp)s)"

try:
    db = mysql.connector.connect(**db_config)
except Exception as exception:
    print(f"Impossible de se connecter à la base de données : {exception}")

class Data(typing.TypedDict):
    capteur: Capteur
    donnee: Donnee


def publier_vers_db(donnees: list[dict]):
    for donnee in donnees:
        cursor = db.cursor()
        cursor.execute(INSERT_CAPTEUR, donnee)
        cursor.execute(INSERT_DONNEES, donnee)

def on_connect(client: Client, userdata: typing.Any, flags: ConnectFlags, reason_code: ReasonCode, properties: Properties):
    if reason_code == 0:
        print("Connecté au broker avec succès")
        client.subscribe("IUT/Colmar2024/SAE2.04/Maison1")
        client.subscribe("IUT/Colmar2024/SAE2.04/Maison2")
    else:
        print(f"Échec de la connexion, code de retour {rc}")

def on_message(client: Client, userdata: typing.Any, msg: MQTTMessage):
    payload = msg.payload.decode('utf-8')
    print(f"=== {msg.topic} ===\n{payload}")

    lieu = msg.topic.split("/")[-1]
    print(lieu)

    infos: list[str] = payload.split(",")
    infos_cle_valeurs: list[list[str]] = [info.split("=") for info in infos]
    true_info = {info[0].lower(): info[1] for info in infos_cle_valeurs}
    true_info["lieu"] = lieu


    # Pour la date
    true_info["date"] = datetime.strptime(date_str, "%d/%m/%Y").date()

    # Pour l'heure
    true_info["time"] = datetime.strptime(time_str, "%H:%M:%S").time()


    if id not in WHITELIST_CAPTEURS:
        return

    if db.is_connected():
        publier_vers_db(temp_save)
        temp_save = []
    else:
        try:
            db.connect()
        except Exception as exception:
            print(f"Impossible de se connecter à la base de données : {exception}")
        temp_save.append(true_info)

client = Client(CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("KeyboardInterrupt")
finally:
    client.loop_stop()
    client.disconnect()
