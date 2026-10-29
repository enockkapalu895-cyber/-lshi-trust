import streamlit as st
from datetime import datetime
st.set_page_config(page_title="Lshi Trust", page_icon="💰")
CODE="LSHI2026"
NUM="0999783612"
if "users" not in st.session_state:
    st.session_state.users={}
if "curr" not in st.session_state:
    st.session_state.curr=None
if "patron" not in st.session_state:
    st.session_state.patron=False
if "trans" not in st.session_state:
    st.session_state.trans=[]
st.title("Lshi Trust 💰")
st.write(f"Airtel Money: {NUM}")
st.divider()
if st.session_state.curr:
    u=st.session_state.users[st.session_state.curr]
    st.header(u["nom"])
    st.metric("USD",str(u["usd"])+" $")
    st.metric("CDF",str(u["cdf"])+" FC")
    st.divider()
    st.subheader("Deposer Airtel")
    st.info(f"Envoie a {NUM} - Enock Kapalu")
    with st.form("dep"):
        d1=st.selectbox("Devise",["USD","CDF"])
        d2=st.number_input("Montant",1,1000000,10)
        d3=st.text_input("Ref Airtel")
        ok=st.form_submit_button("J'ai envoye")
        if ok:
            st.session_state.trans.append([u["tel"],u["nom"],d2,d1,d3,str(datetime.now())[0:16],"Attente"])
            st.success("Recu! Patron va confirmer")
    if st.button("Deconnexion"):
        st.session_state.curr=None
        st.rerun()
else:
    a,b,c=st.tabs(["INSCRIPTION","CONNEXION","
