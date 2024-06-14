from document_extractor import extract_document
from PIL import Image
import time

image = Image.open("image.jpg")

image.save('image.jpg', "JPEG", quality=50)


start_time = time.time()
document = extract_document("image.jpg", "ss.png")
print(f"Taken time is {time.time() - start_time}")