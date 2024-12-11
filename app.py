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
import mysql.connector
EXAMPLE_NO=1
username = 'root'
password = '1234'
host = 'localhost'
database = 'profiles'

def connect_to_mysql():
    try:
        cnx = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )
        return cnx
    except mysql.connector.Error as err:
        st.error(f"Error connecting to MySQL database: {err}")
        return None

def execute_query(query):
    cnx = connect_to_mysql()
    if cnx:
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cnx.commit()  # Commit the changes to the database
        cursor.close()
        cnx.close()
        return result
    else:
        st.warning("Failed to add data to the database.")
    
def list_profiles(column_name):
    query = f"SELECT name, {column_name} FROM user_profiles WHERE {column_name} IS NOT NULL"
    cnx = connect_to_mysql()
    ans=execute_query(query)
    user_data = {}
    for name, leetcode_username in ans:
        user_data[name] = leetcode_username
    return user_data
def get_leetcode_data(username):
    url = "https://leetcode.com/graphql"
    query = """
    query getLeetCodeData($username: String!) {
      userProfile: matchedUser(username: $username) {
        username
        profile {
          userAvatar
          reputation
          ranking
        }
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
          totalSubmissionNum {
            difficulty
            count
          }
        }
      }
      userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
        totalParticipants
        topPercentage
      }
      recentSubmissionList(username: $username) {
        title
        statusDisplay
        lang
      }
      matchedUser(username: $username) {
        languageProblemCount {
          languageName
          problemsSolved
        }
      }
      recentAcSubmissionList(username: $username, limit: 15) {
            id
            title
            titleSlug
            timestamp
          }
     
    }
    
    """
    variables = {
        "username": username
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()

    if 'errors' in data:
        print("Error:", data['errors'])
        return None

    return data['data']
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
    selected = streamlit_menu(example=EXAMPLE_NO)
if selected=="Register":
    st.title("If You Are New")
    st.write("Please fill in the following details to save your data ")    
    name = st.text_input("Enter your name")
    leetcode_username = st.text_input("Enter your LeetCode username")
    codechef_username = st.text_input("Enter your CodeChef username ")
    github_username = st.text_input("Enter your GitHub username")
    codeforces_username = st.text_input("Enter your CodeForces username")
    if st.button("Save Data"):
        insert_query = f"""
            INSERT INTO user_profiles (name, leetcode_username, codechef_username, github_username, codeforces_username)
            VALUES ('{name}', '{leetcode_username}', '{codechef_username}', '{github_username}', '{codeforces_username}')
        """
        execute_query(insert_query)
    st.title("Data from Excel")
if selected == "Leet-code":
    st.title("Compare with your friend")
    ans=list_profiles("leetcode_username")
    st.write(ans)

    your_id = st.multiselect("What is your ?", ans.keys(), [], placeholder="Select Your's Id")    
    fireds_id= st.multiselect("What is your ?", ans.keys(), [], placeholder="Friend's Id")
    #st.write(ans[your_id[0]])
    data = get_leetcode_data(ans[your_id[0]])
    data2 = get_leetcode_data(ans[fireds_id[0]])
    
    st.write(data)
    st.write(data2)
    


if selected=="codechef":
    pass
if selected == "Git-Hub":
    pass
if selected == "CodeForces":
    pass


