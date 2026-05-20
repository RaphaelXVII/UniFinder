import requests
import os
from dotenv import load_dotenv


load_dotenv() #opens and reads .env file

#storing the API key and address in variables
API_KEY = os.getenv("COLLEGE_SCORECARD_API_KEY")
BASE_URL = "https://api.data.gov/ed/collegescorecard/v1/schools"

#defining a function that takes the raw location the user typed and grabs the city and state separately returns both values back
def parse_location(location):
    parts = location.split(",")
    city = parts[0].strip()
    state = parts[1].strip()
    return city, state

#defining main function. takes state as required, city optional.
def get_colleges(state, city=None):
    params = {
        "api_key": API_KEY,
        "school.state": state,
        "fields": "school.name,school.state,school.city,latest.admissions.admission_rate.overall,latest.cost.tuition.in_state,latest.cost.tuition.out_of_state,latest.admissions.sat_scores.average.overall,latest.admissions.act_scores.midpoint.cumulative",
        "per_page": 20
    }
    if city:
            params["school.city"] = city

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    return data["results"]
