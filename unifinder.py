import streamlit as st
import requests

st.header("UniFinder", text_alignment="center")

#Name Input
name = st.text_input(
    "Enter your Name",
    value="",
    placeholder="e.g. John Doe",

)
# GPA Input
gpa = st.number_input(
    "High school GPA",
    min_value=1.0,
    max_value=5.0,
    value=None,
    step=0.1,
    placeholder="Enter GPA (0.0 - 4.0)"
)

# This lets the user pick between an SAT or ACT Score to input /
# the reason why its outside of st.form is because st.form function saves  multiple inputs before submitting it to the backend
# and we want the score input box to pop up after they make a choice so that user can input score.
score_type = st.radio(
    "Select the Test score type",
    ["SAT", "ACT"],
    index=None
)

#st.form is used to create a form of inputs and holds onto all the values so that
# individual inputs are not be re-ran over and over again and instead holds all values.
with st.form("Student Information Input"):


#If else statements based on Score types
    if score_type == "SAT":
        sat_score = st.number_input(
            "SAT score",
            min_value=400,
            max_value=1600,
            value=None,
            step=100,
            placeholder="Enter SAT score (400 to 1600)"
        )
    if score_type == "ACT":
        act_score =st.number_input(
            "ACT score",
            min_value=1,
            max_value=36,
            value=None,
            step=1,
            placeholder="Enter ACT score (1 to 36)"
        )

    #Location Input
    location = st.text_input(
        "Enter Location",
        "",
        placeholder="e.g. Miami"
    )
#st.container is used to move/ center anything that you need
    with st.container(horizontal_alignment="center"):
        sumbit = st.form_submit_button("Submit")

#If Inputs are not filled in, Submit button won't work

 # submit & st.write submit the values and returns what the user enntered
if sumbit:
    st.write("Name: ", name)
    st.write("GPA", gpa)
    if score_type=="SAT":
        st.write("SAT Score: ", sat_score)
    elif score_type=="ACT":
        st.write("ACT Score: ", act_score)
    st.write("Location: ", location)









