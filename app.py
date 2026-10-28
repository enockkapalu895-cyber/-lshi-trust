import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

st.set_page_config(page_title="Lshi Trust", page_icon="💰", layout="centered")

# ===== CONFIGURATION PATRON - DEJA REMPLI POUR TOI =====
AIRTEL_NUMBER = "0999783612"
TRUST_WALLET_BTC = "bc1q4lha2csw8zk3p53lzlt7tlrw3ccjyxwxdeu48e"
PATRON_CODE = "Lshi2026"
BTC_PRICE_USD = 81000
USD_TO_CDF = 2850
# ======================================================

DATA_FILE = "lshi_data.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

st.markdown("<h1 style='text-align:center; color:#FF6B00;'>💰 Lshi Trust</h1><p style='text-align:center;'>Épargne sécurisée Lubumbashi - Convertie en Bitcoin</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["👤 Client", "📝 S'inscrire", "👑 Patron"])

with tab2:
    st.subheader("Créer compte client")
    with st.form("inscription"):
        nom = st.text_input("Nom complet")
        email = st.text_input("Email Gmail")
        whatsapp = st.text_input("WhatsApp")
        mdp = st.text_input("Mot de passe", type="password")
        mdp2 = st.text_input("Confirme mot de passe", type="password")
        if st.form_submit_button("S'inscrire"):
            if mdp == mdp2 and email:
                st.success(f"Compte cree {nom} !")
            else:
                st.error("Verifie mot de passe")

with tab1:
    st.subheader("Espace Client")
    email_login = st.text_input("Ton Email", key="login_email")
    mdp_login = st.text_input("Mot de passe", type="password", key="login_mdp")
    if st.button("Entrer"):
        st.session_state["client"] = email_login
        st.success(f"Bienvenue {email_login}")

    if "client" in st.session_state:
        st.divider()
        st.markdown("### 🔶 Étape 1 : Envoie l'argent sur Airtel Money")
        st.info(f"📱 Airtel Money : {AIRTEL_NUMBER}\nNom : Enock - Lshi Trust")
        st.warning("Apres envoi, copie l'ID de transaction")

        montant = st.number_input("Montant que tu as envoyé (CDF)", min_value=5000, step=1000)
        operateur = st.selectbox("Operateur", ["Airtel Money", "Orange Money", "M-Pesa"])
        tx_id = st.text_input("Colle ton ID de transaction Mobile Money")

        btc_estime = montant / USD_TO_CDF / BTC_PRICE_USD
        usd_estime = montant / USD_TO_CDF
        date_retour = (datetime.now()+timedelta(days=14)).strftime("%d/%m/%Y")

        st.markdown(f"Sera converti en : {btc_estime:.6f} BTC (~${usd_estime:.2f})")
        st.markdown(f"Tu recevras le {date_retour} : {montant*1.03:.0f} CDF (+3% benefice)")
        st.code(f"Adresse BTC Patron: {TRUST_WALLET_BTC}", language="text")

        if st.button("J'ai envoye, valider"):
            if not tx_id:
                st.error("Colle l'ID transaction !")
            else:
                data = load_data()
                data.append({
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "client": st.session_state["client"],
                    "montant_cdf": montant,
                    "btc": btc_estime,
                    "operateur": operateur,
                    "tx_id": tx_id,
                    "statut": "En attente - Airtel a verifier",
                    "converti_btc": False,
                    "date_retour": date_retour
                })
                save_data(data)
                st.success(f"Recu {montant} CDF ! En attente confirmation patron.")

        st.divider()
        st.subheader("Mes epargnes")
        data = load_data()
        mes = [d for d in data if d["client"] == st.session_state["client"]]
        if mes:
            st.dataframe(pd.DataFrame(mes))

with tab3:
    st.subheader("Cahier Patron")
    code = st.text_input("Code Patron", type="password")
    if code == PATRON_CODE:
        data = load_data()
        if not data:
            st.info("Aucune epargne")
        else:
            df = pd.DataFrame(data)
            total_cdf = df["montant_cdf"].sum()
            total_btc = df["btc"].sum()
            a_rendre = (df["montant_cdf"] * 1.03).sum()

            c1,c2,c3 = st.columns(3)
            c1.metric("Total collecte", f"{total_cdf:.0f} CDF")
            c2.metric("En BTC", f"{total_btc:.6f} BTC")
            c3.metric("A rendre +3%", f"{a_rendre:.0f} CDF")

            st.info(f"Airtel: {AIRTEL_NUMBER} | BTC: {TRUST_WALLET_BTC}")

            for i, row in enumerate(data):
                with st.expander(f"{row['client']} - {row['montant_cdf']} CDF - {row['statut']}"):
                    st.json(row)
                    col_a, col_b = st.columns(2)
                    if col_a.button(f"Confirmer Airtel recu {i}", key=f"conf{i}"):
                        data[i]["statut"] = "Confirme - En attente conversion BTC"
                        save_data(data)
                        st.rerun()
                    if col_b.button(f"Convertir en BTC Trust Wallet {i}", key=f"btc{i}"):
                        data[i]["converti_btc"] = True
                        data[i]["statut"] = f"Converti en {row['btc']:.6f} BTC - Trading en cours"
                        save_data(data)
                        st.success(f"Va sur Binance P2P achete {row['montant_cdf']/USD_TO_CDF:.2f} USDT et envoie vers {TRUST_WALLET_BTC}")
                        st.rerun()
            st.dataframe(df)
    elif code:
        st.error("Code faux")
