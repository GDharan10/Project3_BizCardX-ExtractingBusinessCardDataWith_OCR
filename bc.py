# Package
import easyocr


# Reading image using easy ocr
reader = easyocr.Reader(['en'], gpu=False)
image_path = "C:\\GD\\Notes\\DS Class\\DTM15\\Project\\Guvi project\\3 BizCardX Extracting Business Card Data with OCR\\Business Cards\\1.png"
image_data = reader.readtext(image_path, detail = 0)