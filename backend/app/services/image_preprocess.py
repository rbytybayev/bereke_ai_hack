import fitz  # PyMuPDF
import cv2
import numpy as np

def preprocess_pdf(filepath: str):
    doc = fitz.open(filepath)
    images = []

    for page in doc:
        pix = page.get_pixmap(dpi=150)  # ↓ DPI для ускорения
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, binarized = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
        images.append(binarized)

    return images
