import streamlit as st

st.set_page_config(page_title="Lshi Trust", page_icon="💰")
st.title("Lshi Trust 💰")
st.subheader("Épargne sécurisée à Lubumbashi")

st.success("Ton site est en ligne !")

nom = st.text_input("Ton nom")
montant = st.number_input("Montant à épargner (CDF)", min_value=0)

if st.button("Épargner"):
    if nom:
        st.balloons()
        st.write(f"Merci {nom}, ton épargne de {montant} CDF est enregistrée !")
    else:
        st.error("Écris ton nom d'abord")
