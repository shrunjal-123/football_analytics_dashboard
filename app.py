"""
app.py
------
Football Player Performance Analytics Dashboard
Powered by a fully synthetic dataset — all names, teams, and statistics
are fictional and generated for portfolio / demo purposes only.

Run with: streamlit run app.py
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Page config — must be the very first Streamlit call
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="⚽ Football Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Theme / CSS injection
# ---------------------------------------------------------------------------

DARK_THEME_CSS = """
<style>
/* ── Main background ─────────────────────────────────────────────────────── */
.stApp {
    background-color: #0e1117;
    color: #ffffff;
}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #10131a;
    border-right: 1px solid #2a2d35;
}
[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}

/* ── Metric / KPI cards ──────────────────────────────────────────────────── */
.metric-card {
    background-color: #1a1d23;
    border: 1px solid #2a2d35;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 8px;
}

/* ── Streamlit default metric widget overrides ───────────────────────────── */
[data-testid="stMetric"] {
    background-color: #1a1d23;
    border: 1px solid #2a2d35;
    border-radius: 10px;
    padding: 16px 20px;
}
[data-testid="stMetricValue"] {
    color: #00ff87 !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    color: #a0a8b8 !important;
    font-size: 0.85rem !important;
}

/* ── General text ────────────────────────────────────────────────────────── */
body, p, span, label, div {
    color: #ffffff;
}
h1, h2, h3, h4 {
    color: #00ff87;
}

/* ── Dividers ────────────────────────────────────────────────────────────── */
hr {
    border-color: #2a2d35;
}

/* ── Info / warning banners ──────────────────────────────────────────────── */
[data-testid="stAlert"] {
    background-color: #1a1d23;
    border-radius: 8px;
}
</style>
"""

st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EXPECTED_COLUMNS = [
    "player_id", "player_name", "team", "position", "season", "age",
    "matches_played", "minutes_played", "goals", "assists", "shots",
    "shots_on_target", "pass_accuracy", "dribbles_completed",
    "yellow_cards", "red_cards", "clean_sheets", "rating",
]

NUMERIC_COLUMNS = [
    "player_id", "age", "matches_played", "minutes_played", "goals",
    "assists", "shots", "shots_on_target", "pass_accuracy",
    "dribbles_completed", "yellow_cards", "red_cards", "clean_sheets",
    "rating",
]

STRING_COLUMNS = ["player_name", "team", "position", "season"]

POSITION_LABELS = {
    "GK": "Goalkeeper",
    "DEF": "Defender",
    "MID": "Midfielder",
    "FWD": "Forward",
}

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

@st.cache_data
def load_data() -> pd.DataFrame:
    """Read football_players.csv, validate columns, fill missing values."""
    df = pd.read_csv("football_players.csv")

    # Validate all expected columns are present
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        st.error(
            f"The CSV is missing required columns: {missing}. "
            "Please regenerate football_players.csv using generate_data.py."
        )
        st.stop()

    # Fill missing values
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    for col in STRING_COLUMNS:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    return df


# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------

def render_sidebar(df: pd.DataFrame) -> dict:
    """Render sidebar filter widgets; return dict of selected values."""
    st.sidebar.title("⚽ Filters")
    st.sidebar.markdown("---")

    # Season
    all_seasons = sorted(df["season"].unique().tolist())
    selected_seasons = st.sidebar.multiselect(
        "Season",
        options=all_seasons,
        default=all_seasons,
    )

    # Team
    all_teams = sorted(df["team"].unique().tolist())
    selected_teams = st.sidebar.multiselect(
        "Team",
        options=all_teams,
        default=all_teams,
    )

    # Position — show human-readable labels
    all_positions = sorted(df["position"].unique().tolist())
    position_display = {POSITION_LABELS.get(p, p): p for p in all_positions}
    selected_position_labels = st.sidebar.multiselect(
        "Position",
        options=list(position_display.keys()),
        default=list(position_display.keys()),
    )
    selected_positions = [position_display[lbl] for lbl in selected_position_labels]

    # Player
    all_players = sorted(df["player_name"].unique().tolist())
    selected_players = st.sidebar.multiselect(
        "Player",
        options=all_players,
        default=all_players,
    )

    return {
        "seasons": selected_seasons,
        "teams": selected_teams,
        "positions": selected_positions,
        "players": selected_players,
    }


# ---------------------------------------------------------------------------
# Filter application
# ---------------------------------------------------------------------------

def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Chain all four sidebar filter predicates; return filtered DataFrame."""
    filtered = df.copy()

    if filters["seasons"]:
        filtered = filtered[filtered["season"].isin(filters["seasons"])]

    if filters["teams"]:
        filtered = filtered[filtered["team"].isin(filters["teams"])]

    if filters["positions"]:
        filtered = filtered[filtered["position"].isin(filters["positions"])]

    if filters["players"]:
        filtered = filtered[filtered["player_name"].isin(filters["players"])]

    if filtered.empty:
        st.warning(
            "No players match the selected filters. "
            "Please adjust your selections."
        )
        st.stop()

    return filtered


# ---------------------------------------------------------------------------
# Stub page renderers (Sub-Tasks 3–7 will fill these in)
# ---------------------------------------------------------------------------

def render_overview(df: pd.DataFrame) -> None:
    """Render the Overview page: KPI cards, summary stats, and top-10 goals chart."""
    st.subheader("📊 Overview")

    # ── KPI calculations ────────────────────────────────────────────────────
    total_players = len(df)
    total_goals = int(df["goals"].sum())
    total_assists = int(df["assists"].sum())
    total_minutes = int(df["minutes_played"].sum())
    avg_rating = df["rating"].mean()

    # ── Row 1: five KPI metric cards ────────────────────────────────────────
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("👥 Total Players", total_players)
    col2.metric("⚽ Total Goals", total_goals)
    col3.metric("🎯 Total Assists", total_assists)
    col4.metric("⏱️ Total Minutes", f"{total_minutes:,}")
    col5.metric("⭐ Avg Rating", f"{avg_rating:.2f}")

    st.markdown("---")

    # ── Row 2: top scorer and top assister ───────────────────────────────────
    top_scorer_row = df.loc[df["goals"].idxmax()]
    top_assister_row = df.loc[df["assists"].idxmax()]

    col_a, col_b = st.columns(2)
    col_a.metric(
        "🏆 Top Scorer",
        top_scorer_row["player_name"],
        delta=f"{int(top_scorer_row['goals'])} goals",
    )
    col_b.metric(
        "🎖️ Top Assister",
        top_assister_row["player_name"],
        delta=f"{int(top_assister_row['assists'])} assists",
    )

    st.markdown("---")

    # ── Top 10 players by goals bar chart ───────────────────────────────────
    top10 = (
        df[["player_name", "goals"]]
        .sort_values("goals", ascending=False)
        .head(10)
    )
    fig = px.bar(
        top10,
        x="player_name",
        y="goals",
        title="Top 10 Players by Goals",
        labels={"player_name": "Player", "goals": "Goals"},
        template="plotly_dark",
        color_discrete_sequence=["#00ff87"],
    )
    fig.update_layout(height=400, xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)


def render_player_analysis(df: pd.DataFrame) -> None:
    st.subheader("🔍 Player Analysis")

    # Computed column used across both scatter plots
    df = df.copy()
    df["conversion_rate"] = (df["goals"] / df["shots"].replace(0, 1) * 100).round(1)

    # ── Scatter Plot 1: Goals vs Assists ─────────────────────────────────────
    fig1 = px.scatter(
        df,
        x="assists",
        y="goals",
        color="position",
        hover_name="player_name",
        hover_data={"team": True, "rating": True, "conversion_rate": True, "minutes_played": True},
        title="Goals vs Assists by Player",
        template="plotly_dark",
        height=450,
    )
    # Diagonal reference line (y = x) showing equal goals and assists
    axis_max = int(max(df["goals"].max(), df["assists"].max())) + 1
    fig1.add_shape(
        type="line",
        x0=0, y0=0,
        x1=axis_max, y1=axis_max,
        line=dict(color="gray", dash="dash", width=1),
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ── Scatter Plot 2: Shots vs Goals ───────────────────────────────────────
    fig2 = px.scatter(
        df,
        x="shots",
        y="goals",
        color="position",
        hover_name="player_name",
        hover_data={"team": True, "shots_on_target": True, "conversion_rate": True},
        title="Shots vs Goals (Conversion Efficiency)",
        template="plotly_dark",
        height=450,
        trendline="lowess",
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ── Player Comparison Tool ───────────────────────────────────────────────
    st.subheader("⚖️ Player Comparison")

    player_names = sorted(df["player_name"].unique().tolist())

    if len(player_names) < 2:
        st.info("Select at least 2 players to use the comparison tool.")
        return

    col_left, col_right = st.columns(2)
    with col_left:
        player_a = st.selectbox("Player A", options=player_names, index=0)
    with col_right:
        player_b = st.selectbox("Player B", options=player_names, index=1)

    metrics = ["goals", "assists", "shots", "pass_accuracy", "dribbles_completed", "rating"]

    def aggregate_player(name: str) -> dict:
        rows = df[df["player_name"] == name]
        return {
            "goals": int(rows["goals"].sum()),
            "assists": int(rows["assists"].sum()),
            "shots": int(rows["shots"].sum()),
            "pass_accuracy": round(float(rows["pass_accuracy"].mean()), 1),
            "dribbles_completed": int(rows["dribbles_completed"].sum()),
            "rating": round(float(rows["rating"].mean()), 2),
        }

    stats_a = aggregate_player(player_a)
    stats_b = aggregate_player(player_b)

    fig3 = go.Figure(data=[
        go.Bar(
            name=player_a,
            x=metrics,
            y=[stats_a[m] for m in metrics],
            marker_color="#00ff87",
        ),
        go.Bar(
            name=player_b,
            x=metrics,
            y=[stats_b[m] for m in metrics],
            marker_color="#ff6b6b",
        ),
    ])
    fig3.update_layout(
        barmode="group",
        title="Player Comparison",
        template="plotly_dark",
        height=400,
    )
    st.plotly_chart(fig3, use_container_width=True)


def render_team_analysis(df: pd.DataFrame) -> None:
    st.subheader("🏟️ Team Analysis")

    # ------------------------------------------------------------------
    # Aggregation
    # ------------------------------------------------------------------
    team_agg = (
        df.groupby("team")
        .agg(
            goals=("goals", "sum"),
            assists=("assists", "sum"),
            player_count=("player_name", "count"),
            rating=("rating", "mean"),
        )
        .reset_index()
    )
    team_agg["rating"] = team_agg["rating"].round(2)
    team_agg = team_agg.sort_values("goals", ascending=False)

    # ------------------------------------------------------------------
    # Stacked bar: Goals + Assists per Team
    # ------------------------------------------------------------------
    goals_df = team_agg[["team", "goals"]].rename(columns={"goals": "Value"})
    goals_df["Metric"] = "Goals"
    assists_df = team_agg[["team", "assists"]].rename(columns={"assists": "Value"})
    assists_df["Metric"] = "Assists"
    long_df = pd.concat([goals_df, assists_df], ignore_index=True)

    fig = px.bar(
        long_df,
        x="team",
        y="Value",
        color="Metric",
        barmode="stack",
        color_discrete_map={"Goals": "#00ff87", "Assists": "#4ecdc4"},
        title="Goals & Assists per Team",
        template="plotly_dark",
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------
    # Two-column layout: Player Count | Avg Rating
    # ------------------------------------------------------------------
    col_left, col_right = st.columns(2)

    with col_left:
        fig_count = px.bar(
            team_agg,
            x="team",
            y="player_count",
            color_discrete_sequence=["#7c5cd8"],
            title="Players per Team",
            template="plotly_dark",
            height=350,
        )
        st.plotly_chart(fig_count, use_container_width=True)

    with col_right:
        fig_rating = px.bar(
            team_agg,
            x="team",
            y="rating",
            color_discrete_sequence=["#ff6b6b"],
            title="Average Player Rating per Team",
            template="plotly_dark",
            height=350,
        )
        fig_rating.update_layout(yaxis_range=[5, 9.5])
        st.plotly_chart(fig_rating, use_container_width=True)

    # ------------------------------------------------------------------
    # Top Players Section
    # ------------------------------------------------------------------
    st.subheader("🏆 Top Players")

    col_scorers, col_assisters = st.columns(2)

    with col_scorers:
        st.markdown("**Top 5 Scorers**")
        top_scorers = (
            df[["player_name", "team", "position", "goals"]]
            .sort_values("goals", ascending=False)
            .head(5)
        )
        st.dataframe(top_scorers.reset_index(drop=True), use_container_width=True)

    with col_assisters:
        st.markdown("**Top 5 Assisters**")
        top_assisters = (
            df[["player_name", "team", "position", "assists"]]
            .sort_values("assists", ascending=False)
            .head(5)
        )
        st.dataframe(top_assisters.reset_index(drop=True), use_container_width=True)


def render_position_analysis(df: pd.DataFrame) -> None:
    st.subheader("📐 Position Analysis")

    # ── Box Plot: Player Rating Distribution by Position ────────────────────
    position_order = ["GK", "DEF", "MID", "FWD"]
    fig_box = px.box(
        df,
        x="position",
        y="rating",
        color="position",
        category_orders={"position": position_order},
        title="Player Rating Distribution by Position",
        template="plotly_dark",
        height=400,
    )
    fig_box.update_layout(showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

    # ── Two-column layout: Heatmap (left) | Goals per 90 Bar (right) ────────
    col_left, col_right = st.columns(2)

    # ── Heatmap: Average Stats per Position ─────────────────────────────────
    with col_left:
        stat_cols = ["goals", "assists", "pass_accuracy", "dribbles_completed", "clean_sheets"]
        pivot = (
            df.groupby("position")[stat_cols]
            .mean()
            .round(1)
            .reindex([p for p in position_order if p in df["position"].unique()])
        )
        fig_heat = px.imshow(
            pivot,
            color_continuous_scale="Greens",
            text_auto=True,
            title="Average Stats by Position",
            template="plotly_dark",
            height=350,
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    # ── Bar Chart: Goals per 90 by Position ─────────────────────────────────
    with col_right:
        df_g90 = df.copy()
        df_g90["goals_per_90"] = (
            df_g90["goals"] / (df_g90["minutes_played"].replace(0, np.nan) / 90)
        ).fillna(0)
        goals_per_90 = (
            df_g90.groupby("position")["goals_per_90"]
            .mean()
            .round(2)
            .reindex([p for p in position_order if p in df_g90["position"].unique()])
            .reset_index()
        )
        fig_g90 = px.bar(
            goals_per_90,
            x="position",
            y="goals_per_90",
            color_discrete_sequence=["#00ff87"],
            title="Average Goals per 90 Minutes by Position",
            template="plotly_dark",
            height=350,
        )
        st.plotly_chart(fig_g90, use_container_width=True)


def render_data_table(df: pd.DataFrame) -> None:
    st.subheader("📋 Player Statistics Table")

    # ── Search input ─────────────────────────────────────────────────────────
    search = st.text_input("🔍 Search by player name", placeholder="e.g. Marcus Silva")
    if search:
        df_show = df[df["player_name"].str.contains(search, case=False, na=False)]
    else:
        df_show = df.copy()
    st.caption(f"Showing {len(df_show)} player(s)")

    # ── Column reordering (drop player_id) ───────────────────────────────────
    col_order = [
        "player_name", "team", "position", "season", "age",
        "matches_played", "minutes_played", "goals", "assists",
        "shots", "shots_on_target", "pass_accuracy", "dribbles_completed",
        "yellow_cards", "red_cards", "clean_sheets", "rating",
    ]

    # ── Dataframe display ─────────────────────────────────────────────────────
    st.dataframe(df_show[col_order], use_container_width=True, height=400)

    # ── CSV download button ───────────────────────────────────────────────────
    csv_data = df_show.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_data,
        file_name="football_players_filtered.csv",
        mime="text/csv",
    )

    # ── Summary statistics expander ───────────────────────────────────────────
    with st.expander("📊 Summary Statistics"):
        st.dataframe(
            df_show[["goals", "assists", "rating", "pass_accuracy", "minutes_played"]]
            .describe()
            .round(2),
            use_container_width=True,
        )


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

PAGE_OPTIONS = [
    "Overview",
    "Player Analysis",
    "Team Analysis",
    "Position Analysis",
    "Data Table",
]

PAGE_ROUTER = {
    "Overview": render_overview,
    "Player Analysis": render_player_analysis,
    "Team Analysis": render_team_analysis,
    "Position Analysis": render_position_analysis,
    "Data Table": render_data_table,
}


def main() -> None:
    # Load and validate data
    df = load_data()

    # Synthetic data disclaimer — shown on every page
    st.info(
        "ℹ️ This dashboard uses synthetic data for demonstration purposes only. "
        "All player names, teams, and statistics are fictional."
    )

    # Sidebar filters
    filters = render_sidebar(df)
    filtered_df = apply_filters(df, filters)

    # Page navigation
    st.sidebar.markdown("---")
    st.sidebar.subheader("Navigation")
    selected_page = st.sidebar.radio(
        "Go to",
        options=PAGE_OPTIONS,
        label_visibility="collapsed",
    )

    # Route to the selected page
    PAGE_ROUTER[selected_page](filtered_df)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
