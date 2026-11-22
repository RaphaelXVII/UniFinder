# UniFinder

UniFinder helps prospective students explore U.S. colleges by location and
annual tuition. The companion Usability Lab guides testing sessions, saves
responses to CSV, and summarizes task performance and feedback.

## Run

From the project directory:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run unifinder.py
```

Use Python 3.10 or later. If you do not have a virtual environment yet, run
`python3 -m venv .venv` first.
Home opens by default. Select **Usability Testing** in the sidebar for the Lab.

## College search

Set `COLLEGE_SCORECARD_API_KEY` in your local `.env` or shell environment.
On **Home**, the optional student profile appears above the location panel.
Enter a U.S. city, press Enter or select **Search locations**, and choose a
suggestion in the same panel. UniFinder searches for colleges across that
location's state. Choose a tuition rate and annual budget, then select
**Find colleges**. Sort the results
table by clicking a column heading. The budget checkbox filters the table,
tuition chart, and campus map together. The search covers operating colleges
whose predominant degree is an associate or bachelor's degree.

Enter a weighted GPA or choose **ACT** or **SAT** to enter one test score
under **Student profile for matches**. Up to five personalized matches appear
above the full results.
The [2025–2026 Florida public university fall profiles](https://www.flbog.edu/wp-content/uploads/2025/09/25_26_Matrix_Pager.pdf)
provide GPA benchmarks for 12 universities. Those matches use the distance
from the published midpoints, giving equal weight to differences of 0.5 GPA
points, 5 ACT points, or 150 SAT points. Where GPA benchmarks are unavailable,
matches use the student's selected test score and College Scorecard data.

Location suggestions use [OpenStreetMap Nominatim](https://operations.osmfoundation.org/policies/nominatim/).
The classroom app submits searches on demand, caches results, and limits the
process to one request per second. A deployment can set `NOMINATIM_SEARCH_URL`
to a compatible search endpoint.

The [HCI report](output/UniFinder_HCI_Report.docx) describes the search interface,
data processing, and verification.

## Usability Lab workflow

1. Introduction: explains the study and its steps.
2. Consent: customizable wording, explicit acceptance, and saved consent terms.
3. Demographics: age range, occupation/student status, grade level, school type, GPA range, sports,
   extracurricular activities, attendance, and prior familiarity with college search tools.
4. Tasks: task selection, start/stop timing, Yes/Partial/No outcomes, and observer notes.
5. Exit Questionnaire: satisfaction and difficulty ratings plus written feedback.
6. Report: saved responses, success rates, mean times, rating averages, charts, and CSV downloads.

An anonymous participant ID links the responses; timestamps use UTC. Each step
unlocks after the preceding step is saved. Use **Start New Participant** in the
facilitator expander for another session. A browser refresh starts a new
participant but retains saved data. Keep the browser session open during a test.

For the required mock demonstration, expand **Offline demo product: fictional
college results** on Tasks and use the synthetic table for both tasks. This path
needs no API key or internet connection. To test the live search, open
Home in a second browser tab while keeping the testing tool open. The live
search needs internet access and `COLLEGE_SCORECARD_API_KEY` in your local `.env`.
The original Compare page still has the project's earlier placeholders and is
outside this assignment's usability testing workflow.

## Code structure

- `unifinder.py`: app configuration and navigation.
- `usability.py`: testing tabs, validation, timers, and report UI.
- `usability_data.py`: CSV persistence and report calculations.
- `home.py` and `college_api.py`: college search, results, and API integration.
- `compare.py`: inactive comparison prototype.
- `tests/test_usability.py`: storage and Streamlit workflow checks.
- `scripts/build_submission_pdf.py`: source-code PDF generator (requires ReportLab).

Responses are saved in `data/consent_data.csv`, `data/demographic_data.csv`,
`data/task_data.csv`, and `data/exit_data.csv`. Paths are relative to the project.
`UNIFINDER_DATA_DIR` overrides the directory for isolated tests. Tests use
temporary directories and leave the real report empty for your recording.
CSV updates are atomic and protected within one Python process. This local
classroom tool has no authentication or multi-server database; Report shows all
local responses to the facilitator. Outcomes are observer-reported.

Student questions include a Prefer not to say option. GPA uses an unweighted
4.0 scale, with Not sure / different scale and Not applicable options. Earlier
demographic responses remain readable; questions that were not previously
asked appear blank. The form groups general demographics (age range,
occupation/student status, and tool familiarity) and student/school background.

## Verification and submission

```bash
python -m unittest discover -s tests -v
```

See `VERIFICATION.md` for the checks and `VIDEO_GUIDE.md` for a recording outline.
Method reference: [NN/g's Usability Testing 101](https://www.nngroup.com/articles/usability-testing-101/).

Submit `output/pdf/UniFinder_Source_Code.pdf`. Record a video of no more than
three minutes, upload it to YouTube (Unlisted is allowed), and put its link in
the submission comments. Upload the PDF to the assignment submission page.
