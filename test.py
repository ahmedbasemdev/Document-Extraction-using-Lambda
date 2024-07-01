from document_extractor import extract_document
from PIL import Image
import time


start_time = time.time()
document = extract_document("IMG_7059.jpg", "1.png")
print(f"Taken time is {time.time() - start_time}")