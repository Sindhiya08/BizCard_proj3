
import streamlit as st
import pandas as pd
import easyocr as ocr
from PIL import Image
import numpy as np
import sqlite3
import re

db = sqlite3.connect("OCR.db")
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Data (id INTEGER PRIMARY KEY AUTOINCREMENT, image BLOB, Brand Name varchar(255),Name_Designation varchar(255),Contact Number integer,Email varchar(255),Website varchar(255),Address varchar(255))")

st.title("Business Card Extraction using OCR")
image = st.file_uploader(label="Upload Your Image", type=("jpg", "png", "jpeg"), accept_multiple_files=True)

if image:
    @st.cache_data
    def load():
        reader = ocr.Reader(['en'], gpu=True)
        return reader

    reader = load()

    if image is not None:
        for img in image:
            input = Image.open(img)
            st.image(img, caption='Uploaded Image', use_column_width='auto')
            res = reader.readtext(np.array(input))
            st.subheader("Extracted Data")
            data = []
            for text in res:
                data.append({'Text': text[1]})
            df = pd.DataFrame(data,columns=['Extracted Data'])

            st.experimental_data_editor(df)
            
            brandname=""
            name = ""
            phone = ""
            website = ""
            email = ""
            address = ""

            for cndtn in data:
              if re.search(r'(^[A-Za-z\s]+$)',data):
                name= cndtn.strip()
              elif re.search('(^[A-z].+[@]\w+[.][A-z])',data):
                email= cndtn.strip()
              elif re.search('(^www.+[A-z]+[.][A-z])',data):
                website=cndtn.strip()
              elif re.search('(^[+]|[0-9]+\d[-]*\d$)',data):
                contact=cndtn.strip()
              elif re.search('(^/d+[A-z].+\d{6}$)',data):
                address=cndtn.strip()
              else:
                brand=cndtn.strip()
              dict_data = {'Brand Name':[brandname],
                         'Name & Designation': [name],
                         'Contact Number': [contact],
                         'Email': [email],
                         'Website': [website],
                         'Address': [address]}

              extr_data=pd.DataFrame(dict_data)

              st.experimental_data_editor(extr_data)


              st.success("Successfully extracted the text data from the business card image", icon="✅")

              store = st.button("Click here to save the data")
              if store:
                try:
                    ins_query = "INSERT INTO Data (image,Brand Name,Name_Designation,Contact Number,Email,Website,Address)VALUES (?,?,?,?,?,?,?)"
                    val = (sqlite3.Binary(input.tobytes()), extr_data)
                    cur.execute(ins_query, val)
                    st.info("Data stored successfully")
                except Exception as e:
                    st.error(f"An error occurred while storing the data: {e}")

              update = st.button("Click here to update the data")
              if update:
                row_id = st.text_input("Enter the ID of the row to be updated:")
                new_text_data = st.text_input("Enter the new value of the text_data column:")
                cur.execute("UPDATE Data SET text_data = ? WHERE id = ?", (new_text_data, row_id))
                st.info("Updated successfully")

              delete = st.button("Click here to delete the data stored")
              if delete:
                cur.execute("DELETE FROM Data")
                st.info("Deleted successfully")