from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import os
import sys

df_players = pd.read_csv(os.path.join("..", "Resources", "players.csv"))

player_ids = df_players['id']

df_game_log = pd.DataFrame()

for player_id in player_ids:
    url = f'https://www.pro-football-reference.com/players/C/{player_id}/gamelog/'

    source_home = req.get(url).text

    soup = bs(source_home, 'lxml')

    rows = soup.find('table', id='stats').find('tbody').find_all('tr', class_=lambda c: c == None)

    # setup toolbar
    sys.stdout.write(player_id + " [%s]" % (" " * len(rows)))
    sys.stdout.flush()
    sys.stdout.write("\b" * (len(rows)+1)) # return to start of line, after '['

    for row in rows:
        df_row = pd.DataFrame()
        df_row = pd.concat([df_row, pd.DataFrame({'player_id':[player_id]})], axis=1)

        for cell in row.find_all(['th', 'td']):
            df_cell = pd.DataFrame({cell['data-stat']:[cell.text]})
            df_row = pd.concat([df_row, df_cell], axis=1)
        
        df_game_log = pd.concat([df_game_log, df_row], axis=0, ignore_index=True)

        sys.stdout.write("-")
        sys.stdout.flush()
    
    sys.stdout.write("]\n") # this ends the progress bar
    df_game_log.to_csv(os.path.join("..", "Resources", "full_game_logs.csv"), index=False)






