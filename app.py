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

if not st.session_state.logged_in and not st.session_state.is_admin:
    st.title("Lshi Trust 💰")
    st.subheader("Bienvenue Lubumbashi")
    st.write("Cree ton compte avant d'epargner")
    tab1, tab2, tab3 = st.tabs(["S'inscrire", "Se connecter", "Patron"])
    with tab1:
        st.markdown("### Creer un compte")
        nom = st.text_input("Nom complet", key="n1")
        email = st.text_input("Email Gmail", key="e1")
        whatsapp = st.text_input("WhatsApp", key="w1")
        mdp = st.text_input("Mot de passe", type="password", key="m1")
        mdp2 = st.text_input("Confirme mot de passe", type="password", key="m2")
        if st.button("S'inscrire", use_container_width=True):
            if not nom or not email or not mdp:
                st.error("Remplis tout")
            elif mdp != mdp2:
                st.error("Mots de passe differents")
            elif trouver_user(email):
                st.error("Compte existe deja")
            else:
                st.session_state.users.append({"nom": nom, "email": email, "whatsapp": whatsapp, "password": mdp})
                st.success("Compte cree ! Va dans Se connecter")
                st.balloons()
    with tab2:
        st.markdown("### Connexion Client")
        email_log = st.text_input("Ton Email", key="e2")
        mdp_log = st.text_input("Mot de passe", type="password", key="m3")
        if st.button("Entrer", use_container_width=True):
            u = trouver_user(email_log)
            if u and u["password"] == mdp_log:
                st.session_state.logged_in = True
                st.session_state.current_user = u
                st.rerun()
            else:
                st.error("Email ou mot de passe incorrect")
    with tab3:
        st.markdown("### Espace Patron")
        code = st.text_input("Code Admin", type="password", key="c1")
        if st.button("Ouvrir cahier"):
            if code == CODE_PATRON:
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("Code incorrect")
else:
    c1, c2 = st.columns([3, 1])
    with c1:
        if st.session_state.is_admin:
            st.write("**Mode PATRON**")
        else:
            st.write(f"Bonjour {st.session_state.current_user['nom']}")
    with c2:
        if st.button("Quitter"):
            st.session_state.logged_in = False
            st.session_state.is_admin = False
            st.session_state.current_user = None
            st.rerun()
    if st.session_state.is_admin:
        st.header("CAHIER DU PATRON")
        if st.session_state.epargnes:
            df = pd.DataFrame(st.session_state.epargnes)
            st.dataframe(df, use_container_width=True)
            st.metric("Total", f"{df['Montant'].sum()} CDF")
        else:
            st.info("Pas encore d'epargnes")
        if st.session_state.users:
            st.subheader("Comptes inscrits")
            st.dataframe(pd.DataFrame(st.session_state.users))
    else:
        st.title("Epargner maintenant")
        st.success("Compte verifie")
        with st.form("epar"):
            st.write(f"Nom: {st.session_state.current_user['nom']}")
            montant = st.number_input("Montant CDF", min_value=5000, step=1000)
            duree = st.selectbox("Duree", ["2 semaines (Bonus 3%)", "1 mois (Bonus 5%)", "3 mois (Bonus 10%)"])
            btn = st.form_submit_button("Epargner", use_container_width=True)
            if btn:
                pct = {"2 semaines (Bonus 3%)": 0.03, "1 mois (Bonus 5%)": 0.05, "3 mois (Bonus 10%)": 0.10}[duree]
                jours = {"2 semaines (Bonus 3%)": 14, "1 mois (Bonus 5%)": 30, "3 mois (Bonus 10%)": 90}[duree]
                total = int(montant * (1 + pct))
                date_ret = datetime.now() + timedelta(days=jours)
                st.session_state.epargnes.append({"Client": st.session_state.current_user['nom'], "Email": st.session_state.current_user['email'], "Montant": montant, "Total": total, "Retour": date_ret.strftime("%d/%m/%Y")})
                st.success(f"Recu {montant} CDF. Tu recevras {total} CDF le {date_ret.strftime('%d/%m/%Y')}")
        mes = [e for e in st.session_state.epargnes if e["Email"] == st.session_state.current_user["email"]]
        if mes:
            st.subheader("Mes epargnes")
            st.dataframe(pd.DataFrame(mes))
