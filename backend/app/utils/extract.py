# app/utils/extract.py

import pdfplumber
import pytesseract
from langdetect import detect

def extract_text(path: str) -> str:
    """
    Извлекает текст через pdfplumber, для пустых страниц — OCR с автодетектом языка.
    """
    text_chunks = []
    detected_lang = None

    with pdfplumber.open(path) as pdf:
        # 1) Сначала определяем язык по первой странице с текстом
        for page in pdf.pages:
            sample = page.extract_text() or ""
            if sample.strip():
                detected_lang = detect(sample)
                break

        # Маппинг langdetect → tesseract-коды
        lang_map = {
            "ru": "rus",
            "en": "eng",
            "kk": "kaz",
        }
        # по умолчанию все три
        default_langs = "+".join(lang_map.values())

        # 2) Обрабатываем каждую страницу
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_chunks.append(page_text)
            else:
                # выбираем код для OCR
                tesseract_lang = (
                    lang_map.get(detected_lang, default_langs)
                )
                img = page.to_image(resolution=300).original
                ocr_text = pytesseract.image_to_string(img, lang=tesseract_lang)
                text_chunks.append(ocr_text or "")

    return "\n\n".join(text_chunks)
