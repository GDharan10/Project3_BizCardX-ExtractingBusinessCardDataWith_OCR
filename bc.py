# Package
# File: image_processing.py
import easyocr
from PIL import Image
import re
# File: database.py
import pandas as pd
from sqlalchemy import create_engine
# File: app.py
import os
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
#from image_processing import extract_text, process_text
#from database import store_data

import io
import cv2
import matplotlib.pyplot as plt

# Create a database engine
engine = create_engine("postgresql+psycopg2://postgres:1005@localhost/bizcardx_data")

# Create a connection
conn = engine.connect()

def extract_text(image_path):
    reader = easyocr.Reader(['en'], gpu=False)
    image = Image.open(image_path).convert('RGB')
    # Extracting text from image
    details = reader.readtext(image_path, detail=0)
    return details

def process_text(details):
    data = {
        "name": "",
        "designation": "",
        "contact": [],
        "email": "",
        "website": "",
        "street": "",
        "city": "",
        "state": "",
        "pincode": "",
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
            data["name"] = details[i]
        elif i == 1:
            data["designation"] = details[i]
        elif '-' in details[i]:
            data["contact"].append(details[i])
        elif '@' in details[i]:
            data["email"] = details[i]
        elif "www " in details[i].lower() or "www." in details[i].lower():
            data["website"] = details[i]
        elif "WWW" in details[i]:
            data["website"] = details[i] + "." + details[i+1]
        elif match6:
            pass
        elif match1:
            data["street"] = match1[0][0]
            data["city"] = match1[0][1]
            data["state"] = match1[0][2]
        elif match2:
            data["street"] = match2[0][0]
            data["city"] = match2[0][1]
        elif match3:
            data["city"] = match3[0]
        elif match4:
            data["state"] = match4[0][0]
            data["pincode"] = match4[0][1]
        elif match5:
            data["street"] = match5[0] + ' St,'
        elif match7:
            data["pincode"] = match7[0]
        else:
            data["company"].append(details[i])

    data["contact"] = " & ".join(data["contact"])
    # Join company names with comma and space
    data["company"] = " ".join(data["company"])
    return data


def store_data(data):
    # Converting dictionary to DataFrame
    df = pd.DataFrame([data]) # Wrap data in a list to create DataFrame
    # Storing DataFrame in SQL table
    df.to_sql('business_card', engine, if_exists='append', index=False)
    return df


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
                
                if uploaded_file is not None:
                    image_path = os.getcwd()+ "\\"+"Business Cards"+"\\"+ uploaded_file.name
                    image = Image.open(image_path)
                    col3.image(image)
                    path = True

                    extract = st.button("Extract")
                              
                    upload = st.button("Upload")
                    if upload:
                        if path:
                            image_details = extract_text(image_path)
                            processed_details = process_text(image_details)
                            df = store_data(processed_details)
                            st.write(df)
                            st.success("Uploaded successfully")


            with col4:
                    st.write('')
                    st.write('')
                    st.info(f'''i) Kindly upload the image in JPG, PNG, or JPEG format.       
                            ii) Click the "**Extract and Upload**" button to extract text from the image and upload the extracted text details to the database.''', icon="ℹ️")
                    if path:
                        if extract:
                            image_details = extract_text(image_path)
                            processed_details = process_text(image_details)
                            st.write('**Name** :', processed_details['name'])
                            st.write('**Designation** :', processed_details['designation'])
                            st.write('**Company Name** :', processed_details['company'])
                            st.write('**Contact Number** :', processed_details['contact'])
                            st.write('**E-mail** :', processed_details['email'])
                            st.write('**Website** :', processed_details['website'])
                            st.write('**Street** :', processed_details['street'])
                            st.write('**City** :', processed_details['city'])
                            st.write('**State** :', processed_details['state'])
                            st.write('**Pincode** :', processed_details['pincode'])

    if menu == 'Database':
        # Read data from the 'business_card' table into a DataFrame
        df = pd.read_sql('business_card', engine)
        st.header("Database")                    
        st.dataframe(df)
        st.button('Show Changes')

        if Database_menu == 'Modify':
            modify_col,display = st.columns([1,1])
            with modify_col:
                names= ['','name','designation','email','company_name']
                selected = st.selectbox('**Select Categories**',names)
                if selected != '':
                        select = df[selected]
                        select_detail = st.selectbox('**Select Details**', select)
                        st.header('Select the modify details')
                        df1 = df[df[selected] == select_detail]
                        df1 = df1.reset_index()
                        select_modify = st.selectbox('**Select categories**', df.columns)
                        a = df1[select_modify][0]            
                        st.write(f'Do you want to change {select_modify}: **{a}** ?')
                        modified = st.text_input(f'**Enter the {select_modify}**')
                        if modified:
                            st.write(f'{select_modify} **{a}** changed as **{modified}**')
                        if st.button("Commit Changes"):
                            # Define the update statement
                            update_statement = f"UPDATE bizcardx_data SET {select_modify} = '{modified}' WHERE {selected} = '{select_detail}'"

                            try:
                                # Execute the update statement directly
                                with engine.connect() as conn:
                                    conn.execute(update_statement)
                                st.success("Data successfully updated ✅")
                            except Exception as e:
                                # Handle exceptions
                                st.error(f"Error updating data: {e}")

