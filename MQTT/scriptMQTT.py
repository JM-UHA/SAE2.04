# Code de récupération des données MQTT

from paho.mqtt.client import MQTTMessage, Client, ConnectFlags
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.reasoncodes import ReasonCode
from paho.mqtt.properties import Properties
import typing
import mysql.connector
from datetime import datetime


temp_save: list[dict[str, typing.Any]] = []
WHITELIST_CAPTEURS = ["B8A5F3569EFF", "A72E3F6B79BB"]

db_config = {
    "host": "db.grp11.local",
    "user": "toto",
    "password": "toto",
    "database": "dbcapteurs",
    "connection_timeout": 1
}

INSERT_CAPTEUR = "INSERT IGNORE INTO Capteurs (capteur_id, piece, lieu, emplacement) VALUES (%(id)s, %(piece)s, %(lieu)s, NULL)"
INSERT_DONNEES = "INSERT INTO Donnees (capteur_id, date, heure, temperature) VALUES (%(id)s, %(date)s, %(time)s, %(temp)s)"

try:
    db = mysql.connector.connect(**db_config)
    print("Connecté à la base de données.")
except Exception as exception:
    db = None
    print(f"Impossible de se connecter à la base de données : {exception}")


def publier_vers_db(donnees: list[dict[typing.Any, typing.Any]]):
    global db
    db = typing.cast(mysql.connector.MySQLConnection, db)
    cursor = db.cursor()
    for donnee in donnees:
        cursor.execute(INSERT_CAPTEUR, donnee)
        cursor.execute(INSERT_DONNEES, donnee)
    db.commit()
    cursor.close()

def on_connect(client: Client, userdata: typing.Any, flags: ConnectFlags, reason_code: ReasonCode, properties: Properties):
    if reason_code == 0:
        print("Connecté au broker avec succès")
        client.subscribe("IUT/Colmar2024/SAE2.04/Maison1")
        client.subscribe("IUT/Colmar2024/SAE2.04/Maison2")
    else:
        print(f"Échec de la connexion, code de retour {reason_code}")

def on_message(client: Client, userdata: typing.Any, msg: MQTTMessage):
    global db
    global temp_save
    payload = msg.payload.decode('utf-8')
    print(f"========== {msg.topic} =============\n{payload}")

    lieu = msg.topic.split("/")[-1]
    print(lieu)

    infos: list[str] = payload.split(",")
    infos_cle_valeurs: list[list[str]] = [info.split("=") for info in infos]
    true_info: dict[str, typing.Any] = {info[0].lower(): info[1] for info in infos_cle_valeurs}
    true_info["lieu"] = lieu


    # Pour la date
    true_info["date"] = datetime.strptime(true_info["date"], "%d/%m/%Y").date()

    # Pour l'heure
    true_info["time"] = datetime.strptime(true_info["time"], "%H:%M:%S").time()


    if true_info["id"] not in WHITELIST_CAPTEURS:
        print("Ignoré.")
        return

    if db and db.is_connected():
        publier_vers_db(temp_save)
        temp_save = []
    else:
        try:
            db = mysql.connector.connect(**db_config)
        except Exception as exception:
            print(f"Impossible de se connecter à la base de données : {exception}")
        print(f"Sauvegardé dans mémoire temporaire : Entrée {len(temp_save)}")
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
