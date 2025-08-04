import streamlit as st
import pandas as pd
import os

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MONEYLINE_CSV = os.path.join(BASE_DIR, "2025-08-04_predictions.csv")
TOTALS_CSV = os.path.join(BASE_DIR, "2025-08-04_totals_predictions.csv")

# Load Moneyline CSV
if os.path.isfile(MONEYLINE_CSV):
    df_moneyline = pd.read_csv(MONEYLINE_CSV)
else:
    st.warning("Moneyline CSV not found. Please upload it.")
    uploaded_moneyline = st.file_uploader("Upload Moneyline CSV", type=["csv"], key="moneyline")
    if uploaded_moneyline:
        df_moneyline = pd.read_csv(uploaded_moneyline)
    else:
        st.stop()

# Load Totals CSV
if os.path.isfile(TOTALS_CSV):
    df_totals = pd.read_csv(TOTALS_CSV)
else:
    st.warning("Totals CSV not found. Please upload it.")
    uploaded_totals = st.file_uploader("Upload Totals CSV", type=["csv"], key="totals")
    if uploaded_totals:
        df_totals = pd.read_csv(uploaded_totals)
    else:
        df_totals = pd.DataFrame()

# Example team logos mapping (replace/add more teams)
team_logos = {
    # AL East
    'New York Yankees': 'https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png',
    'Boston Red Sox': 'https://a.espncdn.com/i/teamlogos/mlb/500/bos.png',
    'Toronto Blue Jays': 'https://a.espncdn.com/i/teamlogos/mlb/500/tor.png',
    'Tampa Bay Rays': 'https://a.espncdn.com/i/teamlogos/mlb/500/tb.png',
    'Baltimore Orioles': 'https://a.espncdn.com/i/teamlogos/mlb/500/bal.png',

    # AL Central
    'Cleveland Guardians': 'https://a.espncdn.com/i/teamlogos/mlb/500/cle.png',
    'Chicago White Sox': 'https://a.espncdn.com/i/teamlogos/mlb/500/cws.png',
    'Minnesota Twins': 'https://a.espncdn.com/i/teamlogos/mlb/500/min.png',
    'Detroit Tigers': 'https://a.espncdn.com/i/teamlogos/mlb/500/det.png',
    'Kansas City Royals': 'https://a.espncdn.com/i/teamlogos/mlb/500/kc.png',

    # AL West
    'Houston Astros': 'https://a.espncdn.com/i/teamlogos/mlb/500/hou.png',
    'Los Angeles Angels': 'https://a.espncdn.com/i/teamlogos/mlb/500/laa.png',
    'Oakland Athletics': 'https://a.espncdn.com/i/teamlogos/mlb/500/oak.png',
    'Seattle Mariners': 'https://a.espncdn.com/i/teamlogos/mlb/500/sea.png',
    'Texas Rangers': 'https://a.espncdn.com/i/teamlogos/mlb/500/tex.png',

    # NL East
    'Atlanta Braves': 'https://a.espncdn.com/i/teamlogos/mlb/500/atl.png',
    'New York Mets': 'https://a.espncdn.com/i/teamlogos/mlb/500/nym.png',
    'Philadelphia Phillies': 'https://a.espncdn.com/i/teamlogos/mlb/500/phi.png',
    'Miami Marlins': 'https://a.espncdn.com/i/teamlogos/mlb/500/mia.png',
    'Washington Nationals': 'https://a.espncdn.com/i/teamlogos/mlb/500/wsh.png',

    # NL Central
    'Chicago Cubs': 'https://a.espncdn.com/i/teamlogos/mlb/500/chc.png',
    'St. Louis Cardinals': 'https://a.espncdn.com/i/teamlogos/mlb/500/stl.png',
    'Milwaukee Brewers': 'https://a.espncdn.com/i/teamlogos/mlb/500/mil.png',
    'Pittsburgh Pirates': 'https://a.espncdn.com/i/teamlogos/mlb/500/pit.png',
    'Cincinnati Reds': 'https://a.espncdn.com/i/teamlogos/mlb/500/cin.png',

    # NL West
    'Los Angeles Dodgers': 'https://a.espncdn.com/i/teamlogos/mlb/500/lad.png',
    'San Francisco Giants': 'https://a.espncdn.com/i/teamlogos/mlb/500/sf.png',
    'San Diego Padres': 'https://a.espncdn.com/i/teamlogos/mlb/500/sd.png',
    'Arizona Diamondbacks': 'https://a.espncdn.com/i/teamlogos/mlb/500/ari.png',
    'Colorado Rockies': 'https://a.espncdn.com/i/teamlogos/mlb/500/col.png'
}

# Add logos to both DataFrames
for df in [df_moneyline, df_totals]:
    if not df.empty:
        df['team_logo'] = df['team'].map(team_logos)
        df['opponent_logo'] = df['opponent'].map(team_logos)

# --- Streamlit Page Config ---
st.set_page_config(page_title="MLB Matchup Predictions", layout="wide")

# Sidebar Filters
teams = sorted(df_moneyline['team'].unique())
selected_team = st.sidebar.selectbox("Filter by Team", ["All"] + teams)
if selected_team != "All":
    df_moneyline = df_moneyline[df_moneyline["team"] == selected_team]
    df_totals = df_totals[df_totals["team"] == selected_team]

sort_option = st.sidebar.radio("Sort by", ["Date", "Win Probability"])
if sort_option == "Win Probability":
    df_moneyline = df_moneyline.sort_values(by="team_win_next_pred", ascending=False)
    df_totals = df_totals.sort_values(by="model_confidence", ascending=False)

# Tabs for Moneyline and Totals
tab1, tab2 = st.tabs(["💰 Moneyline Predictions", "📊 Totals Predictions"])

# ================================
# GLOBAL CSS STYLES
# ================================
st.markdown("""
<style>
body { background-color: #f7f7f7 !important; color: #222; font-family: 'Segoe UI', sans-serif; }
[data-testid="stAppViewContainer"] { background-color: #f7f7f7; }
[data-testid="stHeader"] { background: none; }

.scoreboard-header {
    font-size: 36px; font-weight: bold; text-align: center; color: #1a3d7c;
    margin-bottom: 30px; margin-top: 10px;
}
.date-header {
    font-size: 22px; font-weight: bold; color: #1a1a1a;
    margin: 40px 0 20px; border-bottom: 2px solid #ddd; padding-bottom: 8px;
}

/* Game card */
.game-card {
    background: #ffffff; border: 1px solid #e6e6e6; border-radius: 12px;
    padding: 20px; margin-bottom: 25px; text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 10px rgba(0,0,0,0.06); max-width: 300px;
    margin-left: auto; margin-right: auto;
}
.game-card:hover { transform: translateY(-4px); box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.12); }

/* Logo container */
.logo-container {
    background-color: #ffffff; border-radius: 50%;
    display: flex; justify-content: center; align-items: center;
    width: 70px; height: 70px; margin: 0 auto 8px auto;
    border: 3px solid transparent; overflow: hidden;
}
.logo-container img { width: 100%; height: 100%; object-fit: contain; padding: 8px; }

.team-name { font-weight: bold; font-size: 16px; margin-top: 6px; color: #222; }
.pitcher { font-size: 13px; color: #666; margin-bottom: 6px; }
.win-prob { font-size: 14px; margin-top: 6px; font-weight: bold; }
.prob-bar { height: 6px; border-radius: 3px; margin-top: 4px; transition: width 0.8s ease-in-out; }
</style>
""", unsafe_allow_html=True)

# ================================
# TAB 1: MONEYLINE
# ================================
with tab1:
    st.markdown("<div class='scoreboard-header'>MLB Moneyline Predictions</div>", unsafe_allow_html=True)
    for game_date, games_on_date in df_moneyline.groupby("date"):
        st.markdown(f"<div class='date-header'>{game_date}</div>", unsafe_allow_html=True)
        games_list = list(games_on_date.iterrows())
        cards_per_row = 4 if len(games_list) > 6 else 3
        for i in range(0, len(games_list), cards_per_row):
            cols = st.columns(cards_per_row, gap="large")
            for col_idx in range(cards_per_row):
                if i + col_idx < len(games_list):
                    _, game = games_list[i + col_idx]
                    team_prob = float(game['team_win_next_pred']) * 100
                    opp_prob = 100 - team_prob
                    with cols[col_idx]:
                        st.markdown(f"""
                            <div class="game-card">
                                <div style="display:flex; justify-content:space-around; align-items:center;">
                                    <div>
                                        <div class="logo-container"><img src="{game['team_logo']}"/></div>
                                        <div class="team-name">{game['team']}</div>
                                        <div class="pitcher">{game['home_pitcher']}</div>
                                        <div class="win-prob" style="color:{'green' if team_prob>=50 else 'red'};">{team_prob:.1f}%</div>
                                        <div class="prob-bar" style="width:{team_prob}%; background:{'green' if team_prob>=50 else 'red'};"></div>
                                    </div>
                                    <div style="font-weight:bold; font-size:16px; margin:0 10px; color:#555;">VS</div>
                                    <div>
                                        <div class="logo-container"><img src="{game['opponent_logo']}"/></div>
                                        <div class="team-name">{game['opponent']}</div>
                                        <div class="pitcher">{game['away_pitcher']}</div>
                                        <div class="win-prob" style="color:{'green' if opp_prob>=50 else 'red'};">{opp_prob:.1f}%</div>
                                        <div class="prob-bar" style="width:{opp_prob}%; background:{'green' if opp_prob>=50 else 'red'};"></div>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

# ================================
# TAB 2: TOTALS
# ================================
with tab2:
    st.markdown("<div class='scoreboard-header'>MLB Totals Predictions</div>", unsafe_allow_html=True)
    for game_date, games_on_date in df_totals.groupby("date"):
        st.markdown(f"<div class='date-header'>{game_date}</div>", unsafe_allow_html=True)
        games_list = list(games_on_date.iterrows())
        cards_per_row = 4 if len(games_list) > 6 else 3
        for i in range(0, len(games_list), cards_per_row):
            cols = st.columns(cards_per_row, gap="large")
            for col_idx in range(cards_per_row):
                if i + col_idx < len(games_list):
                    _, game = games_list[i + col_idx]
                    prob = float(game['model_confidence']) * 100
                    color = 'green' if game['model_pred'] == 'over' else 'red'
                    with cols[col_idx]:
                        st.markdown(f"""
                            <div class="game-card">
                                <div style="display:flex; justify-content:space-around; align-items:center;">
                                    <div>
                                        <div class="logo-container"><img src="{game['team_logo']}"/></div>
                                        <div class="team-name">{game['team']}</div>
                                        <div class="pitcher">{game['home_pitcher']}</div>
                                        <div class="win-prob" style="color:{color};">
                                            {game['model_pred'].capitalize()} {game['bookie_total']} ({prob:.1f}%)
                                        </div>
                                    </div>
                                    <div style="font-weight:bold; font-size:16px; margin:0 10px; color:#555;">VS</div>
                                    <div>
                                        <div class="logo-container"><img src="{game['opponent_logo']}"/></div>
                                        <div class="team-name">{game['opponent']}</div>
                                        <div class="pitcher">{game['away_pitcher']}</div>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)