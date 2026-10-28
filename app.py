import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Lshi Trust", page_icon="💰", layout="centered")

# --- MEMOIRE ---
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
ADMIN_EMAIL = "enockkapalu895@gmail.com"

def trouver_user(email):
    for u in st.session_state.users:
        if u["email"].lower() == email.lower():
            return u
    return None

# =================================================
# PAGE 1 : SI PAS CONNECTÉ -> INSCRIPTION OBLIGATOIRE
# =================================================
if not st.session_state.logged_in and not st.session_state.is_admin:
    st.title("Lshi Trust 💰")
    st.subheader("Bienvenue à Lubumbashi")
    st.write("Avant d'épargner, crée ton compte sécurisé")

    tab_inscrit, tab_connect, tab_patron = st.tabs(["📝 S'inscrire", "🔐 Se connecter", "👑 Patron"])

    with tab_inscrit:
        st.markdown("### Créer un compte")
        
        # BOUTON GOOGLE (visuel)
        if st.button("🔵 Continuer avec Google", use_container_width=True):
            st.info("Connexion Google bientôt disponible ! Pour l'instant, inscris-toi avec ton email ci-dessous 👇")
        
        st.divider()
        st.write("Ou avec email :")
        
        nom = st.text_input("Nom complet", key="ins_nom")
        email = st.text_input("Ton Email Gmail", key="ins_email")
        whatsapp = st.text_input("Numéro WhatsApp", key="ins_what")
        mdp = st.text_input("Crée un mot de passe", type="password", key="ins_mdp1")
        mdp2 = st.text_input("Confirme mot de passe", type="password", key="ins_mdp2")

        if st.button("S'inscrire maintenant", use_container_width=True):
            if not nom or not email or not mdp:
                st.error("Remplis tout chef")
            elif mdp != mdp2:
                st.error("Les 2 mots de passe ne sont pas les mêmes")
            elif trouver_user(email):
                st.error("Ce compte existe déjà, va dans 'Se connecter'")
            else:
                st.session_state.users.append({"nom":nom, "email":email, "whatsapp":whatsapp, "password":mdp})
                st.success("✅ Compte créé ! Va maintenant dans 'Se connecter' pour entrer")
                st.balloons()

    with tab_connect:
        st.markdown("### Connexion Client")
        email_login = st.text_input("Ton Email", key="log_email")
        mdp_login = st.text_input("Mot de passe", type="password", key="log_mdp")
        if st.button("Entrer dans Lshi Trust", use_container_width=True):
            user = trouver_user(email_login)
            if user and user["password"] == mdp_login:
                st.session_state.logged_in = True
                st.session_state.current_user = user
                st.rerun()
            else:
                st.error("Email ou mot de passe incorrect")

    with tab_patron:
        st.markdown("### Espace Patron")
        code = st.text_input("Code Admin", type="password", key="patron_code")
        if st.button("Ouvrir mon cahier"):
            if code == CODE_PATRON:
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("Code incorrect")

# =================================================
# PAGE 2 : SI CONNECTÉ -> ACCUEIL ÉPARGNE
# =================================================
else:
    # BOUTON DECONNEXION
    col1, col2 = st.columns([3,1])
    with col1:
       
