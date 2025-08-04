import streamlit as st
import pandas as pd

# Load predictions CSV
# Read predictions CSV (if already saved)
df_future_games = pd.read_csv('2025-08-04_predictions.csv')

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

# Map logos
df_future_games['team_logo'] = df_future_games['team'].map(team_logos)
df_future_games['opponent_logo'] = df_future_games['opponent'].map(team_logos)

import streamlit as st
import pandas as pd
import altair as alt

# Streamlit Page Config
st.set_page_config(page_title="MLB Matchup Predictions", layout="wide")

# Sidebar Filters
teams = sorted(df_future_games['team'].unique())
selected_team = st.sidebar.selectbox("Filter by Team", ["All"] + teams)
if selected_team != "All":
    df_future_games = df_future_games[df_future_games["team"] == selected_team]

sort_option = st.sidebar.radio("Sort by", ["Date", "Win Probability"])
if sort_option == "Win Probability":
    df_future_games = df_future_games.sort_values(by="team_win_next_pred", ascending=False)

# Updated CSS for Light Theme with Extra Spacing
st.markdown("""
    <style>
    body {
        background-color: #f7f7f7 !important;
        color: #222;
        font-family: 'Segoe UI', sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #f7f7f7;
    }
    [data-testid="stHeader"] {
        background: none;
    }

    .scoreboard-header {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #1a3d7c; /* Navy Blue */
        margin-bottom: 40px;
        margin-top: 10px;
    }

    .date-header {
        font-size: 22px;
        font-weight: bold;
        color: #1a1a1a;
        margin: 50px 0 25px;
        border-bottom: 2px solid #ddd;
        padding-bottom: 8px;
    }

    /* Game card styling */
    .game-card {
        background: #ffffff;
        border: 1px solid #e6e6e6;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 30px; /* Extra spacing between rows */
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    }
    .game-card:hover {
        transform: translateY(-4px);
        box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.12);
    }

    /* Logo styling */
    .logo-container {
        background-color: #ffffff;
        border-radius: 50%;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        width: 65px;
        height: 65px;
        margin-bottom: 8px;
        border: 3px solid transparent;
    }
    .logo-container img {
        max-width: 60%;
        max-height: 60%;
    }

    .team-name {
        font-weight: bold;
        font-size: 16px;
        margin-top: 6px;
        color: #222;
    }
    .pitcher {
        font-size: 13px;
        color: #666;
        margin-bottom: 6px;
    }
    .win-prob {
        font-size: 14px;
        margin-top: 6px;
        font-weight: bold;
    }
    .prob-bar {
        height: 6px;
        border-radius: 3px;
        margin-top: 4px;
        transition: width 0.8s ease-in-out;
    }

    .strong-win {
        box-shadow: 0 0 10px rgba(0, 200, 80, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Page Title (Removed Emoji)
st.markdown("<div class='scoreboard-header'>MLB Matchup Predictions</div>", unsafe_allow_html=True)

# Group games by date
for game_date, games_on_date in df_future_games.groupby("date"):
    st.markdown(f"<div class='date-header'>{game_date}</div>", unsafe_allow_html=True)

    games_list = list(games_on_date.iterrows())
    num_games = len(games_list)
    cards_per_row = 4 if num_games > 6 else 3

    for i in range(0, num_games, cards_per_row):
        cols = st.columns(cards_per_row, gap="large")  # Added larger gap between columns
        for col_idx in range(cards_per_row):
            if i + col_idx < num_games:
                _, game = games_list[i + col_idx]
                team_prob = float(game['team_win_next_pred']) * 100
                opp_prob = 100 - team_prob

                team_color = game.get("team_color", "#1a3d7c")
                opp_color = game.get("opponent_color", "#1a3d7c")

                with cols[col_idx]:
                    st.markdown(f"""
                        <div class="game-card {'strong-win' if max(team_prob, opp_prob) >= 65 else ''}">
                            <div style="display:flex; justify-content:space-around; align-items:center;">
                                <div>
                                    <div class="logo-container" style="border-color:{team_color};">
                                        <img src="{game['team_logo']}"/>
                                    </div>
                                    <div class="team-name">{game['team']}</div>
                                    <div class="pitcher" title="ERA: {game.get('home_era','N/A')} | WHIP: {game.get('home_whip','N/A')}">
                                        Pitcher: {game['home_pitcher']}
                                    </div>
                                    <div class="win-prob" style="color:{'green' if team_prob>=50 else 'red'};">{team_prob:.1f}%</div>
                                    <div class="prob-bar" style="width:{team_prob}%; background:{'green' if team_prob>=50 else 'red'};"></div>
                                </div>
                                <div style="font-weight:bold; font-size:16px; margin:0 10px; color:#555;">VS</div>
                                <div>
                                    <div class="logo-container" style="border-color:{opp_color};">
                                        <img src="{game['opponent_logo']}"/>
                                    </div>
                                    <div class="team-name">{game['opponent']}</div>
                                    <div class="pitcher" title="ERA: {game.get('away_era','N/A')} | WHIP: {game.get('away_whip','N/A')}">
                                        Pitcher: {game['away_pitcher']}
                                    </div>
                                    <div class="win-prob" style="color:{'green' if opp_prob>=50 else 'red'};">{opp_prob:.1f}%</div>
                                    <div class="prob-bar" style="width:{opp_prob}%; background:{'green' if opp_prob>=50 else 'red'};"></div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)


