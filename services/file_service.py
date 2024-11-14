import os
from pathlib import Path
# from paddleocr import PaddleOCR
from fastapi.responses import FileResponse
from typing import List
import cv2
import numpy as np
from easyocr import Reader

from config import UPLOAD_FOLDER


class OCRResponse:
    def __init__(self, text: List[str], confidence: List[float], file_link: str, highlighted_file_link: str):
        self.text = text
        self.confidence = confidence
        self.file_link = file_link
        self.highlighted_file_link = highlighted_file_link


# ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=True)
reader = Reader(['en'], gpu=False)


# def save_file(file):
#     file_name = file.filename
#     file_path = os.path.join(UPLOAD_FOLDER, file_name)

#     with open(file_path, 'wb') as f:
#         f.write(file.file.read())

#     result = ocr.ocr(file_path, cls=True)

#     if not result or not result[0]:
#         return OCRResponse(text=[], confidence=[], file_link=file_path, highlighted_file_link="")

#     texts = []
#     confidences = []
#     highlighted_image_path = os.path.join(
#         UPLOAD_FOLDER, f"highlighted_{file_name}")

#     image = cv2.imread(file_path)

#     for line in result[0]:
#         text, confidence = line[1]
#         texts.append(text)
#         confidences.append(float(confidence))

#         bbox = line[0]
#         pts = [(int(point[0]), int(point[1])) for point in bbox]

#         cv2.polylines(image, [np.array(pts)], isClosed=True,
#                       color=(0, 255, 0), thickness=2)

#     cv2.imwrite(highlighted_image_path, image)

#     return OCRResponse(
#         text=texts,
#         confidence=confidences,
#         file_link=file_path,
#         highlighted_file_link=highlighted_image_path
#     )


def save_file(file):
    file_name = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    with open(file_path, 'wb') as f:
        f.write(file.file.read())

    result = reader.readtext(file_path, detail=1)

    if not result:
        return OCRResponse(text=[], confidence=[], file_link=file_path, highlighted_file_link="")

    texts = []
    confidences = []
    highlighted_image_path = os.path.join(
        UPLOAD_FOLDER, f"highlighted_{file_name}")

    image = cv2.imread(file_path)

    for bbox, text, confidence in result:
        texts.append(text)
        confidences.append(float(confidence))

        pts = [(int(point[0]), int(point[1])) for point in bbox]

        cv2.polylines(image, [np.array(pts)], isClosed=True,
                      color=(0, 255, 0), thickness=2)

    cv2.imwrite(highlighted_image_path, image)

    return OCRResponse(
        text=texts,
        confidence=confidences,
        file_link=file_path,
        highlighted_file_link=highlighted_image_path
    )


def get_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return FileResponse(file_path, media_type='application/octet-stream', filename=filename)
