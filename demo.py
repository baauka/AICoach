import streamlit as st
import cv2
import mediapipe as mp
from streamlit_option_menu import option_menu
import time
import sqlite3
import pandas as pd 
import subprocess
import numpy as np
import pickle
from interface import *
from calorie_calculator import *
from database import *
from datetime import datetime, timedelta

from faker import Faker
import random


def stream_data():
    sentences = total_calorie.split('.')
    for sentence in sentences:
        words = sentence.split(" ")
        for word in words:
            yield word + " "
            time.sleep(0.02)
        yield "\n" 


if 'logged_or_registered' not in st.session_state:
    st.session_state.logged_or_registered = False
if 'global_email' not in st.session_state:
    st.session_state.global_email = None


database_start()

st.markdown(page_bg_img, unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",  # required
        options=['About', 'Login Page',
                 'Account Info',
                 'Calorie Calculator', 'AI Coach'],  # required
        icons=['info-circle', 'box-arrow-in-right', 'person-circle', 'prescription2',
               'clipboard2-heart-fill'],  # optional
        menu_icon='cast',  # optional
        default_index=1,  # optional
    )

if selected == 'About':
    st.markdown("<h1 style='text-align: center;'>About the <span style='color: #7F00FF;'>Program</span></h1>",
                unsafe_allow_html=True)
    st.write(info_string, unsafe_allow_html=True)

#-----------------------------------------------------------------------------------------------------------------------------------

if selected == 'Login Page':

    if st.session_state.global_email is None:
        try:
            with open('login_page.py') as f:
                code = f.read()
                exec(code, globals())
        except Exception as e:
            st.error(f"An error occurred while running login_page.py: {e}") 
    else:
        st.markdown(login_page_else_string, unsafe_allow_html=True)
        
#------------------------------------------------------------------------------------------------------------------------------
if selected == 'Account Info':
    if st.session_state.logged_or_registered:
        try:
            with open('account_info.py') as f:
                code = f.read()
                exec(code, globals())
        except Exception as e:
            st.error(f"An error occurred while running account_info.py: {e}") 
    else:
        st.markdown(account_info_page_else_string, unsafe_allow_html=True)

#------------------------------------------------------------------------------------------------------------------------------

if selected == 'Calorie Calculator':
    
    st.markdown("<h1 style='text-align: center;'>Welcome to your <span style='color: #7F00FF;'>calories calculator!</span></h1>", unsafe_allow_html=True)
    age = st.text_input(
        '**Age(Between 15-80)**',
        placeholder='Enter your age',
        value=None
    )
    gender = st.selectbox(
        "**Gender**",
        ("Male", "Female"),
        index=None,
        placeholder='Select gender')
    height = st.text_input(
        '**Height(cm)**',
        placeholder='Enter your height',
        value=None
    )
    weight = st.text_input(
        '**Weight(kg)**',
        placeholder='Enter your weight',
        value=None
    )
    activity = st.selectbox(
        "**Activity**",
        ("Sedentary(little or no exercise)", "Light(light exercise/sports 1-3 days​/week)",
            "Moderate(moderate exercise/sports 3-5 days/week)", "Active(hard exercise/sports 6-7 days a week)"),
        index=None,
        placeholder='Select activity')

    is_submitted = st.button("Calculate")

    all_filled_in = (age is not None) and (gender is not None) and (
        height is not None) and (weight is not None) and (activity is not None)

    if is_submitted and all_filled_in:
        bmr = calculate_bmr(gender, float(weight), float(height), int(age))
        total_calorie = total_calculation_calorie(bmr, activity)
        st.write_stream(stream_data)
    elif is_submitted and (not all_filled_in):
        st.error('Please, fill in all the information needed')

#-------------------------------------------------------------------------------------------------------------------------------
if selected == 'AI Coach':
    if st.session_state.logged_or_registered:
        try:
            with open('ai_coach.py') as f:
                code = f.read()
                exec(code, globals())
        except Exception as e:
            st.error(f"An error occurred while running ai_coach.py: {e}")            
    else:
        st.markdown(ai_coach_else_string, unsafe_allow_html=True)
