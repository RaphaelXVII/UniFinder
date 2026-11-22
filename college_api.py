import os
from threading import Lock
from time import monotonic, sleep

import requests
from dotenv import load_dotenv


load_dotenv()

BASE_URL = "https://api.data.gov/ed/collegescorecard/v1/schools"
LOCATION_URL = "https://nominatim.openstreetmap.org/search"
_location_lock = Lock()
_last_location_request = float("-inf")
SCHOOL_FIELDS = {
    "id": "Institution ID",
    "school.name": "School",
    "school.city": "City",
    "school.state": "State",
    "latest.admissions.admission_rate.overall": "Admission rate",
    "latest.cost.tuition.in_state": "In-state tuition",
    "latest.cost.tuition.out_of_state": "Out-of-state tuition",
    "latest.admissions.sat_scores.average.overall": "Average SAT",
    "latest.admissions.act_scores.midpoint.cumulative": "ACT midpoint",
    "location.lat": "Latitude",
    "location.lon": "Longitude",
}


def get_location_suggestions(city):
    global _last_location_request
    with _location_lock:
        sleep(max(0, 1 - (monotonic() - _last_location_request)))
        _last_location_request = monotonic()
        response = requests.get(
            os.getenv("NOMINATIM_SEARCH_URL", LOCATION_URL),
            params={"q": city, "format": "jsonv2", "countrycodes": "us",
                    "addressdetails": 1, "accept-language": "en", "limit": 5},
            headers={"User-Agent": "UniFinder/1.0 (classroom college search)"},
            timeout=5,
        )
    response.raise_for_status()
    locations = response.json()
    if not isinstance(locations, list):
        raise ValueError("Unexpected location response")
    return locations


def get_colleges(state, city=None):
    api_key = os.getenv("COLLEGE_SCORECARD_API_KEY")
    if not api_key:
        raise RuntimeError("Set COLLEGE_SCORECARD_API_KEY in your environment before searching.")

    params = {
        "api_key": api_key,
        "school.state": state,
        "school.operating": 1,
        "school.degrees_awarded.predominant": "2,3",
        "fields": ",".join(SCHOOL_FIELDS),
        "per_page": 100,
        "page": 0,
    }
    if city:
        params["school.city"] = city

    schools = []
    while True:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        try:
            results = data["results"]
            total = data["metadata"]["total"]
            if not isinstance(results, list) or not isinstance(total, int):
                raise TypeError
        except (KeyError, TypeError):
            raise ValueError("College Scorecard returned an unexpected response. Please try again.") from None

        schools.extend(results)
        if len(schools) >= total:
            return schools
        if not results:
            raise ValueError("College Scorecard returned an incomplete result. Please try again.")
        params["page"] += 1
