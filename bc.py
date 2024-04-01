# Package
import easyocr
from PIL import Image
import io
import re
import pandas as pd
from sqlalchemy import create_engine 

engine = create_engine("postgresql+psycopg2://postgres:1005@localhost/bizcardx_data")

# Reading image using easy ocr
reader = easyocr.Reader(['en'], gpu=False)
image_path = "C:\\GD\\Notes\\DS Class\\DTM15\\Project\\Guvi project\\3 BizCardX Extracting Business Card Data with OCR\\Business Cards\\1.png"
# Extracting text from image
image_data = reader.readtext(image_path, detail = 0)
# Load the image
image = Image.open(image_path)
# Convert RGBA image to RGB
image = image.convert('RGB')


# Convert the image to binary data
def img_to_binary(image):
    image_binary = io.BytesIO()
    image.save(image_binary, format='JPEG')
    image_binary = image_binary.getvalue()
    return image_binary

def extracted_text(details):
    data = {
        "name": [],
        "designation": [],
        "contact": [],
        "email": [],
        "website": [],
        "street": [],
        "city": [],
        "state": [],
        "pincode": [],
        "company": [],
        "image" : img_to_binary(image)
    }
    
    for i in range(len(details)):
        match1 = re.findall('([0-9]+ [A-Z]+ [A-Za-z]+)., ([a-zA-Z]+). ([a-zA-Z]+)', details[i])
        match2 = re.findall('([0-9]+ [A-Z]+ [A-Za-z]+)., ([a-zA-Z]+)', details[i])
        match3 = re.findall('^[E].+[a-z]', details[i])
        match4 = re.findall('([A-Za-z]+) ([0-9]+)', details[i])
        match5 = re.findall('([0-9]+ [a-zA-z]+)', details[i])
        match6 = re.findall('.com$', details[i])
        match7 = re.findall('([0-9]+)', details[i])
        if i == 0:
            data["name"].append(details[i])
        elif i == 1:
            data["designation"].append(details[i])
        elif '-' in details[i]:
            data["contact"].append(details[i])
        elif '@' in details[i]:
            data["email"].append(details[i])
        elif "www " in details[i].lower() or "www." in details[i].lower():
            data["website"].append(details[i])
        elif "WWW" in details[i]:
            data["website"].append(details[i] + "." + details[i+1])
        elif match6:
            pass
        elif match1:
            data["street"].append(match1[0][0])
            data["city"].append(match1[0][1])
            data["state"].append(match1[0][2])
        elif match2:
            data["street"].append(match2[0][0])
            data["city"].append(match2[0][1])
        elif match3:
            data["city"].append(match3[0])
        elif match4:
            data["state"].append(match4[0][0])
            data["pincode"].append(match4[0][1])
        elif match5:
            data["street"].append(match5[0] + ' St,')
        elif match7:
            data["pincode"].append(match7[0])
        else:
            data["company"].append(details[i])
    
    data["contact"] = [" & ".join(data["contact"])]
    # Join company names with space
    data["company"] = [" ".join(data["company"])]
    return data

# converting to dictionary
data = extracted_text(image_data)
# Converting dictionary to DataFrame
df = pd.DataFrame(data)
# Storing DataFrame in SQL table
df.to_sql('business_card', engine, if_exists='append', index=False)


