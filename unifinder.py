import streamlit as st

st.set_page_config(page_title="UniFinder", page_icon="🎓", layout="wide")

#Defining Pages across service
Home = st.Page("home.py", title="Home", default=True)
#ComparePage = st.Page("compare.py", title="Compare Your Stats")
UsabilityPage = st.Page("usability.py", title="Usability Testing")
pg = st.navigation([Home, UsabilityPage])
pg.run()
