import pytesseract
from typing import List

def extract_text_from_pdf(images: List):
    full_text = ""
    config = "--oem 3 --psm 6"  # оптимальный режим
    for img in images[:2]:  # максимум 2 страницы
        text = pytesseract.image_to_string(img, lang="rus+eng", config=config)
        full_text += text + "\n"
    return full_text.strip()
