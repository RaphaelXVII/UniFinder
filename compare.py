import streamlit as st
import requests
from college_api import get_colleges
#from college_api import parse_location

#st.header is used for alignment of text
st.header("Compare your Stats 📚", text_alignment="center")
#Progress Bar
#bar = st.progress(0)
with st.sidebar:
    # COMPARE Tab will be used to compare student stats to university stats
    Compare = st.button("Compare your Stats", width=300)
    st.empty()