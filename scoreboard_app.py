from flask import Flask, render_template
import pandas as pd
from data_loader import load_elo_predictions, load_and_merge_predictions
from team_logos import TEAM_LOGOS

app = Flask(__name__)

@app.route('/')
def index():
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
        df['start_time_sort'] = pd.to_datetime(df['start_time'], format='%I:%M %p', errors='coerce')
        df.sort_values('start_time_sort', inplace=True)

    return render_template(
        'index.html',
        df_moneyline=df_moneyline,
        df_totals=df_totals,
        df_runline=df_runline
    )

if __name__ == '__main__':
    app.run(debug=True)
