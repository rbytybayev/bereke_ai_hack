import pytesseract
import cv2
from typing import List


def extract_text_from_pdf(images: List):
    full_text = ""
    for img in images:
        text = pytesseract.image_to_string(img, lang="rus+eng")
        full_text += text + "\n"
    return full_text.strip()
