from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import os
import csv

def GetStat(row, data_stat):
    cell = row.find(['th', 'td'], {'data-stat':data_stat})
    if cell != None:
        return cell.text
    else:
        return ''

def CleanInt(value):
    return 0 if value == '' else int(value)


c1 = pd.Series(data=None, dtype='string', name='player_id')
c2 = pd.Series(data=None, dtype='int', name='year')
c3 = pd.Series(data=None, dtype='datetime64[ns]', name='date')
c4 = pd.Series(data=None, dtype='int', name='week')
c5 = pd.Series(data=None, dtype='string', name='team')
c7 = pd.Series(data=None, dtype='string', name='location')
c8 = pd.Series(data=None, dtype='string', name='opponent')
c9 = pd.Series(data=None, dtype='string', name='result')
c10 = pd.Series(data=None, dtype='bool', name='started')
c11 = pd.Series(data=None, dtype='int', name='rushing_attempts')
c12 = pd.Series(data=None, dtype='int', name='rushing_yards')
c13 = pd.Series(data=None, dtype='int', name='rushing_touchdowns')
c14 = pd.Series(data=None, dtype='int', name='pass_targets')
c15 = pd.Series(data=None, dtype='int', name='receptions')
c16 = pd.Series(data=None, dtype='int', name='receiving_yards')
c17 = pd.Series(data=None, dtype='int', name='receiving_touchdowns')
c18 = pd.Series(data=None, dtype='int', name='conversions')
c19 = pd.Series(data=None, dtype='int', name='fumbles_lost')
c20 = pd.Series(data=None, dtype='int', name='fumble_touchdowns')

df_game_log = pd.concat([c1, c2, c3, c4, c5, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20], axis=1)

df_players = pd.read_csv(os.path.join("Resources", "players.csv"))

player_ids = df_players['id']

for player_id in player_ids:
    url = f'https://www.pro-football-reference.com/players/C/{player_id}/gamelog/'

    source_home = req.get(url).text

    soup = bs(source_home, 'lxml')

    rows = soup.find('table', id='stats').find('tbody').find_all('tr', class_=lambda c: c == None)

    for row in rows:

        cells = row.find_all(['th', 'td'])

        year = GetStat(row, 'year_id')
        date = GetStat(row, 'game_date')
        week = GetStat(row, 'week_num')
        team = GetStat(row, 'team')
        location = 'Away' if GetStat(row, 'game_location') == '@' else 'Home'
        opponent = GetStat(row, 'opp')
        result = GetStat(row, 'game_result').split(' ')[0]
        started = True if GetStat(row, 'gs') == '*' else False
        rushing_attempts = CleanInt(GetStat(row, 'rush_att'))
        rushing_yards = CleanInt(GetStat(row, 'rush_yds'))
        rushing_touchdowns = CleanInt(GetStat(row, 'rush_td'))
        pass_targets = CleanInt(GetStat(row, 'targets'))
        receptions = CleanInt(GetStat(row, 'rec'))
        receiving_yards = CleanInt(GetStat(row, 'rec_yds'))
        receiving_touchdowns = CleanInt(GetStat(row, 'rec_td'))
        conversions =  CleanInt(GetStat(row, 'two_pt_md'))
        fumbles_lost = CleanInt(GetStat(row, 'fumbles_lost'))
        fumble_touchdowns = CleanInt(GetStat(row, 'fumbles_rec_td'))

        game_log = {'player_id': player_id,
                    'year': year,
                    'date': date,
                    'week': week,
                    'team': team,
                    'location': location,
                    'opponent': opponent,
                    'result': result,
                    'started': started,
                    'rushing_attempts': rushing_attempts,
                    'rushing_yards': rushing_yards,
                    'rushing_touchdowns': rushing_touchdowns,
                    'pass_targets': pass_targets,
                    'receptions': receptions,
                    'receiving_yards': receiving_yards,
                    'receiving_touchdowns': receiving_touchdowns,
                    'conversions': conversions,
                    'fumbles_lost': fumbles_lost,
                    'fumble_touchdowns': fumble_touchdowns}

        df_game_log = df_game_log.append(game_log, ignore_index=True)
        
df_game_log.to_csv(os.path.join("..", "Resources", "game_logs.csv"), index=False)

