import json
import os
import re
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
URL = ("https://trouverunlogement.lescrous.fr/tools/48/search"
       "?bounds=3.8070597_43.6533542_3.9413208_43.5667088&locationName=Montpellier")
BASE = "https://trouverunlogement.lescrous.fr/tools/48/accommodations/"
FICHIER = "vus.json"


def notifier(texte):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": texte},
        timeout=20,
    )


html = requests.get(URL, timeout=20, headers={"User-Agent": "Mozilla/5.0"}).text
ids = set(re.findall(r"/accommodations/(\d+)", html))

if os.path.exists(FICHIER):
    vus = set(json.load(open(FICHIER)))
    premier = False
else:
    vus = set()
    premier = True

if premier:
    notifier(f"Bot Crous en ligne. {len(ids)} logement(s) détecté(s) pour l'instant.")
else:
    for i in sorted(ids - vus):
        notifier(f"Nouveau logement Crous : {BASE}{i}")

json.dump(sorted(vus | ids), open(FICHIER, "w"))
