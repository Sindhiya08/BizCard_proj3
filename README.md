https://user-images.githubusercontent.com/118071774/224509347-b33fadf1-57e1-4cd0-be19-4592293fc46f.mp4




# Business Card Data Extraction using OCR


Import all the required libraries --> streamlit, pandas, easyocr, PIL, numpy, and sqlite3

Create connection to DB with sqlite3 and a cursor object is created to execute SQL queries.

The Streamlit UI is created with a title and a file uploader that accepts images in JPG, PNG, or JPEG format.

If an image is uploaded, the OCR reader is loaded using the easyocr library, and the uploaded image is opened and displayed using the PIL library. Then, the OCR reader extracts text data from the image, and the extracted data is displayed in a Pandas DataFrame using the pandas library.

If the user clicks on the "Click here to save the data" button, the extracted data is stored in the SQLite database with the INSERT SQL query.

If the user clicks on the "Click here to update the data" button, a text input is provided for the user to enter the row ID and the new value of the text_data column to be updated. The UPDATE SQL query is then executed to update the row with the new value.

If the user clicks on the "Click here to delete the data stored" button, the DELETE SQL query is executed to delete all the rows from the Data table in the database.
