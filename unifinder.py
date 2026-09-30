import streamlit as st
import requests
from college_api import get_colleges
#from college_api import parse_location

#Defining Pages across service
Home = st.Page("home.py", title="Home")
ComparePage = st.Page("compare.py", title="Compare Your Stats")
pg = st.navigation([Home, ComparePage])
pg.run()
