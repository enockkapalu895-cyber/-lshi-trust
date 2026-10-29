import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Lshi Trust", page_icon="💰", layout="centered")
CODE_PATRON = "LSHI2026"

if "users" not in st.session_state:
    st.session_state.users = {}
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "is_patron" not in st.session_state:
    st.session_state.is_patron = False

st.title("💰 Lshi Trust")
st.markdown("<p style='text-align:center;color:#888;'>Micro-épargne - Lubumbashi</p>", unsafe_allow_html=True)
st.write("---")

if st.session_state.current_user:
    user = st.session_state.users[st.session_state.current_user]
    st.header(f"Salut {user['nom']} 👋")
    c1,c2 = st.columns(2)
    c1.metric("Ton Épargne", f"{user['solde']} $")
    c2.metric("Commune", user['commune'])
    if st.button("Se déconnecter"):
        st.session_state.current_user=None
        st.rerun()
else:
    tab1, tab2, tab3 = st.tabs(["📝 INSCRIPTION", "🔑 SE CONNECTER", "👑 MODE PATRON"])
    with tab1:
        with st.form("insc"):
            nom=st.text_input("Nom complet")
            tel=st.text_input("WhatsApp ex: 097...")
            commune=st.selectbox("Commune",["Kenya","Kamalondo","Katuba","Ruashi","Kampemba","Lubumbashi","Autre"])
            mdp=st.text_input("Mot de passe",type="password")
            epargne=st.number_input("Épargne départ $",10,1000,20)
            btn=st.form_submit_button("S'INSCRIRE")
            if btn and nom and tel and mdp:
                st.session_state.users[tel]={"nom":nom,"tel":tel,"commune":commune,"mdp":mdp,"solde":epargne,"date":datetime.now().strftime("%d/%m/%Y"),"historique":[f"Inscription {epargne}$"]}
                st.success("Compte créé ! Va dans SE CONNECTER")
                st.balloons()
            elif btn:
                st.error("Remplis tout chef")
    with tab2:
        t=st.text_input("Ton numéro WhatsApp")
        m=st.text_input("Mot de passe",type="password",key="m2")
        if st.button("SE CONNECTER", use_container_width=True):
            if t in st.session_state.users and st.session_state.users[t]['mdp']==m:
                st.session_state.current_user=t
                st.rerun()
            else:
                st.error("Numéro ou mot de passe incorrect")
    with tab3:
        code=st.text_input("Code patron",type="password", placeholder="LSHI2026")
        if st.button("Entrer mode Patron"):
            if code==CODE_PATRON:
                st.session_state.is_patron=True
                st.rerun()
            else:
                st.error("Code incorrect")
        if st.session_state.is_patron:
            st.success("Bienvenue Patron 👑 LSHI2026")
            if st.session_state.users:
                total=sum(u['solde'] for u in st.session_state.users.values())
                st.metric("TOTAL CAISSE",f"{total} $")
                st.metric("CLIENTS",len(st.session_state.users))
                df=pd.DataFrame([{"Nom":u['nom'],"Tel":u['tel'],"Solde":u['solde'],"Commune":u['commune']} for u in st.session_state.users.values()])
                st.dataframe(df,use_container_width=True)
            if st.button("Quitter mode patron"):
                st.session_state.is_patron=False
                st.rerun()

st.write("---")
st.caption("Lshi Trust © 2026 - Lubumbashi")
