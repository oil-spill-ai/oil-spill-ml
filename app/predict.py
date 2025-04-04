# ml/app/predict.py
# ЗАГЛУШКА

import os
import cv2
import numpy as np

def predict_image(image_path: str) -> str:
    image = cv2.imread(image_path)

    # Заглушка маски
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    h, w = mask.shape
    cv2.circle(mask, (w//2, h//2), min(h, w)//4, 255, -1)

    result_path = image_path.replace(".jpg", "_mask.png")
    cv2.imwrite(result_path, mask)

    return result_path
