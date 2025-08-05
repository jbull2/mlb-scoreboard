import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from data_loader import load_elo_predictions, load_and_merge_predictions
from team_logos import TEAM_LOGOS

# --- Page Config ---
st.set_page_config(page_title="MLB Matchup Predictions", layout="wide")

# --- Load Data ---
df_moneyline = load_elo_predictions("2025-08-05_elo_predictions.csv")
df_totals, df_runline = load_and_merge_predictions(
    "2025-08-05_totals_predictions.csv",
    "2025-08-05_runline_predictions.csv",
    "mlb_schedule.csv"
)

# --- Map Logos ---
for df in [df_moneyline, df_totals, df_runline]:
    df['team_logo'] = df['team'].map(TEAM_LOGOS)
    df['opponent_logo'] = df['opponent'].map(TEAM_LOGOS)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["Moneyline", "Totals", "Runline"])

def render_two_row_table(df, table_type):
    """Builds a full HTML table for 2-rows-per-game display."""
    # Sort games by start_time (convert to datetime)
    df['start_time_sort'] = pd.to_datetime(df['start_time'], format='%I:%M %p', errors='coerce')
    df = df.sort_values('start_time_sort')

    col_header = "Win Probability" if table_type == "moneyline" else "Prediction"

    table_html = f"""
    <style>
    .scoreboard-table {{
        width: 100%; /* Full width table */
        border-collapse: collapse;
        table-layout: fixed; /* Even spacing across page */
        margin-bottom: 30px;
        font-family: Arial, sans-serif;
    }}
    .scoreboard-table th {{
        background: #0d2040;
        color: white;
        font-weight: bold;
        padding: 12px;
        white-space: nowrap;
    }}
    /* Center align Start Time and Win Probability headings */
    .scoreboard-table th:first-child,
    .scoreboard-table th:last-child {{
        text-align: center;
    }}
    /* Left align Teams and Pitchers headings */
    .scoreboard-table th:nth-child(2),
    .scoreboard-table th:nth-child(3) {{
        text-align: left;
    }}
    .scoreboard-table td {{
        padding: 12px;
        border-bottom: 1px solid #ddd;
        font-size: 14px;
        vertical-align: middle;
    }}
    /* Left align teams and pitchers */
    .scoreboard-table td.team-col, 
    .scoreboard-table td.pitcher-col {{
        text-align: left;
        white-space: nowrap;
    }}
    /* Bold team names only */
    .scoreboard-table td.team-col span {{
        font-weight: bold;
    }}
    /* Alternate shading */
    .scoreboard-table tr.game-block:nth-child(4n-1),
    .scoreboard-table tr.game-block:nth-child(4n) {{
        background: #f9f9f9;
    }}
    /* Divider after each matchup */
    .scoreboard-table tr.divider td {{
        border-bottom: 3px solid #bbb;
    }}
    /* Logos aligned with text */
    .scoreboard-table img {{
        vertical-align: middle;
        margin-right: 8px;
        height: 22px;
        width: auto;
    }}
    /* Wider columns proportionally */
    .scoreboard-table td:nth-child(1) {{ width: 12%; }}
    .scoreboard-table td:nth-child(2) {{ width: 38%; }}
    .scoreboard-table td:nth-child(3) {{ width: 30%; }}
    .scoreboard-table td:nth-child(4) {{ width: 20%; }}
    </style>
    <table class="scoreboard-table">
        <thead>
            <tr>
                <th>Start Time</th>
                <th>Teams</th>
                <th>Pitchers</th>
                <th>{col_header}</th>
            </tr>
        </thead>
        <tbody>
    """

    for _, game in df.iterrows():
        if table_type == "moneyline":
            team_prob = float(game['team_win_next_pred']) * 100
            opp_prob = 100 - team_prob

            table_html += f"""
            <tr class="game-block">
                <td rowspan='2'>{game['start_time']}</td>
                <td class="team-col"><img src='{game['opponent_logo']}'/> <span>{game['opponent']}</span></td>
                <td class="pitcher-col">{game['away_pitcher']}</td>
                <td>{opp_prob:.1f}%</td>
            </tr>
            <tr class="game-block divider">
                <td class="team-col"><img src='{game['team_logo']}'/> <span>{game['team']}</span></td>
                <td class="pitcher-col">{game['home_pitcher']}</td>
                <td>{team_prob:.1f}%</td>
            </tr>
            """
        elif table_type == "totals":
            prob = float(game['model_confidence']) * 100
            table_html += f"""
            <tr class="game-block">
                <td rowspan='2'>{game['start_time']}</td>
                <td class="team-col"><img src='{game['opponent_logo']}'/> <span>{game['opponent']}</span></td>
                <td class="pitcher-col">{game['away_pitcher']}</td>
                <td rowspan='2'>{game['model_pred'].capitalize()} {game['bookie_total']} ({prob:.1f}%)</td>
            </tr>
            <tr class="game-block divider">
                <td class="team-col"><img src='{game['team_logo']}'/> <span>{game['team']}</span></td>
                <td class="pitcher-col">{game['home_pitcher']}</td>
            </tr>
            """
        elif table_type == "runline":
            confidence = float(game['confidence']) * 100
            spread_value = float(game['home_spread']) if game['pred_winner'] == game['team'] else float(game['away_spread'])
            spread_formatted = f"{'+' if spread_value > 0 else ''}{spread_value:.1f}"

            table_html += f"""
            <tr class="game-block">
                <td rowspan='2'>{game['start_time']}</td>
                <td class="team-col"><img src='{game['opponent_logo']}'/> <span>{game['opponent']}</span></td>
                <td class="pitcher-col">{game['away_pitcher']}</td>
                <td rowspan='2'>Predicted: {game['pred_winner']} {spread_formatted} ({confidence:.1f}%)</td>
            </tr>
            <tr class="game-block divider">
                <td class="team-col"><img src='{game['team_logo']}'/> <span>{game['team']}</span></td>
                <td class="pitcher-col">{game['home_pitcher']}</td>
            </tr>
            """

    table_html += "</tbody></table>"
    return table_html

# --- Render Tabs with components.html ---
with tab1:
    st.markdown("<h2>MLB Moneyline Predictions</h2>", unsafe_allow_html=True)
    for game_date, games_on_date in df_moneyline.groupby("date"):
        st.markdown(f"<h3>{game_date}</h3>", unsafe_allow_html=True)
        components.html(render_two_row_table(games_on_date, "moneyline"), height=600, scrolling=True)

with tab2:
    st.markdown("<h2>MLB Totals Predictions</h2>", unsafe_allow_html=True)
    for game_date, games_on_date in df_totals.groupby("date"):
        st.markdown(f"<h3>{game_date}</h3>", unsafe_allow_html=True)
        components.html(render_two_row_table(games_on_date, "totals"), height=600, scrolling=True)

with tab3:
    st.markdown("<h2>MLB Runline Predictions</h2>", unsafe_allow_html=True)
    for game_date, games_on_date in df_runline.groupby("date"):
        st.markdown(f"<h3>{game_date}</h3>", unsafe_allow_html=True)
        components.html(render_two_row_table(games_on_date, "runline"), height=600, scrolling=True)
