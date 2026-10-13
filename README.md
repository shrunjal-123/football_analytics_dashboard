# ⚽ Football Player Performance Analytics Dashboard

An interactive, multi-page analytics dashboard built with Python and Streamlit that visualises synthetic football player statistics across teams, positions, and seasons. The app delivers KPI cards, scatter plots, box plots, heatmaps, and a searchable data table — all driven by a fully synthetic dataset so it runs out of the box with no external data sources or API keys required.

---

## ⚠️ Data Disclaimer

**All data in this project is entirely synthetic and fictional.**
The dataset was generated programmatically using `numpy.random.seed(42)` for reproducibility. Player names, team names, and all statistics are computer-generated and do **not** represent real football players, clubs, or match results.

---

## 📋 Features

- **Overview KPIs** — Five live metric cards (Total Players, Total Goals, Total Assists, Total Minutes Played, Average Rating) that update instantly when sidebar filters change.
- **Player Analysis** — Goals vs Assists scatter, Shots vs Goals scatter, and a head-to-head player comparison bar chart across 6 key metrics.
- **Team Analysis** — Stacked goals + assists bar chart per team, player count per team, and top-5 scorers / assisters for a selected team.
- **Position Analysis** — Rating distribution box plots by position, an average-stats heatmap, and goals-per-90 bar chart.
- **Data Table + CSV Export** — Sortable, searchable (player name) data table with a one-click filtered CSV download.

---

## 🗂️ Project Structure

```
football_analysis_dashboard/
├── app.py                  # Main Streamlit application
├── football_players.csv    # Synthetic player dataset (120 rows, 18 columns)
├── generate_data.py        # Script to regenerate the dataset
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🚀 Running Locally

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/your-username/football_analysis_dashboard.git
   cd football_analysis_dashboard
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

6. **Open in your browser** at `http://localhost:8501`

---

## ☁️ Deploying to Streamlit Cloud

1. Push the project to a **public GitHub repository**.
2. Go to [https://share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **"New app"** → select your repository → set the **Main file path** to `app.py`.
4. Click **"Deploy"** — Streamlit Cloud reads `requirements.txt` and installs all dependencies automatically.

---

## 📊 Dataset Schema

The synthetic dataset (`football_players.csv`) contains **120 rows** and **18 columns**:

| Column | Type | Description |
|---|---|---|
| `player_id` | int | Unique numeric identifier for each player record |
| `player_name` | str | Randomly generated "First Last" name |
| `team` | str | One of 10 synthetic club names |
| `position` | str | Player position: GK, DEF, MID, or FWD |
| `season` | str | Season label, e.g. `"2022-23"` or `"2023-24"` |
| `age` | int | Player age, sampled between 17 and 38 |
| `matches_played` | int | Appearances in the season, range 1–38 |
| `minutes_played` | int | `matches_played × ~70–90` minutes |
| `goals` | int | Position-weighted count; FWD > MID > DEF > GK |
| `assists` | int | Position-weighted count; MID > FWD > DEF > GK |
| `shots` | int | Always ≥ goals |
| `shots_on_target` | int | Always ≤ shots |
| `pass_accuracy` | float | Percentage value in range 60–98 % |
| `dribbles_completed` | int | Position-weighted; attackers complete more |
| `yellow_cards` | int | Random integer in range 0–10 |
| `red_cards` | int | Random integer in range 0–3 |
| `clean_sheets` | int | Non-zero only for GK and DEF; zero for MID/FWD |
| `rating` | float | Match rating 5.0–9.5, weighted by goal/assist output |

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** — multi-page app framework and UI widgets
- **Pandas & NumPy** — data generation, wrangling, and aggregation
- **Plotly Express & Plotly Graph Objects** — interactive charts (scatter, bar, box, heatmap)
- **statsmodels** — LOWESS trendline support in Plotly Express

---

*Built as a portfolio project. All data is synthetic.*
