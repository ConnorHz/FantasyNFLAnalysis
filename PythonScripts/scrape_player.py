from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import os
import csv


year = 2020
url = f'https://www.pro-football-reference.com/years/{year}/fantasy.htm'

column_names = ["id", "name", "team", "team_abbr", "position"]
df_players = pd.DataFrame(columns = column_names)

source_home = req.get(url).text

soup = bs(source_home, 'lxml')

id_ = ''
name = ''
team = ''
team_abbr = ''
position = ''


for row in soup.find('table', id='fantasy').find('tbody').find_all('tr'):
    for cell in row.find_all('td'):
        if cell['data-stat'] == 'player':
            id_ = cell['data-append-csv']
            name = cell.text
        if cell['data-stat'] == 'team':
            team = cell.a['title']
            team_abbr = cell.text
        if cell['data-stat'] == 'fantasy_pos':
            position = cell.text

    player = {"id":id_, "name":name.strip(), "team":team, "team_abbr":team_abbr, "position":position}
    df_players = df_players.append(player, ignore_index=True)

df_players.drop_duplicates().to_csv(os.path.join("..", "Resources", "players.csv"), index=False)

