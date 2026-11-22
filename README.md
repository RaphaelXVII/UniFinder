# UniFinder

Find U.S. colleges by location and compare tuition, campus locations, and reported admissions profiles. Enter a weighted GPA or an ACT or SAT score to see personalized matches where benchmarks are available.

## Run locally

Use Python 3.10 or later and install the requirements.

```sh
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Set `COLLEGE_SCORECARD_API_KEY` in your shell environment or a local `.env` file. On Streamlit Community Cloud, set it in the app's Secrets settings.

## Data sources

- [U.S. Department of Education College Scorecard](https://collegescorecard.ed.gov/data/api-documentation/)
- [OpenStreetMap Nominatim](https://operations.osmfoundation.org/policies/nominatim/)
- [Florida public university fall admissions profiles](https://www.flbog.edu/wp-content/uploads/2025/09/25_26_Matrix_Pager.pdf)
