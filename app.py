import streamlit as st
from PIL import Image
import pandas as pd
from channel_detail import *
from create_table import *
from query import *

st.title("ETL Project ")

image = Image.open('youtube_selects_2.jpg')

st.image(image, caption='youtube scraping')

chan_id = st.sidebar.text_input("Enter channel id")

st.write("The YouTube API and integrating it with Streamlit, i build a powerful tool to scrape data from YouTube and extract valuable insights. ")

st.write("YouTube, being the world's largest video-sharing platform, offers a vast amount of valuable data."
         "By leveraging the YouTube API and integrating it with Streamlit, a popular Python library for building interactive web applications, we can create a powerful tool for scraping data from YouTube and extracting useful information.")

v = "UCKZozRVHRYsYHGEyNKuhhdA"
def view_collections():
    st.sidebar.write(f"The database contains the following collections: {db.list_collection_names()}")


    
channel_ids =f"{chan_id}"
              



if st.sidebar.button("Data getting"):
    a = get_data(channel_ids)
    st.write(a)
    st.success("Data fetched successfully.")

if st.sidebar.button("Data moving to MongoDB database"):
    a = get_data(channel_ids)
    collection.insert_one(a)
    st.success("Data inserted successfully.")
    view_collections()

if st.sidebar.button("Migrate data to SQL"):
    migrate_data()
    st.success("Data migrated successfully.")

query_option = st.sidebar.selectbox("Select a query:", list(queries.keys()))
if st.sidebar.button("Run Query"):
    query = queries[query_option]
    df = pd.read_sql_query(query, mydb)
    st.dataframe(df)
    
    



        




    

