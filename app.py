import streamlit as st
import pandas as pd
from datetime import datetime
st.set_page_config(page_title="Lshi Trust", page_icon="💰", layout="centered")
CODE_PATRON = "LSHI2026"
AIRTEL_NUM = "0999783612"
AIRTEL_NOM = "Enock Kapalu"
if "users" not in st.session_state:
    st.session_state.users = {}
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "is_patron" not in st.session_state:
    st.session_state.is_patron = False
if "trans" not in st.session_state:
    st.session_state.trans = []
st.title("💰 Lshi Trust")
st.caption("Micro-epargne Lubumbashi - Airtel Money " + AIRTEL_NUM)
st.divider()
if st.session_state.current_user:
    u = st.session_state.users[st.session_state.current_user
