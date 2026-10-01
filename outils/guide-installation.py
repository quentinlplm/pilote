#!/usr/bin/env python3
# Dessine le guide d'installation illustré, avec le QR code personnel d'un espace.
#   python3 outils/guide-installation.py ami-c728 ~/Desktop/Pilote-ami/
# La clé d'installation est lue dans ~/.pilote/installation-<espace> : elle n'est jamais écrite ici.
import os
import sys

import qrcode
from PIL import Image, ImageDraw, ImageFont

espace, dossier = sys.argv[1], os.path.expanduser(sys.argv[2])
cle = open(os.path.expanduser("~/.pilote/installation-" + espace)).read().strip()
LIEN = "https://quentinlplm.github.io/pilote/%s/#installer=%s" % (espace, cle)
ICONE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icones", "icone-512.png")

S = 2                                   # on dessine en double, puis on réduit : traits nets
W = 1080 * S
AV = "/System/Library/Fonts/Avenir Next.ttc"
POIDS = {"heavy": 8, "bold": 0, "demi": 2, "medium": 5, "regular": 7}
def p(taille, poids): return ImageFont.truetype(AV, int(taille * S), index=POIDS[poids])
ENCRE, PAPIER, BLANC = (13, 15, 17), (245, 243, 239), (255, 255, 255)
VERT, VERT_VIF, VERT_DOUX = (7, 94, 87), (10, 122, 113), (226, 241, 238)
GRIS, GRIS_CLAIR, FILET, OMBRE = (75, 80, 87), (201, 204, 209), (214, 209, 199), (222, 218, 210)
NB, AP = " ", "’"
M = 80 * S


def lignes(d, texte, police, largeur):
    res, cur = [], ""
    for m in texte.split(" "):
        essai = (cur + " " + m).strip()
        if d.textlength(essai, font=police) <= largeur:
            cur = essai
        else:
            res.append(cur)
            cur = m
    return res + [cur]


def paragraphe(d, x, y, texte, police, largeur, couleur, interligne, dessin):
    for l in lignes(d, texte, police, largeur):
        if dessin:
            d.text((x, y), l, font=police, fill=couleur)
        y += interligne
    return y


def icone(img, x, y, taille, rayon):
    ic = Image.open(ICONE).resize((taille, taille))
    masque = Image.new("L", ic.size, 0)
    ImageDraw.Draw(masque).rounded_rectangle([0, 0, taille, taille], radius=rayon, fill=255)
    img.paste(ic, (x, y), masque)


def picto(img, d, n, x, y, t):
    d.rounded_rectangle([x, y, x + t, y + t], radius=28 * S, fill=VERT_DOUX)
    c, e = VERT, int(6 * S)
    cx, cy = x + t // 2, y + t // 2
    if n == 1:      # un téléphone et sa barre d'adresse
        d.rounded_rectangle([cx - 30 * S, cy - 46 * S, cx + 30 * S, cy + 46 * S], radius=12 * S, outline=c, width=e)
        d.rounded_rectangle([cx - 18 * S, cy - 30 * S, cx + 18 * S, cy - 20 * S], radius=5 * S, fill=c)
        d.line([cx - 10 * S, cy + 34 * S, cx + 10 * S, cy + 34 * S], fill=c, width=e)
    elif n == 2:    # six points de code, trois déjà tapés
        for i in range(6):
            px, py, r = cx + (i % 3 - 1) * 26 * S, cy + (i // 3 - 0.5) * 30 * S, 9 * S
            if i < 3:
                d.ellipse([px - r, py - r, px + r, py + r], fill=c)
            else:
                d.ellipse([px - r, py - r, px + r, py + r], outline=c, width=int(4 * S))
    elif n == 3:    # le bouton Partager de l'iPhone
        d.line([cx - 16 * S, cy - 14 * S, cx - 30 * S, cy - 14 * S, cx - 30 * S, cy + 40 * S, cx + 30 * S, cy + 40 * S,
                cx + 30 * S, cy - 14 * S, cx + 16 * S, cy - 14 * S], fill=c, width=e, joint="curve")
        d.line([cx, cy + 14 * S, cx, cy - 44 * S], fill=c, width=e)
        d.line([cx - 16 * S, cy - 28 * S, cx, cy - 44 * S, cx + 16 * S, cy - 28 * S], fill=c, width=e, joint="curve")
    else:           # l'icône de Pilote
        icone(img, x + int(t * .18), y + int(t * .18), int(t * .64), 18 * S)


ETAPES = [
    ("Ouvre le lien", [(None, "Sur iPhone dans Safari, sur Android dans Chrome. S" + AP + "il s" + AP + "ouvre dans Snap, Insta ou WhatsApp, copie-le dans ton navigateur.")]),
    ("Choisis ton code", [(None, "6 chiffres, à taper deux fois, puis «" + NB + "Enregistrer mon code" + NB + "». C" + AP + "est la clé de ton app" + NB + ": retiens-le.")]),
    ("Mets-la sur ton écran d" + AP + "accueil", [
        ("iPhone", "Partager, puis «" + NB + "Sur l" + AP + "écran d" + AP + "accueil" + NB + "», puis «" + NB + "Ajouter" + NB + "»."),
        ("Android", "Les 3 petits points en haut à droite, puis «" + NB + "Installer l" + AP + "application" + NB + "».")]),
    ("Ouvre Pilote", [(None, "Touche le cintre vert sur ton écran d" + AP + "accueil, tape ton code" + NB + ": c" + AP + "est prêt.")]),
]


def dessiner(img, d, dessin):
    # 1. le bandeau
    if dessin:
        d.rectangle([0, 0, W, 640 * S], fill=ENCRE)
        icone(img, M, 84 * S, 150 * S, 34 * S)
        d.text((M, 262 * S), "Pilote", font=p(118, "heavy"), fill=PAPIER)
    paragraphe(d, M, 418 * S, "Ton app Vinted" + NB + ": ton stock, tes envois et ta compta, dans ta poche.",
               p(38, "medium"), W - 2 * M, GRIS_CLAIR, 54 * S, dessin)
    # 2. la carte du QR code, à cheval sur le bandeau
    cy0, cy1 = 560 * S, 1050 * S
    if dessin:
        d.rounded_rectangle([M, cy0 + 8 * S, W - M, cy1 + 8 * S], radius=40 * S, fill=OMBRE)
        d.rounded_rectangle([M, cy0, W - M, cy1], radius=40 * S, fill=BLANC)
        q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=1)
        q.add_data(LIEN)
        q.make(fit=True)
        qi = q.make_image(fill_color=ENCRE, back_color=BLANC).convert("RGB").resize((410 * S, 410 * S), Image.NEAREST)
        img.paste(qi, (M + 40 * S, cy0 + 40 * S))
    tx = M + 494 * S
    largeur_tx = W - M - 40 * S - tx
    yy = cy0 + 70 * S
    if dessin:
        d.text((tx, yy), "Scanne-moi", font=p(50, "heavy"), fill=ENCRE)
    yy = paragraphe(d, tx, yy + 82 * S, "avec l" + AP + "appareil photo de ton téléphone.", p(32, "medium"), largeur_tx, GRIS, 44 * S, dessin)
    yy += 26 * S
    if dessin:
        d.line([tx, yy, W - M - 40 * S, yy], fill=FILET, width=2 * S)
    paragraphe(d, tx, yy + 26 * S, "Tu as reçu le lien par message" + NB + "? Ouvre-le directement" + NB + ": c" + AP + "est pareil.",
               p(29, "regular"), largeur_tx, GRIS, 41 * S, dessin)
    # 3. les étapes
    y = cy1 + 96 * S
    if dessin:
        d.text((M, y), "En 4 étapes", font=p(54, "heavy"), fill=ENCRE)
    y += 104 * S
    T, xt = 124 * S, M + 104 * S
    largeur_t = W - M - T - 36 * S - xt
    for i, (titre, morceaux) in enumerate(ETAPES, 1):
        y0 = y
        if dessin:
            d.ellipse([M, y, M + 76 * S, y + 76 * S], fill=VERT_VIF)
            f = p(40, "heavy")
            d.text((M + 38 * S - d.textlength(str(i), font=f) / 2, y + 12 * S), str(i), font=f, fill=BLANC)
            picto(img, d, i, W - M - T, y0, T)
        y = paragraphe(d, xt, y + 8 * S, titre, p(40, "demi"), largeur_t, ENCRE, 52 * S, dessin) + 6 * S
        for etiquette, texte in morceaux:
            if etiquette:
                fe = p(24, "demi")
                lg = d.textlength(etiquette, font=fe) + 28 * S
                if dessin:
                    d.rounded_rectangle([xt, y + 6 * S, xt + lg, y + 44 * S], radius=19 * S, fill=VERT_DOUX)
                    d.text((xt + 14 * S, y + 9 * S), etiquette, font=fe, fill=VERT)
                y = paragraphe(d, xt, y + 56 * S, texte, p(31, "regular"), largeur_t, GRIS, 44 * S, dessin) + 10 * S
            else:
                y = paragraphe(d, xt, y, texte, p(31, "regular"), largeur_t, GRIS, 44 * S, dessin)
        y = max(y, y0 + T) + 52 * S
        if dessin and i < len(ETAPES):
            d.line([xt, y - 26 * S, W - M, y - 26 * S], fill=FILET, width=2 * S)
    # 4. l'encart et le pied
    y += 8 * S
    texte = ("Ensuite, tout est automatique" + NB + ": mets tes articles en ligne sur Vinted comme d" + AP +
             "habitude, ils arrivent dans Pilote en général dans les 2 heures, entre 9 h et 21 h.")
    h = len(lignes(d, texte, p(31, "demi"), W - 2 * M - 80 * S)) * 46 * S + 72 * S
    if dessin:
        d.rounded_rectangle([M, y, W - M, y + h], radius=30 * S, fill=VERT_DOUX)
    paragraphe(d, M + 40 * S, y + 36 * S, texte, p(31, "demi"), W - 2 * M - 80 * S, VERT, 46 * S, dessin)
    y += h + 50 * S
    paragraphe(d, M, y, "Ce QR code et le lien sont personnels" + NB + ": ne les partage pas.", p(27, "medium"), W - 2 * M, GRIS, 40 * S, dessin)
    return y + 110 * S


brouillon = Image.new("RGB", (W, 6000 * S), PAPIER)
H = dessiner(brouillon, ImageDraw.Draw(brouillon), False)
img = Image.new("RGB", (W, H), PAPIER)
dessiner(img, ImageDraw.Draw(img), True)
os.makedirs(dossier, exist_ok=True)
img.resize((W // S, H // S), Image.LANCZOS).save(os.path.join(dossier, "Guide-Pilote-avec-QR.png"), optimize=True)
q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=16, border=3)
q.add_data(LIEN)
q.make(fit=True)
q.make_image(fill_color=ENCRE, back_color=BLANC).save(os.path.join(dossier, "QR-code-Pilote.png"))
print("Guide et QR code rangés dans", dossier)
