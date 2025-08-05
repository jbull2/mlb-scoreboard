import pandas as pd

def load_elo_predictions(elo_csv):
    df = pd.read_csv(elo_csv)
    required_cols = {'start_time', 'Date', 'home_team', 'away_team', 'home_pitcher', 'away_pitcher', 'elo_prob_home', 'elo_prob_away'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Elo CSV missing required columns: {required_cols - set(df.columns)}")

    df.rename(columns={
        'Date': 'date',
        'home_team': 'team',
        'away_team': 'opponent',
        'elo_prob_home': 'team_win_next_pred',
        'elo_prob_away': 'opponent_win_next_pred'
    }, inplace=True)
    return df

def load_and_merge_predictions(totals_csv, runline_csv, schedule_csv):
    schedule_df = pd.read_csv(schedule_csv)
    if not {'team', 'opponent', 'start_time'}.issubset(schedule_df.columns):
        raise ValueError("Schedule CSV must contain 'team', 'opponent', 'start_time'")

    def load_and_merge(csv_file):
        df = pd.read_csv(csv_file)
        required_cols = {'date', 'team', 'opponent'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"{csv_file} missing columns: {required_cols - set(df.columns)}")
        df = df.merge(schedule_df[['team', 'opponent', 'start_time']], on=['team', 'opponent'], how='left')
        df['start_time'] = df['start_time'].fillna('TBD')
        return df

    return load_and_merge(totals_csv), load_and_merge(runline_csv)
