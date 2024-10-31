import pandas as pd

# Load the dataset
nba_data = pd.read_csv('nba_games.csv')

# Step 1: Calculate each team's average performance for each stat in each season
team_season_avg = nba_data.groupby(['season', 'team']).mean(numeric_only=True).reset_index()

# Step 2: Calculate each team's performance against each opponent for each stat in each season
team_vs_opponent = nba_data.groupby(['season', 'team', 'team_opp']).mean(numeric_only=True).reset_index()

# Step 3: Calculate (average stats against each opponent - total average stats) for each team in each season
merged_data = pd.merge(
    team_vs_opponent,
    team_season_avg,
    on=['season', 'team'],
    suffixes=('_vs_opp', '_season_avg')
)

# Calculate the difference for each stat
stats_diff = merged_data.filter(regex='_vs_opp').subtract(
    merged_data.filter(regex='_season_avg').values
)

# Add identifiers back to the stats_diff DataFrame
stats_diff['season'] = merged_data['season']
stats_diff['team'] = merged_data['team']
stats_diff['team_opp'] = merged_data['team_opp']

# Step 4: Calculate the percentage difference for each stat
# Extract only relevant stat columns to align dimensions for calculation
stats_diff_only = stats_diff.filter(regex='_vs_opp')
season_avg_only = merged_data.filter(regex='_season_avg')
percentage_diff = stats_diff_only.divide(season_avg_only.values) * 100

# Add identifiers back to the percentage_diff DataFrame
percentage_diff['season'] = stats_diff['season']
percentage_diff['team'] = stats_diff['team']
percentage_diff['team_opp'] = stats_diff['team_opp']

# Reorder columns to place identifiers first for all tables
team_season_avg_cleaned = team_season_avg[['season', 'team'] + [col for col in team_season_avg.columns if col not in ['season', 'team']]]
team_vs_opponent_cleaned = team_vs_opponent[['season', 'team', 'team_opp'] + [col for col in team_vs_opponent.columns if col not in ['season', 'team', 'team_opp']]]
stats_diff_cleaned = stats_diff[['season', 'team', 'team_opp'] + [col for col in stats_diff.columns if col not in ['season', 'team', 'team_opp']]]
percentage_diff_cleaned = percentage_diff[['season', 'team', 'team_opp'] + [col for col in percentage_diff.columns if col not in ['season', 'team', 'team_opp']]]

# Drop unnecessary columns from percentage_diff_cleaned
columns_to_drop = ['Unnamed: 0_vs_opp', 'mp_vs_opp', 'mp.1_vs_opp']
percentage_diff_cleaned = percentage_diff_cleaned.drop(columns=columns_to_drop, errors='ignore')

# Save each form as a CSV file
'''team_season_avg_cleaned.to_csv('team_season_average.csv', index=False)
team_vs_opponent_cleaned.to_csv('team_vs_opponent_average.csv', index=False)
stats_diff_cleaned.to_csv('team_performance_difference.csv', index=False)'''
percentage_diff_cleaned.to_csv('percentage_difference.csv', index=False)
