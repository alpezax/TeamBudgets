import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from dotenv import load_dotenv
import os

load_dotenv()

def authenticate():
    with open(os.getenv("AUTH_CONFIG_FILE", "config.yaml")) as file:
        config = yaml.load(file, Loader=SafeLoader)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    try:
        authenticator.login()
    except Exception as e:
        st.error(e)
        
    if st.session_state['authentication_status']:
        authenticator.logout()
        return True
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
        return False
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')
        return False