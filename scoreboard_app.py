import streamlit as st
import pandas as pd
import os

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MONEYLINE_CSV = os.path.join(BASE_DIR, "2025-08-04_predictions.csv")
TOTALS_CSV = os.path.join(BASE_DIR, "2025-08-04_totals_predictions.csv")
RUNLINE_CSV = os.path.join(BASE_DIR, "2025-08-04_runline_predictions.csv")
TODAYS_GAMES_CSV = os.path.join(BASE_DIR, "mlb_schedule.csv")

# Load CSVs
def load_csv(file_path, upload_key):
    if os.path.isfile(file_path):
        return pd.read_csv(file_path)
    else:
        st.warning(f"{os.path.basename(file_path)} not found. Please upload it.")
        uploaded = st.file_uploader(f"Upload {os.path.basename(file_path)}", type=["csv"], key=upload_key)
        return pd.read_csv(uploaded) if uploaded else pd.DataFrame()

df_moneyline = load_csv(MONEYLINE_CSV, "moneyline")
df_totals = load_csv(TOTALS_CSV, "totals")
df_runline = load_csv(RUNLINE_CSV, "runline")
df_schedule = load_csv(TODAYS_GAMES_CSV, "schedule")

# Merge schedule times
for name, df in zip(["moneyline", "totals", "runline"], [df_moneyline, df_totals, df_runline]):
    if not df.empty:
        if not df_schedule.empty:
            merged_df = df.merge(df_schedule[['team', 'opponent', 'start_time']], on=['team', 'opponent'], how='left')
            if name == "moneyline": df_moneyline = merged_df
            elif name == "totals": df_totals = merged_df
            else: df_runline = merged_df
        else:
            df['start_time'] = 'TBD'

# Sort by start time
for df in [df_moneyline, df_totals, df_runline]:
    if 'start_time' in df.columns:
        df['start_time_sort'] = pd.to_datetime(df['start_time'], format='%I:%M %p', errors='coerce')
        df.sort_values(by=['date', 'start_time_sort'], inplace=True)

# --- Streamlit Page Config ---
st.set_page_config(page_title="MLB Matchup Predictions", layout="wide")

# Example team logos mapping (replace/add more teams)
team_logos = {
    'New York Yankees': 'https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png',
    'Boston Red Sox': 'https://a.espncdn.com/i/teamlogos/mlb/500/bos.png',
    'Toronto Blue Jays': 'https://a.espncdn.com/i/teamlogos/mlb/500/tor.png',
    'Tampa Bay Rays': 'https://a.espncdn.com/i/teamlogos/mlb/500/tb.png',
    'Baltimore Orioles': 'https://a.espncdn.com/i/teamlogos/mlb/500/bal.png',
    'Cleveland Guardians': 'https://a.espncdn.com/i/teamlogos/mlb/500/cle.png',
    'Chicago White Sox': 'https://a.espncdn.com/i/teamlogos/mlb/500/cws.png',
    'Minnesota Twins': 'https://a.espncdn.com/i/teamlogos/mlb/500/min.png',
    'Detroit Tigers': 'https://a.espncdn.com/i/teamlogos/mlb/500/det.png',
    'Kansas City Royals': 'https://a.espncdn.com/i/teamlogos/mlb/500/kc.png',
    'Houston Astros': 'https://a.espncdn.com/i/teamlogos/mlb/500/hou.png',
    'Los Angeles Angels': 'https://a.espncdn.com/i/teamlogos/mlb/500/laa.png',
    'Oakland Athletics': 'https://a.espncdn.com/i/teamlogos/mlb/500/oak.png',
    'Seattle Mariners': 'https://a.espncdn.com/i/teamlogos/mlb/500/sea.png',
    'Texas Rangers': 'https://a.espncdn.com/i/teamlogos/mlb/500/tex.png',
    'Atlanta Braves': 'https://a.espncdn.com/i/teamlogos/mlb/500/atl.png',
    'New York Mets': 'https://a.espncdn.com/i/teamlogos/mlb/500/nym.png',
    'Philadelphia Phillies': 'https://a.espncdn.com/i/teamlogos/mlb/500/phi.png',
    'Miami Marlins': 'https://a.espncdn.com/i/teamlogos/mlb/500/mia.png',
    'Washington Nationals': 'https://a.espncdn.com/i/teamlogos/mlb/500/wsh.png',
    'Chicago Cubs': 'https://a.espncdn.com/i/teamlogos/mlb/500/chc.png',
    'St. Louis Cardinals': 'https://a.espncdn.com/i/teamlogos/mlb/500/stl.png',
    'Milwaukee Brewers': 'https://a.espncdn.com/i/teamlogos/mlb/500/mil.png',
    'Pittsburgh Pirates': 'https://a.espncdn.com/i/teamlogos/mlb/500/pit.png',
    'Cincinnati Reds': 'https://a.espncdn.com/i/teamlogos/mlb/500/cin.png',
    'Los Angeles Dodgers': 'https://a.espncdn.com/i/teamlogos/mlb/500/lad.png',
    'San Francisco Giants': 'https://a.espncdn.com/i/teamlogos/mlb/500/sf.png',
    'San Diego Padres': 'https://a.espncdn.com/i/teamlogos/mlb/500/sd.png',
    'Arizona Diamondbacks': 'https://a.espncdn.com/i/teamlogos/mlb/500/ari.png',
    'Colorado Rockies': 'https://a.espncdn.com/i/teamlogos/mlb/500/col.png'
}

# Add logos to all DataFrames
for df in [df_moneyline, df_totals, df_runline]:
    if not df.empty:
        df['team_logo'] = df['team'].map(team_logos)
        df['opponent_logo'] = df['opponent'].map(team_logos)

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
    margin-bottom: 35px; margin-top: 15px;
}
.date-header {
    font-size: 22px; font-weight: bold; color: #1a1a1a;
    margin: 50px 0 25px; border-bottom: 2px solid #ddd; padding-bottom: 8px;
}
.game-card {
    background: #ffffff; border: 1px solid #e6e6e6; border-radius: 14px;
    padding: 20px; text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    display: flex; flex-direction: column; justify-content: flex-start;
    height: 300px; width: 330px; margin: 10px auto 25px auto;
}
.game-card:hover { transform: translateY(-4px); box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.14); }
.start-time {
    font-size: 16px; font-weight: 600; color: #1a3d7c;
    background: #eef3fc; border-radius: 8px; padding: 4px 8px;
    display: inline-block; margin-bottom: 10px;
}
.logo-container {
    background-color: #ffffff; border-radius: 50%;
    display: flex; justify-content: center; align-items: center;
    width: 75px; height: 75px; margin: 0 auto 8px auto;
    border: 3px solid transparent; overflow: hidden;
}
.logo-container img { width: 100%; height: 100%; object-fit: contain; padding: 8px; }
.team-name { font-weight: bold; font-size: 17px; color: #222; min-height: 42px; }
.pitcher { font-size: 14px; color: #666; margin-bottom: 6px; min-height: 20px; }
.win-prob { font-size: 15px; font-weight: bold; margin-top: 6px; min-height: 22px; }
</style>
""", unsafe_allow_html=True)

# ================================
# TABS
# ================================
tab1, tab2, tab3 = st.tabs(["Moneyline Predictions", "Totals Predictions", "Runline Predictions"])

# MONEYLINE TAB
# MONEYLINE TAB
with tab1:
    st.markdown("<div class='scoreboard-header'>MLB Moneyline Predictions</div>", unsafe_allow_html=True)
    for game_date, games_on_date in df_moneyline.groupby("date"):
        st.markdown(f"<div class='date-header'>{game_date}</div>", unsafe_allow_html=True)
        games_list = list(games_on_date.iterrows())
        cards_per_row = 5
        
        for i in range(0, len(games_list), cards_per_row):
            cols = st.columns(cards_per_row, gap="large")  # Create columns for each row
            
            for col_idx in range(cards_per_row):
                if i + col_idx < len(games_list):
                    _, game = games_list[i + col_idx]
                    team_prob = float(game['team_win_next_pred']) * 100
                    opp_prob = 100 - team_prob
                    
                    # ✅ Place each card inside its respective column
                    with cols[col_idx]:
                        st.markdown(f"""
                            <div class="game-card">
                                <div class="start-time">{game['start_time']}</div>
                                <div style="display:flex; justify-content:space-around; align-items:center;">
                                    <div>
                                        <div class="logo-container"><img src="{game['team_logo']}"/></div>
                                        <div class="team-name">{game['team']}</div>
                                        <div class="pitcher">{game['home_pitcher']}</div>
                                        <div class="win-prob">{team_prob:.1f}%</div>
                                    </div>
                                    <div style="font-weight:bold; font-size:16px; margin:0 10px; color:#555;">VS</div>
                                    <div>
                                        <div class="logo-container"><img src="{game['opponent_logo']}"/></div>
                                        <div class="team-name">{game['opponent']}</div>
                                        <div class="pitcher">{game['away_pitcher']}</div>
                                        <div class="win-prob">{opp_prob:.1f}%</div>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

# TOTALS TAB
with tab2:
    st.markdown("<div class='scoreboard-header'>MLB Totals Predictions</div>", unsafe_allow_html=True)
    for game_date, games_on_date in df_totals.groupby("date"):
        st.markdown(f"<div class='date-header'>{game_date}</div>", unsafe_allow_html=True)
        games_list = list(games_on_date.iterrows())
        cards_per_row = 5

        for i in range(0, len(games_list), cards_per_row):
            cols = st.columns(cards_per_row, gap="large")  # Create columns per row
            
            for col_idx in range(cards_per_row):
                if i + col_idx < len(games_list):
                    _, game = games_list[i + col_idx]
                    prob = float(game['model_confidence']) * 100

                    # ✅ Place card inside the column
                    with cols[col_idx]:
                        st.markdown(f"""
                            <div class="game-card">
                                <div class="start-time">{game['start_time']}</div>
                                <div style="display:flex; justify-content:space-around; align-items:center;">
                                    <div>
                                        <div class="logo-container"><img src="{game['team_logo']}"/></div>
                                        <div class="team-name">{game['team']}</div>
                                        <div class="pitcher">{game['home_pitcher']}</div>
                                    </div>
                                    <div style="font-weight:bold; font-size:16px; margin:0 10px; color:#555;">VS</div>
                                    <div>
                                        <div class="logo-container"><img src="{game['opponent_logo']}"/></div>
                                        <div class="team-name">{game['opponent']}</div>
                                        <div class="pitcher">{game['away_pitcher']}</div>
                                    </div>
                                </div>
                                <div style="margin-top:14px; font-size:15px; font-weight:600;">
                                    {game['model_pred'].capitalize()} {game['bookie_total']} ({prob:.1f}%)
                                </div>
                            </div>
                        """, unsafe_allow_html=True)


# RUNLINE TAB
with tab3:
    st.markdown("<div class='scoreboard-header'>MLB Runline Predictions</div>", unsafe_allow_html=True)
    for game_date, games_on_date in df_runline.groupby("date"):
        st.markdown(f"<div class='date-header'>{game_date}</div>", unsafe_allow_html=True)
        games_list = list(games_on_date.iterrows())
        cards_per_row = 5

        for i in range(0, len(games_list), cards_per_row):
            cols = st.columns(cards_per_row, gap="large")  # Create columns per row
            
            for col_idx in range(cards_per_row):
                if i + col_idx < len(games_list):
                    _, game = games_list[i + col_idx]
                    confidence = float(game['confidence']) * 100
                    
                    # Determine predicted team's spread and format sign
                    if game['pred_winner'] == game['team']:
                        spread_value = float(game['home_spread'])
                        odds = game['home_spread_odds']
                    else:
                        spread_value = float(game['away_spread'])
                        odds = game['away_spread_odds']

                    spread_formatted = f"{'+' if spread_value > 0 else ''}{spread_value:.1f}"

                    with cols[col_idx]:
                        st.markdown(f"""
                            <div class="game-card">
                                <div class="start-time">{game.get('start_time', 'TBD')}</div>
                                <div style="display:flex; justify-content:space-around; align-items:center;">
                                    <div>
                                        <div class="logo-container"><img src="{game['team_logo']}"/></div>
                                        <div class="team-name">{game['team']}</div>
                                        <div class="pitcher">{game['home_pitcher']}</div>
                                    </div>
                                    <div style="font-weight:bold; font-size:16px; margin:0 10px; color:#555;">VS</div>
                                    <div>
                                        <div class="logo-container"><img src="{game['opponent_logo']}"/></div>
                                        <div class="team-name">{game['opponent']}</div>
                                        <div class="pitcher">{game['away_pitcher']}</div>
                                    </div>
                                </div>
                                <div style="margin-top:14px; font-size:15px; font-weight:600;">
                                    Predicted: {game['pred_winner']} {spread_formatted} ({confidence:.1f}%)
                                </div>
                            </div>
                        """, unsafe_allow_html=True)