import streamlit as st
import requests


#st.header is used for alignment of text
st.header("UniFinder", text_alignment="center")

# This is where we implemented Nominatim API to find a more precise location of where the student is located
#the url is where we are getting the specific locations that match the input that the User inputs
def search_location(query):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": query,
        "format": "json",
        "countrycodes": "us",
        "limit": 5,
    }

    headers = {"User-Agent": "UniFinder"}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception:
        return []

#User inputs their name
name = st.text_input(
    "Enter your Name",
    value="",
    placeholder="e.g. John Doe",

)
# User inputs their GPA / min 1.0 GPA - max 5.0 GPA
gpa = st.number_input(
    "High school GPA",
    min_value=1.0,
    max_value=5.0,
    value=None,
    step=0.1,
    placeholder="Enter GPA (0.0 - 4.0)"
)



# SAT/ACT INPUT This lets the user pick between an SAT or ACT Score to input
# the reason why its outside of st.form is because st.form function saves multiple inputs before submitting it to the backend
# and we want the score input box to pop up after they make a choice so that user can input score.
score_type = st.radio(
    "Select the Test score type",
    ["SAT", "ACT"],
    index=None
)
#Setting the inital scores as 0 so then the user can input their own score
sat_score = None
act_score = None

#If else statements for ACT and SAT scores. It will not accept scores outside the range which is min & max values
if score_type == "SAT":
        sat_score = st.number_input(
            "SAT score",
            min_value=400,
            max_value=1600,
            value=None,
            step=100,
            placeholder="Enter SAT score (400 to 1600)"
        )
elif score_type == "ACT":
        act_score =st.number_input(
            "ACT score",
            min_value=1,
            max_value=36,
            value=None,
            step=1,
            placeholder="Enter ACT score (1 to 36)"
        )


#LOCATION INPUT / User inputs a location and the code
# on line 10 uses that input from the user to find the most similar location entered
location = st.text_input(
    "Enter your Location",
    placeholder="e.g. Miami"
)

selected_location =None


#If else statements for location search.
# This is the function that actually finds the most similar location inputted
if location and len(location) >=2:
    results = search_location(location)
    if results:
        options = [place["display_name"] for place in results]
        selected_location = st.selectbox(
            "Select Location",
            options,
            index=None,
            placeholder="Select a Location"
        )
        if selected_location:
            st.success(f"Selected: {selected_location}")
    else:
            st.error("Not a valid U.S location")


#This is slider for Tuition
st.slider(
    "Tuition you are willing to pay",
    min_value = 0,
    max_value = 300000,
    value=None,
    step=1000,
    format = "dollar",
    key=None,
)


#If all Inputs are not filled in, the submit button will not work line 110 and 123 are conneceted
score_filled = (score_type == "ACT" and act_score is not None) or (score_type == "SAT" and sat_score is not None)
filled = (gpa is not None) and (score_type is not None) and (selected_location is not None) and score_filled


#st.form is used to create a form of inputs and holds onto all the values so that
# individual inputs are not be re-ran over and over again and instead holds all values.
with st.form("Student Information Input"):





#SUBMIT BUTTON IS HERE / st.container is used to align anything that you need
#line 110 is a boolean that checks if every input is filled
#line 123 has the "disabled= not filled" which is another boolean is that automatically false and turns on when all inputs are filled in
    with st.container(horizontal_alignment="center"):
        sumbit = st.form_submit_button("Submit", disabled= not filled)




 # "if submit" & "st.write" actually submit the inputs and returns what the user entered
if sumbit:
    st.write("Name: ", name)
    st.write("GPA", gpa)
    if score_type=="SAT":
        st.write("SAT Score: ", sat_score)
    elif score_type=="ACT":
        st.write("ACT Score: ", act_score)
    st.write("Location: ", selected_location)









