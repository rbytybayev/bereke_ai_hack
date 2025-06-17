import fitz  # PyMuPDF
import cv2
import numpy as np
import tempfile
import os


def preprocess_pdf(filepath: str):
    doc = fitz.open(filepath)
    processed_images = []

    for i in range(len(doc)):
        pix = doc[i].get_pixmap(dpi=300)
        image_bytes = pix.tobytes("png")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name

        img = cv2.imread(tmp_path, cv2.IMREAD_GRAYSCALE)
        os.unlink(tmp_path)

        img = cv2.fastNlMeansDenoising(img, None, 30, 7, 21)
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img = cv2.resize(img, (img.shape[1], img.shape[0]))  # ensure uniform size

        processed_images.append(img)

    return processed_images
