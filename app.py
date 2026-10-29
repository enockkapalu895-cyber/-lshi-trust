import streamlit as st

CODE = "LSHI2026"
NUM = "0999783612"

st.title("Lshi Trust")
st.write("Airtel Money: 0999783612")
st.write("Nom: Enock Kapalu")
st.divider()

if "users" not in st.session_state:
    st.session_state.users = {}

mode = st.selectbox("Menu", ["Inscription", "Connexion", "Patron"])

if mode == "Inscription":
    nom = st.text_input("Nom")
    tel = st.text_input("Tel")
    mdp = st.text_input("Mdp", type="password")
    if st.button("Creer"):
        st.session_state.users[tel] = {"nom": nom, "mdp": mdp}
        st.success("Cree! Va dans Connexion")

if mode == "Connexion":
    tel = st.text_input("Tel")
    mdp = st.text_input("Mdp", type="password")
    if st.button("Entrer"):
        if tel in st.session_state.users:
            st.success("Connecte " + tel)
            st.write("Pour deposer, envoie Airtel a 0999783612")

if mode == "Patron":
    code = st.text_input("Code", type="password", placeholder="........")
    if code == CODE:
        st.success("Bienvenue Patron")
        st.write(st.session_state.users)
