#!/usr/bin/env python3
# Fabrique l'app d'un autre vendeur à partir de celle de Quentin (index.html à la racine).
#   python3 outils/construire-espace.py ami-c728
# À relancer après chaque modification de l'app de Quentin, puis publier.
# Le script s'arrête si une phrase à adapter a disparu : il vaut mieux le savoir que publier un texte faux.
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
espace = sys.argv[1]
dossier = os.path.join(RACINE, espace)
os.makedirs(dossier, exist_ok=True)

t = open(os.path.join(RACINE, "index.html"), encoding="utf-8").read()

# Chez Quentin, l'agent tourne sur son propre Mac. Chez un autre vendeur, il tourne sans qu'il ait à s'en occuper.
PHRASES = [
    ('var ESPACE = "quentin";', 'var ESPACE = "%s";' % espace),
    ('href="icones/', 'href="../icones/'),
    ('". Claude passe dans les 2 heures, entre 8 h et 22 h, si ton Mac est allumé avec l\'app Claude ouverte.',
     '". L’agent passe en général dans les 2 heures, entre 9 h et 21 h.'),
    ("Les agents tournent sur ton Mac, avec Claude. Ils passent dans les 2 heures, entre 8 h et 22 h, quand l'app Claude est ouverte sur ton Mac.",
     "Les agents tournent tout seuls, avec Claude. Ils passent en général dans les 2 heures, entre 9 h et 21 h."),
    ("au plus tard dans les 2 heures, si ton Mac est allumé avec l'app Claude ouverte.",
     "en général dans les 2 heures, entre 9 h et 21 h."),
    ("Les agents Claude utilisent ton abonnement Claude, déjà payé", "Les agents sont gratuits pour toi"),
    ("dans les 2 heures entre 8 h et 22 h, quand l'app Claude est ouverte.", "en général dans les 2 heures, entre 9 h et 21 h."),
    ("dans les 2 heures entre 8 h et 22 h.", "en général dans les 2 heures, entre 9 h et 21 h."),
    ('"calcul de l\'app + ton Mac"', '"calcul de l\'app + Claude"'),
    ('"sur ton Mac"', '"automatique"'),
    ("dis-le à Claude et on ajuste les seuils", "dis-le à Quentin et on ajuste les seuils"),
    ('esc(ob.date || "2027-03-31")', 'esc(ob.date || "")'),
    ("Ton Mac", "L’agent"),
    ("ton Mac", "l’agent"),
]
for avant, apres in PHRASES:
    if avant not in t:
        sys.exit("Phrase introuvable, rien n'est fabriqué : " + avant)
    t = t.replace(avant, apres)

# Il ne doit plus rester de Mac que dans la détection de l'iPad et dans les commentaires.
for ligne in t.splitlines():
    if "Mac" in ligne and "MacIntel" not in ligne and not ligne.strip().startswith("/*"):
        sys.exit("Il reste un Mac dans le texte : " + ligne.strip()[:120])

open(os.path.join(dossier, "index.html"), "w", encoding="utf-8").write(t)

manifeste = json.load(open(os.path.join(RACINE, "manifest.webmanifest"), encoding="utf-8"))
for icone in manifeste["icons"]:
    icone["src"] = "../" + icone["src"]
json.dump(manifeste, open(os.path.join(dossier, "manifest.webmanifest"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

sw = open(os.path.join(RACINE, "sw.js"), encoding="utf-8").read()
sw = sw.replace('"./icones/', '"../icones/').replace('const CACHE = "pilote-v1";', 'const CACHE = "pilote-%s-v1";' % espace)
open(os.path.join(dossier, "sw.js"), "w", encoding="utf-8").write(sw)

print("App fabriquée dans", dossier)
