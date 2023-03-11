import streamlit as st
import pandas as pd
import easyocr as ocr
from PIL import Image
import numpy as np
import sqlite3
db = sqlite3.connect("OCR.db")
cur= db.cursor()
cur.execute ("Create table if not exists Data (id integer auto_increment primary key,data varchar(255))")

st.title("Business Card Extraction using OCR")
img=st.file_uploader(label="Upload Your Image",type=("jpg","png","jpeg"))
if img:
	@st.cache_data
	def load():
		reader=ocr.Reader(['en'],gpu=True)
		return reader

	reader= load()
	if img is not None:
		input=Image.open(img)
		st.image(img, caption='Uploaded Image', use_column_width='auto')
		res= reader.readtext(np.array(input))
		st.subheader("Extracted Data")
		for text in res:
			st.text_area("Data Extracted",text[1],label_visibility="hidden")
	else:
		st.write("No image uploaded,Please upload the image to extract")
	st.success("Sucessfully extracted the text data from the business card image",icon="✅")
	store= st.button("Click here to save the data")
	if store:
		ins_query= "Insert into Data (data) values(?)"
		val=(text[1],)
		cur.execute(ins_query,val)
		st.info(" Data stored sucessfully")
	#Update=st.button("Click here to Update the data ")
	#if Update:
		#cur.execute("Update Data")
		#st.write("Updated Sucessfully")
	delete= st.button("Click here if you want to delete the data stored")
	if delete:
		cur.execute("Delete from Data")
		st.info("Deleted Sucessfully")
