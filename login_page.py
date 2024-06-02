import streamlit as st
from database import *
import time

st.markdown("<h1 style='text-align: center;'>Welcome to<span style='color: #7F00FF;'>Login Page</span></h1>",
                    unsafe_allow_html=True)
        

choice = st.selectbox('**Login/SignUp**', ['Login', 'Sign Up'])


if choice == 'Login':
    email = st.text_input('**Email Address**', value=None)
    password = st.text_input('**Password**', type='password', value=None)

    login = st.button('Login')
    login_filled_in = (email is not None) and (password is not None)

    if login:
        if login_filled_in:
            is_right = check_correctness_of_login(email,password)
            if is_right:
                st.write("Welcome to the account Sir")
                st.session_state.global_email = email
                st.session_state.logged_or_registered = True
                st.experimental_rerun()
            else:
                st.error("Email or Password was written wrong")
        else:
            st.error("Please fill in all the information needed")
else:
    email = st.text_input('**Email Address**', value=None)
    password = st.text_input('**Password**', type='password', value=None)
    username = st.text_input('**Enter your unique username**', value=None)

    email_valid = email and (email.endswith('@gmail.com') or email.endswith('@mail.ru'))
    password_valid = password and len(password) >= 6
    username_valid = username and len(username) >= 6

    registration_filled_in = (email is not None) and (password is not None) and (username is not None)
    all_valid = email_valid and password_valid and username_valid
    
    email_error = st.empty()
    password_error = st.empty()
    username_error = st.empty()

    if email and not email_valid:
        email_error.error("Email should end with @gmail.com or @mail.ru")
    if password and not password_valid:
        password_error.error("Password should be at least 6 characters long")
    if username and not username_valid:
        username_error.error("Username should be at least 6 characters long")
    

    button = st.button('Create Account')
    if button:
        if not registration_filled_in:
            st.error("Please fill in all the information")
        else:
            with st.spinner("Creating an account..."):
                time.sleep(1)
                registered = insert_patient_info(email,password,username)
                if registered:
                    st.success('Successfully registered')
                    st.session_state.global_email = email
                    st.session_state.logged_or_registered = True
                    st.experimental_rerun()