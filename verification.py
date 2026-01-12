import smtplib
from email.mime.text import MIMEText
from random import randint
import time
import streamlit as st

# --------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = st.secrets["SENDER_EMAIL"]      # Replace with your Gmail
SENDER_APP_PASSWORD = st.secrets["SENDER_APP_PASSWORD"]
USERS = st.secrets["USERS"]

def send_otp(email, otp):
    """Send OTP via Gmail SMTP"""
    msg = MIMEText(f"Your OTP code is: {otp}")
    msg['Subject'] = 'Your Streamlit App OTP'
    msg['From'] = SENDER_EMAIL
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Failed to send OTP: {e}")
        return False
    

def generate_otp():
    otp = f"{randint(0, 999999):06d}"  # always 6 digits, string
    st.session_state.otp = otp
    return otp