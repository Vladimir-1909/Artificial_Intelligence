import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
from pytesseract import image_to_string # С изображения в текст

text = image_to_string(Image.open('text-ru.png'), lang="rus") # default = eng
print(text)