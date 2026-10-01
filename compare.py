import streamlit as st
import requests
from altair.theme import names

from college_api import get_colleges
#from college_api import parse_location

#Header text for Stats
st.header("Stats Overview 📚", text_alignment="center")
with st.container(horizontal=True, gap="medium"):
    with st.container(border=True, width=200, height=200, horizontal=True, horizontal_alignment="center",
                      vertical_alignment="center"):
        st.header("Testing if Text Shows")
        #st.session_state.get("name" )
        st.text("Text Test")

    with st.container(border=True, width=200, height=200, horizontal=True, horizontal_alignment="center",
                      vertical_alignment="center"):
        st.header("Testing if Text Shows")
        st.text("Text Test")

    with st.container(border=True, width=200, height=200, horizontal=True, horizontal_alignment="center",
                      vertical_alignment="center"):
        st.header("Testing if Text Shows")
        st.text("Text Test")



