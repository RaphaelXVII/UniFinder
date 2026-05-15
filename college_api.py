import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COLLEGE_SCORECARD_API_KEY")
BASE_URL = "https://api.data.gov/ed/collegescorecard/v1/schools"
def parse_location(location):
    parts = location.split(",")
    city = parts[0].strip()
    state = parts[1].strip()
    return city, state

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
result = get_colleges("FL")
print(result)