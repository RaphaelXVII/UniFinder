import streamlit as st

st.set_page_config(page_title="UniFinder", page_icon="🎓", layout="wide")
st.navigation([st.Page("home.py", title="Home", default=True)], position="hidden").run()
