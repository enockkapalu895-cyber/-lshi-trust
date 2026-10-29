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
if "transactions" not in st.session_state:
    st.session_state.transactions = []

st.title("💰 Lshi Trust")
st.markdown("<p style='text-align:center;color:#888;'>Micro-épargne - Lubumbashi</p>", unsafe_allow_html=True)
st.write("---")

if st.session_state.current_user:
    user = st.session_state.users[st.session_state.current_user]
    st.header(f"Salut {user['nom']} 👋")
    c1,c2,c3 = st.columns(3)
    c1.metric("Épargne $", f"{user.get('solde_usd',0)} $")
    c2.metric("Épargne FC", f"{user.get('solde_fc',0):,} FC")
    c3.metric("Commune", user['commune'])
    
    st.write("---")
    st.subheader("💳 Faire un dépôt Airtel Money")
    st.info(f"**Envoie sur:**\n\n📱 **{AIRTEL_NUM}**\n\n👤 Nom: **{AIRTEL_NOM}**\n\nAprès l'envoi, clique ci-dessous")
    with st.form("depot"):
        d_devise = st.selectbox("Tu as envoyé en", ["USD ($)", "CDF (FC)"])
        d_montant = st.number_input("Montant envoyé", 1, 10000000, 10)
        d_ref = st.text_input("Code transaction Airtel (optionnel)", placeholder="Ex: MP241029...")
        btn_d = st.form_submit_button("J'AI ENVOYÉ - Déclarer", use_container_width=True)
        if btn
