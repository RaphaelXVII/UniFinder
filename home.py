import pandas as pd
import requests
import streamlit as st

from college_api import SCHOOL_FIELDS, get_colleges, get_location_suggestions
from college_matches import FLORIDA_PROFILE_SOURCE, best_matches


STATE_ABBREVIATIONS = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}


@st.cache_data(ttl=900, max_entries=128, show_spinner=False)
def search_colleges(state):
    return get_colleges(state)


@st.cache_data(ttl=86_400, max_entries=128, show_spinner=False)
def search_locations(city):
    return {
        place["display_name"]: place.get("address", {}).get("state")
        for place in get_location_suggestions(city)
        if place.get("display_name")
        and place.get("address", {}).get("state") in STATE_ABBREVIATIONS
    }


def show_results(search):
    st.header(f"College results for {search['location']}")
    if not search["schools"]:
        st.info("College Scorecard returned no schools for this state. Try selecting a city in another state.")
        return

    schools = pd.DataFrame(search["schools"], columns=list(SCHOOL_FIELDS)).rename(columns=SCHOOL_FIELDS)
    numeric_columns = ["Admission rate", "In-state tuition", "Out-of-state tuition",
                       "Average SAT", "ACT midpoint", "Latitude", "Longitude"]
    schools[numeric_columns] = schools[numeric_columns].apply(pd.to_numeric, errors="coerce")
    schools = schools.sort_values(["School", "City"])
    tuition = search["tuition"]
    budget = search["budget"]
    st.caption(f"Annual budget ${budget:,} · {tuition} · Source: U.S. Department of Education College Scorecard")
    if st.checkbox("Show only schools within my tuition budget", key="within_budget"):
        schools = schools.loc[schools[tuition].le(budget)]
        st.caption("Schools with unreported tuition are excluded while this filter is on.")
    if schools.empty:
        st.info("No schools have reported tuition within this budget. Clear the filter to see every result.")
        return

    st.success(f"Showing {len(schools):,} of {len(search['schools']):,} schools returned for this location.")
    gpa = search.get("gpa")
    score_type = search["score_type"]
    score = search["score"]
    st.subheader("Best matches")
    if gpa is None and score is None:
        st.info("Enter your weighted GPA or an ACT or SAT score, then select Find colleges to see matches.")
    else:
        matches, uses_gpa = best_matches(schools, gpa, score_type, score, tuition)
        if matches.empty:
            if score is None:
                st.info("GPA benchmarks are unavailable for these schools. Add an ACT or SAT score to find more matches.")
            else:
                st.info(f"The schools shown have no published {score_type} benchmark.")
        else:
            profile = []
            if uses_gpa:
                profile.append(f"Weighted GPA {gpa:.2f}")
            if score is not None:
                profile.append(f"{score_type} {score:,}")
            st.caption(" · ".join(profile))
            if uses_gpa:
                st.caption(
                    "Ranked by closeness to published fall profile midpoints for participating "
                    f"Florida public universities. [2025–2026 fall profiles]({FLORIDA_PROFILE_SOURCE})"
                )
            else:
                if gpa is not None:
                    st.info("GPA benchmarks are unavailable for these schools.")
                st.caption(f"Ranked by closeness to reported {score_type} scores in College Scorecard.")
            st.dataframe(
                matches,
                hide_index=True,
                column_config={tuition: st.column_config.NumberColumn(format="dollar")},
            )
            st.caption("Use these comparisons to build a shortlist. Admission decisions depend on each school's criteria.")

    st.subheader("All college results")
    st.caption("Blank cells mean the data was unreported. Admission rates describe past applicants.")
    st.dataframe(
        schools.drop(columns=["Institution ID", "Latitude", "Longitude"]),
        hide_index=True,
        column_config={
            "Admission rate": st.column_config.NumberColumn(format="percent"),
            "In-state tuition": st.column_config.NumberColumn(format="dollar"),
            "Out-of-state tuition": st.column_config.NumberColumn(format="dollar"),
            "Average SAT": st.column_config.NumberColumn(format="%d"),
            "ACT midpoint": st.column_config.NumberColumn(format="%d"),
        },
    )

    st.subheader("Annual tuition comparison")
    lowest = schools.nsmallest(10, tuition).dropna(subset=[tuition])
    if lowest.empty:
        st.info("No tuition data is available for the schools shown.")
    else:
        st.caption(f"Up to 10 schools with the lowest reported {tuition.lower()}. See the table for exact amounts.")
        st.bar_chart(lowest, x="School", y=tuition, horizontal=True, sort=False,
                     y_label="Annual tuition (USD)")

    st.subheader("Campus map")
    campuses = schools.loc[
        schools["Latitude"].between(-90, 90)
        & schools["Longitude"].between(-180, 180)
        & (schools["Latitude"].ne(0) | schools["Longitude"].ne(0))
    ]
    if campuses.empty:
        st.info("The schools shown have no campus coordinates. Their cities and states are listed in the table.")
    else:
        st.caption(f"The map shows {len(campuses):,} schools with campus coordinates. "
                   "See the table for school names, cities, and states.")
        st.map(campuses[["Latitude", "Longitude"]], latitude="Latitude",
               longitude="Longitude", height=400)


st.title("UniFinder")
st.write("Explore U.S. colleges and compare annual tuition, admission rates, and campus locations.")

with st.expander("Student profile for matches (optional)", expanded=True):
    name = st.text_input("Enter your Name")
    gpa = st.number_input(
        "Weighted high school GPA", min_value=0.0, max_value=5.0, value=None, step=0.01,
        help="Use a GPA calculated on a 4.0 base with extra weight for advanced courses. "
             "Used where a school publishes a comparable benchmark.",
    )
    score_type = st.radio("Select the test score type", ["SAT", "ACT"], index=None, horizontal=True)
    score = None
    if score_type == "SAT":
        score = st.number_input("SAT score", min_value=400, max_value=1600, value=None, step=10)
    elif score_type == "ACT":
        score = st.number_input("ACT score", min_value=1, max_value=36, value=None)


with st.container(border=True, key="college_location"):
    with st.form("location_search", border=False):
        city = st.text_input("Enter your City", placeholder="e.g. Miami")
        lookup = st.form_submit_button("Search locations")

    if lookup:
        st.session_state.pop("selected_location", None)
        st.session_state.pop("location_suggestions", None)
        if len(city.strip()) < 2:
            st.warning("Enter a city name to search for locations.")
        else:
            try:
                with st.spinner("Looking up locations…"):
                    st.session_state["location_suggestions"] = search_locations(city.strip().casefold())
            except (requests.RequestException, ValueError):
                st.error("The location search is temporarily unavailable. Please try again.")

    suggestions = st.session_state.get("location_suggestions")
    state = None
    if suggestions:
        selected_location = st.selectbox("Select Location", suggestions, index=None,
                                         placeholder="Select a Location", key="selected_location")
        if selected_location:
            state = suggestions[selected_location]
            st.success(f"Selected: {selected_location}")
            st.caption(f"College results will cover all of {state}.")
    elif suggestions == {}:
        st.info("No matching U.S. locations. Check the city spelling or include its state.")

    st.caption("Location data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)")

with st.form("college_search"):
    rate_column, budget_column = st.columns(2)
    with rate_column:
        tuition = st.radio("Tuition rate", ["In-state tuition", "Out-of-state tuition"])
    with budget_column:
        budget = st.slider("Annual tuition budget", 0, 300_000, 25_000, step=1000, format="dollar")

    submitted = st.form_submit_button("Find colleges", type="primary")

if submitted:
    st.session_state.pop("college_search_results", None)
    if state is None:
        st.warning("Search for a city and select a location before looking up colleges.")
    else:
        try:
            with st.spinner("Looking up colleges on College Scorecard…"):
                results = search_colleges(STATE_ABBREVIATIONS[state])
        except requests.RequestException:
            st.error("College Scorecard could not be reached or returned an error. Please try again.")
        except (RuntimeError, ValueError) as error:
            st.error(str(error))
        else:
            st.session_state["name"] = name
            st.session_state["college_search_results"] = {
                "location": state,
                "budget": budget,
                "tuition": tuition,
                "score_type": score_type,
                "score": score,
                "gpa": gpa,
                "schools": results,
            }

if "college_search_results" in st.session_state:
    show_results(st.session_state["college_search_results"])
