import cv2
import numpy as np
from typing import List

def detect_signature_presence(images: List[np.ndarray]) -> bool:
    """
    Простейшее эвристическое определение наличия подписи:
    - Анализ нижней части последней страницы
    - Поиск тёмных контуров определённой длины и изогнутости
    """
    if not images:
        return False

    img = images[-1]  # берём последнюю страницу
    height = img.shape[0]
    cropped = img[int(height * 0.75):]  # нижняя четверть страницы

    edges = cv2.Canny(cropped, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        length = cv2.arcLength(cnt, True)
        if 150 < length < 1000:  # подписи обычно ~200-800px
            approx = cv2.approxPolyDP(cnt, 0.02 * length, True)
            if len(approx) > 4:  # не просто прямоугольник
                return True

    return False
