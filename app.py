from pathlib import Path
import speech_recognition as sr
import pdf2image
import gtts
import pandas as pd
import json
import traceback
from dotenv import load_dotenv
import streamlit as st
from streamlit_ace import st_ace
from PIL import Image
import base64
import streamlit as st
from streamlit_extras.let_it_rain import rain
from tempfile import NamedTemporaryFile
from streamlit_option_menu import option_menu
from streamlit_extras.mandatory_date_range import date_range_picker
import datetime
import os
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from streamlit_lottie import st_lottie
import requests 
import sys
import io
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from youtube_transcript_api import YouTubeTranscriptApi
import time
EXAMPLE_NO=1
def streamlit_menu(example=1):
    if example == 1:
        with st.sidebar:
            selected = option_menu(
                
                menu_title="Knowledge Builder🧠",  # required
                options=["Register","Leet-code","Git-Hub","Codechef","CodeForces"],  # required
                icons=["geo-alt-fill","bi bi-camera-video-fill","bi bi-code-slash"],  # optional
                menu_icon="cast",  # optional
                default_index=0,
            )
        return selected
def data():
    df = pd.read_excel('profiles/profile_data.xlsx')
    column_names = df.columns.tolist()
    data_dict = {}
    for column in column_names:
        data_dict[column] = df[column].tolist()
    for column, data_list in data_dict.items():
        return  data_list
    

selected = streamlit_menu(example=EXAMPLE_NO)




if selected=="Register":

    st.title("If You Are New")
    st.write("Please fill in the following details to save your data ")    
    name = st.text_input("Enter your name")
    leetcode_username = st.text_input("Enter your LeetCode username")
    codechef_username = st.text_input("Enter your CodeChef username ")
    github_username = st.text_input("Enter your GitHub username")
    codeforces_username = st.text_input("Enter your CodeForces username")

    # Create a DataFrame to store the data
    data = {
            'Name': [name],
            'LeetCode Username': [leetcode_username],
            'CodeChef Username': [codechef_username],
            'GitHub Username': [github_username],
            'CodeForces Username': [codeforces_username]
        }
    df = pd.DataFrame(data)

    # Button to trigger data saving
    if st.button("Save Data"):
            if not os.path.exists('profiles'):
                os.makedirs('profiles')
            file_path = os.path.join('profiles', 'profile_data.xlsx')
            if os.path.exists(file_path):
                existing_df = pd.read_excel(file_path)
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                combined_df.to_excel(file_path, index=False)
            else:
                df.to_excel(file_path, index=False)
        
            st.success("Data saved to Excel file successfully!")


    st.title("Data from Excel")
if selected == "Leet-code":
    pass
if selected=="codechef":
    pass
if selected == "Git-Hub":
    pass
if selected == "CodeForces":
    pass


