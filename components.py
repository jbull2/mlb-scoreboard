import streamlit as st

def render_card_section(games_list, card_fn):
    """Render cards inside a responsive flex container."""
    st.markdown("<div class='card-container'>", unsafe_allow_html=True)
    for _, game in games_list:
        st.markdown(card_fn(game), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def moneyline_card(game):
    team_prob = float(game['team_win_next_pred']) * 100
    opp_prob = 100 - team_prob
    return f"""
    <div class="game-card">
        <div class="start-time">{game['start_time']}</div>
        <div class="logo-row">
            <div class="team">
                <div class="logo-container"><img src="{game['team_logo']}"></div>
                <div class="team-name">{game['team']}</div>
                <div class="pitcher">{game['home_pitcher']}</div>
                <div class="win-prob">{team_prob:.1f}%</div>
            </div>
            <div class="vs-text">VS</div>
            <div class="team">
                <div class="logo-container"><img src="{game['opponent_logo']}"></div>
                <div class="team-name">{game['opponent']}</div>
                <div class="pitcher">{game['away_pitcher']}</div>
                <div class="win-prob">{opp_prob:.1f}%</div>
            </div>
        </div>
    </div>
    """

def totals_card(game):
    prob = float(game['model_confidence']) * 100
    return f"""
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
    """

def runline_card(game):
    confidence = float(game['confidence']) * 100
    spread_value = float(game['home_spread']) if game['pred_winner'] == game['team'] else float(game['away_spread'])
    spread_formatted = f"{'+' if spread_value > 0 else ''}{spread_value:.1f}"

    return f"""
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
                Predicted: {game['pred_winner']} {spread_formatted} ({confidence:.1f}%)
            </div>
        </div>
    """
