import os
import cv2
import pytesseract
from PIL import Image
from pdf2image import convert_from_path


def preprocess_image(image_path: str) -> str:
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Görsel okunamadı.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    threshold = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    processed_path = image_path.replace(".", "_processed.")
    cv2.imwrite(processed_path, threshold)

    return processed_path


def image_to_text(image_path: str, lang: str = "tur+eng") -> str:
    processed_path = preprocess_image(image_path)
    text = pytesseract.image_to_string(Image.open(processed_path), lang=lang)
    return text


def pdf_to_text(pdf_path: str, lang: str = "tur+eng") -> str:
    pages = convert_from_path(pdf_path, dpi=200)
    full_text = ""

    for index, page in enumerate(pages):
        image_path = f"{pdf_path}_page_{index + 1}.png"
        page.save(image_path, "PNG")

        page_text = image_to_text(image_path, lang=lang)
        full_text += page_text + "\n"

    return full_text


def extract_text(file_path: str) -> str:
    extension = os.path.splitext(file_path)[1].lower()

    if extension in [".png", ".jpg", ".jpeg"]:
        return image_to_text(file_path)

    if extension == ".pdf":
        return pdf_to_text(file_path)

    return "Desteklenmeyen dosya türü."
