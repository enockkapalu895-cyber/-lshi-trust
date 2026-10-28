import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Lshi Trust", page_icon="💰", layout="centered")

if "users" not in st.session_state:
    st.session_state.users = []
if "epargnes" not in st.session_state:
    st.session_state.epargnes = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

CODE_PATRON = "Lshi2026"

def trouver_user(email):
    for u in st.session_state.users:
        if u["email"].lower() == email.lower():
            return u
    return None

if not st.session_state
