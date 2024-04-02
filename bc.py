# Package
import easyocr
from PIL import Image
import io
import re
import pandas as pd
from sqlalchemy import create_engine 
import streamlit as st
from streamlit_option_menu import option_menu
import os
import cv2
import matplotlib.pyplot as plt

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
        "company": []
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

def store_data(data):
    # Converting dictionary to DataFrame
    df = pd.DataFrame(data)
    # Storing DataFrame in SQL table
    df.to_sql('business_card', engine, if_exists='append', index=False)



# Streamlit part
st.set_page_config(page_title= "BizCardX",
                   page_icon= '💼',
                   layout= "wide",)

text = 'BizCardX'   
st.markdown(f"<h2 style='color: white; text-align: center;'>{text} </h2>", unsafe_allow_html=True)

st.markdown(f""" <style>.stApp {{
                    background: url('https://img.freepik.com/free-vector/gradient-golden-luxury-business-card-template_23-2149035722.jpg?w=740&t=st=1712021022~exp=1712021622~hmac=af788945480688006d710a5bda024f6d2b87d50990c0edd91b1e0c7c4b205ddf');   
                    background-size: cover}}
                 </style>""",unsafe_allow_html=True)

col1,col2 = st.columns([1,4])
with col1:
    menu = option_menu("Menu", ["Home","Upload","Database"], 
                    icons=["house",'cloud-upload', "list-task"],
                    menu_icon="cast",
                    default_index=0,
                    styles={"icon": {"color": "orange", "font-size": "20px"},
                            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px", "--hover-color": "#FFFFFF"},
                            "nav-link-selected": {"background-color": "#225154"}})
    if menu == 'Upload':
        upload_menu = option_menu("Upload", ['Predefined','Undefined'],                        
                        menu_icon='cloud-upload',
                        default_index=0,
                        styles={"icon": {"color": "orange", "font-size": "20px"},
                                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px", "--hover-color": "#FFFFFF"},
                                "nav-link-selected": {"background-color": "#225154"}})
    
    if menu == 'Database':
        Database_menu = option_menu("Database", ['Modify','Delete'], 
                        
                        menu_icon="list-task",
                        default_index=0,
                        styles={"icon": {"color": "orange", "font-size": "20px"},
                                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#FFFFFF"},
                                "nav-link-selected": {"background-color": "#225154"}})



with col2:
    if menu == 'Home':
        col3,col4 = st.columns([3,2])
        with col3:
            st.header('Welcome to business card application')
            st.subheader(':orange[About the App:]')
            home_text = (f'''In this Streamlit web app, you can upload an image of a business 
                         card and extract relevant information from it using EasyOCR. You can view, 
                         modify, or delete the extracted data in this app. Additionally, the app would 
                         allow users to save the extracted information into a database alongside the 
                         uploaded business card image. The database would be capable of storing multiple 
                         entries, each with its own business card image and the extracted information.''')
                         
            st.markdown(f"<h4 text-align: left;'>{home_text} </h4>", unsafe_allow_html=True)
            st.subheader(":orange[Technologies Used:]")
            tech_text =('  EasyOCR, Python, SQL, Streamlit')
            st.markdown(f"<h4 text-align: left;'>{tech_text} </h4>", unsafe_allow_html=True)
        with col4:
            home_image = Image.open('C:\\GD\\Notes\\DS Class\\DTM15\\Project\\Guvi project\\3 BizCardX Extracting Business Card Data with OCR\\Business Cards\\blue.jpg')
            st.write('')
            st.write('')
            st.image(home_image)


    if menu == 'Upload':
        
        path = False
        if upload_menu == 'Predefined':
            col3,col4 = st.columns([2,2])
            with col3:
                uploaded_file = st.file_uploader("**Choose a file**", type=["jpg", "png", "jpeg"])
                extract = st.button("Extract and Upload")
                if uploaded_file is not None:
                    image_path = os.getcwd()+ "\\"+"Business Cards"+"\\"+ uploaded_file.name
                    image = Image.open(image_path)
                    col3.image(image)
                    path = True
            
            with col4:
                    st.write('')
                    st.write('')
                    st.info(f'''i) Kindly upload the image in JPG, PNG, or JPEG format.       
                            ii) Click the "**Extract and Upload**" button to extract text from the image and upload the extracted text details to the database.''', icon="ℹ️")
                    if path:                
                        image_details = extracted_text(image_path)
                        if extract:
                            img = cv2.imread(image_path)
                            reader = easyocr.Reader(['en'])
                            result = reader.readtext(image_path)
                            for detection in result:    
                                top_left =tuple([int(val) for val in detection[0][0]])
                                bottom_right =tuple([int(val) for val in detection[0][2]])
                                text = detection[1]
                                font =cv2.FONT_HERSHEY_SIMPLEX
                                img = cv2.rectangle(img, top_left, bottom_right, (0,255,0), 2)
                                img = cv2.putText(img, text, top_left, font, 1, (255,0,0),1, cv2.LINE_AA)
                                plt.figure(figsize=(20,20))
                                
                            st.write("")
                            st.write("")
                            st.subheader("Extracted Text")
                            st.image(img)            
                            
                        with col3:
                            if extract:
                                st.write('**Name** :',image_details['name'])
                                st.write('**Designation** :', image_details['designation'])
                                st.write('**Company Name** :', image_details['company'])
                                st.write('**Contact Number** :', image_details['contact'])
                                st.write('**E-mail** :', image_details['email'])
                        with col4:
                            if extract:
                                st.write('**Website** :', image_details['website'])
                                st.write('**Street** :', image_details['street'])
                                st.write('**City** :', image_details['city'])
                                st.write('**State** :', image_details['state'])
                                st.write('**Pincode** :', image_details['pincode'])
                                