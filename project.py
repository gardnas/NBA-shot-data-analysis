# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# This is imports for our new library challenge goal plotly for some of our visualizations.
!pip install plotly
import plotly.express as px
import plotly.graph_objects as go
#drawing our court
from matplotlib.patches import Circle, Rectangle, Arc
# %%
# Reading in the data:
# %%
shot_locations_2023 = pd.read_csv(
'NBA_2023_Shots.csv').rename(columns = {'SEASON_1' : 'year'}).set_index('year')
shot_locations_2014 = pd.read_csv(
'NBA_2014_Shots.csv').rename(columns = {'SEASON_1' : 'year'}).set_index('year')
shot_locations_2004 = pd.read_csv(
'NBA_2004_Shots.csv').rename(columns = {'SEASON_1' : 'year'}).set_index('year')
top_players_2003_2004 = pd.read_csv('NBA TOP PLAYERS 2003-2004.csv')
top_players_2013_2014 = pd.read_csv('NBA TOP PLAYERS 2013-2014.csv')
top_players_2022_2023 = pd.read_csv('NBA TOP PLAYERS 2022-2023.csv').rename(columns = {'#' : 'rank'})
top_players_2003_2004['year'] = 2004
top_players_2013_2014['year'] = 2014
top_players_2022_2023['year'] = 2023
top_players_2003_2004 = top_players_2003_2004.set_index('year')
top_players_2013_2014 = top_players_2013_2014.set_index('year')
top_players_2022_2023 = top_players_2022_2023.set_index('year')
shot_loc_all_years = pd.concat([shot_locations_2004, shot_locations_2014, shot_locations_2023])
top_players_all_years = pd.concat([top_players_2003_2004, top_players_2013_2014,
top_players_2022_2023])
top_players_shot_loc = shot_loc_all_years.merge(top_players_all_years, how = 'right',
left_on = ['year', 'PLAYER_NAME'],
right_on = ['year', 'PLAYER'], )
shot_loc_all_years.to_csv('shot_loc_all_years.csv')
top_players_shot_loc.to_csv('top_players_shot_loc.csv')
top_5_players = pd.read_csv('Top 5 players 2004-2023.csv')
# %%
# %%
#position
def player_position(data):
    """
    Creates the plot to show the counts for the number of players in each repective position given the data
    Parameters:
    - data: DataFrame containing the player data.
    """
    positions = data['POSITION']
    fig = px.bar(data, x = positions, title='Player Positions for Top 5 Players from 2004, 2014, and 2023'
    color = "POSITION", hover_data="Player Name")
    fig.update_layout(yaxis_title = "# of Players")
    fig.show()
# height
def player_height(data):
    """
    Creates a plot for the distribution of player heights given the data.
    Parameters:
    - data: DataFrame containing the player data.
    """
    fig = px.bar(data, x = "HEIGHT", title="Top 5 Players from 2004, 2014, and 2023 height counts", color =
    hover_data = "Player Name")
    fig.update_layout(yaxis_title = "# of Players")
    fig.show()
    # weight
def player_weight(data):
    """
    Creates the plot for the disribution of player weights given the data.
    Parameters:
    - data: DataFrame containing the player data.
    """
    avg_weight = data['WEIGHT'].mean()
    fig = px.bar(data, x="Player Name", y = "WEIGHT", title='Weights for Top 5 Players from 2004, 2014, and 2023')
    fig.add_hline(y=avg_weight, line_color="red", annotation_text=f"Mean weight: {avg_weight:.3f}")
    fig.show()
    #points, assits, rebounds per game
def player_statistics(data, stat):
    """
    Returns a plot of the distribution and calculates the average for a given statistic. The
    Parameters:
    - data: DataFrame containing the player data.
    - stat: String representing the statistic to analyze ('PPG', 'APG', 'RPG') from the data. Also, we assu
    the statistic is present in the data.
    """
    avg = data[stat].mean()
    fig = px.bar(data, x='Player Name', y=stat, title=f'{stat} for Top 5 Players from 2004, 2014, and 2023
    fig.add_hline(y=avg, line_color="red", annotation_text=f"Mean {stat}: {avg:.3f}")
    fig.show()
    return avg
    player_position(top_5_players)
    player_height(top_5_players)
    player_weight(top_5_players)
    player_statistics(top_5_players, 'PPG')
    player_statistics(top_5_players, 'APG')

# %% 
def performs_best_quarter(year, quarter, data):
    '''
    Returns the name of the player that has the highest score per 'quarter' quarter played. takes
    in a specific year and quarter and a dataset to look over.
    '''
    specific_quarter = data[(data['QUARTER'] == quarter) & (data['SHOT_MADE'] == True)].loc[year]
    player_game_count = specific_quarter.set_index('PLAYER_NAME').GAME_ID
    player_scores = {}
    for player, type in zip(specific_quarter['PLAYER_NAME'], specific_quarter['SHOT_TYPE']):
    if player not in player_scores:
    player_scores[player] = 0
    if type == '3PT Field Goal':
    player_scores[player] += 3
    elif type == '2PT Field Goal':
    player_scores[player] += 2
    player_avg_score = {}
    for player in player_scores.keys():
    games = player_game_count.loc[player].tolist()
    if not isinstance(games, list):
    games = 1
    else:
    games = len(set(games))
    player_avg_score[player] = player_scores[player] / games
    return max(player_avg_score, key=player_avg_score.get)

# %%
fig, axs = plt.subplots(nrows = 3, figsize = (18, 12), ncols = 4, sharex = True, sharey = True)
years = [2004, 2014, 2023]
quarters = [1, 2, 3, 4]
for year in years:
    for quarter in quarters:
        shot_chart(performs_best_quarter(year, quarter, top_players_shot_loc), year = year,
        quarter = quarter, data = top_players_shot_loc, ax = axs[years.index(year),
    quarters.index(quarter)], all_shots = True)
    fig.savefig('best_perform_shot_loc.png')

# %%
expected_mean_ppg = top_5_players['PPG'].mean()
expected_mean_apg = top_5_players['APG'].mean()
expected_mean_rpg = top_5_players['RPG'].mean()
test_mean_ppg = player_statistics(top_5_players, 'PPG')
test_mean_apg = player_statistics(top_5_players, 'APG')
_
163 (1).ipynb 17/19
3/12/24, 10:51 PM Final
_
163 (1)
test_mean_rpg = player_statistics(top_5_players, 'RPG')
assert test_mean_ppg == expected_mean_ppg, "PPG mean calculation is incorrect"
assert test_mean_apg == expected_mean_apg, "APG mean calculation is incorrect"