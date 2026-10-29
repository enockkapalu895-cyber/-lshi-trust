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
    c1,c2,c3 = st.columns(3)
    c1.metric("Épargne $", f"{user.get('solde_usd', user.get('solde',0))} $")
    c2.metric("Épargne FC", f"{user.get('solde_fc',0):,} FC")
    c3.metric("Commune", user['commune'])
    st.write("### 📒 Ton historique")
    for h in user.get('historique', []):
        st.write(f"- {h}")
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
            st.write("**Épargne de départ**")
            col_a, col_b = st.columns(2)
            devise = col_a.selectbox("Devise", ["USD ($)", "CDF (FC)"])
            montant = col_b.number_input("Montant", 0, 10000000, 20)
            btn=st.form_submit_button("S'INSCRIRE", use_container_width=True)
            if btn and nom and tel and mdp:
                usd = montant if "USD" in devise else 0
                fc = montant if "CDF" in devise else 0
                st.session_state.users[tel] = {"nom":nom,"tel":tel,"commune":commune,"mdp":mdp,"solde_usd":usd,"solde_fc":fc,"solde":usd,"date":datetime.now().strftime("%d/%m/%Y %H:%M"),"historique":[f"Inscription {montant} {devise} - {datetime.now().strftime('%d/%m/%Y')}"],"observations":""}
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
        st.caption("Accès réservé au gérant")
        code=st.text_input("Code patron",type="password", placeholder="••••••••")
        if st.button("Entrer mode Patron", use_container_width=True):
            if code==CODE_PATRON:
                st.session_state.is_patron=True
                st.rerun()
            else:
                st.error("Code incorrect")
        if st.session_state.is_patron:
            st.success("Bienvenue Patron 👑")
            st.write("---")
            if not st.session_state.users:
                st.info("Aucun client pour le moment")
            else:
                total_usd = sum(u.get('solde_usd', u.get('solde',0)) for u in st.session_state.users.values())
                total_fc = sum(u.get('solde_fc',0) for u in st.session_state.users.values())
                c1,c2,c3 = st.columns(3)
                c1.metric("TOTAL $", f"{total_usd} $")
                c2.metric("TOTAL FC", f"{total_fc:,} FC")
                c3.metric("CLIENTS", len(st.session_state.users))
                st.write("### 📋 Cahier d'observation - Liste complète")
                data = []
                for u in st.session_state.users.values():
                    data.append({"Date":u.get('date',''),"Nom":u['nom'],"Tel":u['tel'],"Commune":u['commune'],"Solde $":u.get('solde_usd', u.get('solde',0)),"Solde FC":u.get('solde_fc',0),"Observations":u.get('observations',''),"Historique":" | ".join(u.get('historique',[]))})
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True, height=400)
                st.write("---")
                st.write("### ✏️ Ajouter observation / épargne")
                tel_edit = st.selectbox("Choisir client", list(st.session_state.users.keys()), format_func=lambda x: f"{st.session_state.users[x]['nom']} - {x}")
                if tel_edit:
                    u = st.session_state.users[tel_edit]
                    st.write(f"Client: **{u['nom']}** | Actuel: {u.get('solde_usd',0)}$ / {u.get('solde_fc',0)} FC")
                    col1,col2 = st.columns(2)
                    new_devise = col1.selectbox("Ajouter en", ["USD ($)", "CDF (FC)"], key="dev2")
                    new_montant = col2.number_input("Montant à ajouter", 0, 10000000, 0, key="mont2")
                    note = st.text_area("Observation / Note", value=u.get('observations',''), placeholder="Ex: A payé 10$ le 29/10...")
                    if st.button("💾 Enregistrer"):
                        if "USD" in new_devise:
                            u['solde_usd'] = u.get('solde_usd', u.get('solde',0)) + new_montant
                        else:
                            u['solde_fc'] = u.get('solde_fc',0) + new_montant
                        u['solde'] = u.get('solde_usd',0)
                        u['observations'] = note
                        if new_montant>0:
                            u['historique'].append(f"+{new_montant} {new_devise} le {datetime.now().strftime('%d/%m/%Y')} - {note}")
                        st.success(f"Mise à jour pour {u['nom']} !")
                        st.rerun()
            if st.button("Quitter mode patron"):
                st.session_state.is_patron=False
                st.rerun()
st.write("---")
st.caption("Lshi Trust © 2026 - Lubumbashi")
