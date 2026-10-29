import streamlit as st
import streamlit.components.v1 as components

# --- FIX POUR ADS.TXT ET ADSENSE ---
query_params = st.query_params
if "ads.txt" in query_params or "ads" in str(query_params).lower():
    st.text("google.com, pub-3622864122301359, DIRECT, f08c47fec0942fa0")
    st.stop()

# Injection du code AdSense dans le HEAD pour que Google le voie
components.html("""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3622864122301359" crossorigin="anonymous"></script>
<script>
  // Forcer ads.txt visible
  console.log("AdSense OK");
</script>
""", height=0)

st.markdown("""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3622864122301359" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

# --- TON APP LSHI TRUST COMMENCE ICI ---
st.title("💰 Lshi Trust")
st.write("Bienvenue sur Lshi Trust - Lubumbashi")

# ... garde le reste de ton code Lshi Trust ici en bas ...
# Si tu avais du code avant, recolle-le en dessous de cette ligne
