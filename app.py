import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="Lshi Trust", page_icon="💰", layout="centered")

ADMIN_PASSWORD = "Lshi2026"

if "epargnes" not in st.session_state:
    st.session_state.epargnes = []

st.title("Lshi Trust 💰")
st.subheader("Épargne sécurisée à Lubumbashi")

with st.sidebar:
    st.header("🔐 Espace Patron")
    code = st.text_input("Code Admin", type="password")
    is_admin = (code == ADMIN_PASSWORD)
    if is_admin:
        st.success("Bienvenue Patron Enock !")

if not is_admin:
    st.markdown("Bienvenue ! Épargne ici.")
    with st.form("client_form"):
        nom = st.text_input("Ton nom complet")
        montant = st.number_input("Montant (CDF)", min_value=5000, step=1000)
        duree = st.selectbox("Durée", ["2 semaines (Bonus 3%)", "1 mois (Bonus 5%)", "3 mois (Bonus 10%)"])
        btn = st.form_submit_button("💰 Épargner maintenant")
        if btn and nom and montant:
            pct = {"2 semaines (Bonus 3%)":0.03, "1 mois (Bonus 5%)":0.05, "3 mois (Bonus 10%)":0.10}[duree]
            jours = {"2 semaines (Bonus 3%)":14, "1 mois (Bonus 5%)":30, "3 mois (Bonus 10%)":90}[duree]
            total = int(montant * (1+pct))
            date_retour = datetime.now() + timedelta(days=jours)
            st.session_state.epargnes.append({"Nom":nom, "Montant":montant, "Total":total, "Retour":date_retour.strftime("%d/%m/%Y")})
            st.success(f"Merci {nom} ! Reçu {montant} CDF. Tu recevras {total} CDF le {date_retour.strftime('%d/%m/%Y')}")
else:
    st.header("📊 CAHIER DU PATRON - CONFIDENTIEL")
    if st.session_state.epargnes:
        df = pd.DataFrame(st.session_state.epargnes)
        st.dataframe(df, use_container_width=True)
        st.metric("Total épargné", f"{df['Montant'].sum()} CDF")
    else:
        st.info("Pas encore d'épargnes")
