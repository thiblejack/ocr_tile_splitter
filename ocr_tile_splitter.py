import os
from PIL import Image
import pytesseract
import glob
import re

# === Configuration ===
INPUT_FOLDER = "input_pages"
OUTPUT_FOLDER = "output_tiles"
#ROWS = 6       # nombre de lignes dans la grille
#COLS = 4       # nombre de colonnes
XPOS = [82,1142,2565,3625]
YPOS = [243,733,1223,1713,2203,2693]
TPOS = [45,395,460,85]
USE_OCR = True # passer à False pour désactiver la reconnaissance de texte
LANG = "eng"   # langue pour Tesseract (ajuster si nécessaire : 'fra', 'deu', etc.)

# === Création du dossier de sortie ===
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === Nettoyeur de nom de fichier à partir de texte OCR ===
def sanitize_filename(text, fallback):
    text = text.strip()
    text = re.sub(r'[^\w\s-]', '', text)  # Supprime les caractères spéciaux
    text = re.sub(r'[\s_]+', '_', text)   # Remplace espaces/underscores par un seul underscore
    return text[:40] if text else fallback

# === Traitement des pages ===
for page_path in sorted(glob.glob(f"{INPUT_FOLDER}/*.png")):
    print(f"Traitement de {page_path}")
    base_name = os.path.splitext(os.path.basename(page_path))[0]
    image = Image.open(page_path)
    width, height = image.size

    tile_width = 1060 #width // COLS
    tile_height = 490#height // ROWS

    for col in range(len(XPOS)):
        for row in range(len(YPOS)):
            x = XPOS[col]
            y = YPOS[row]
            left = x
            top = y
            right = left + tile_width
            bottom = top + tile_height

            tile = image.crop((left, top, right, bottom))

            if USE_OCR:
                left = left + TPOS[0]
                top = top + TPOS[1]
                right = left + TPOS[2]
                bottom = top + TPOS[3]
                zone = image.crop((left, top, right, bottom))
                text = pytesseract.image_to_string(zone, lang=LANG, config="--psm 6")
                safe_name = sanitize_filename(text, f"{base_name}_r{row}_c{col}")
            else:
                safe_name = f"{base_name}_r{row}_c{col}"

            output_path = os.path.join(OUTPUT_FOLDER, f"{safe_name}.png")
            tile.save(output_path)
