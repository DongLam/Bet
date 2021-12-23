from datetime import datetime

import requests
from celery.schedules import crontab

from crawler import constants
from crawler.Serializer.Serializer import MatchSerializer
from crawler.constants import *


def egb(timeStamp):
     try:
          url = "https://egb.com/bets?st=0&ut=0"
          response = requests.get(url, headers={"Accept": "application/json"})
          bets = response.json()['bets']
          i = 0
          for bet in bets:
               game = ''
               if bet['game']:
                    game = get_game_egb(bet['game'])
               if game:

                    match = {
                         'team1': bet['gamer_1']['nick'],
                         'team2': bet['gamer_2']['nick'],
                         'odds1': bet['coef_1'],
                         'odds2': bet['coef_2'],
                         'site': constants.EGB,
                         'game': game,
                         'dateTimeStamp': timeStamp,
                         'team1_tmp': change_name_to_tmp(bet['gamer_1']['nick']),
                         'team2_tmp': change_name_to_tmp(bet['gamer_2']['nick'])
                    }
                    matchSerializer = MatchSerializer(data=match)
                    if matchSerializer.is_valid():
                         matchSerializer.save()
                         i = i + 1
          print("Done Egb: " + str(i))
     except Exception as e:
          print(e)


def bet_winner(timeStamp):
     try:
          url = constants.BET_WINNER_URL
          response = requests.get(url, headers={"Accept": "application/json"})
          bets = response.json()['Value']
          i = 0
          for bet in bets:
               try:
                    game = ''
                    if bet['L']:
                         game = get_game_bet_winnner(bet['L'])
                    if game:
                         match = {
                              'team1': bet['O1'],
                              'team2': bet['O2'],
                              'odds1': bet['E'][0]['C'],
                              'odds2': bet['E'][1]['C'],
                              'site': constants.BET_WINNER,
                              'game': game,
                              'dateTimeStamp': timeStamp,
                              'team1_tmp': change_name_to_tmp(bet['O1']),
                              'team2_tmp': change_name_to_tmp(bet['O2'])
                         }
                         matchSerializer = MatchSerializer(data=match)

                         if matchSerializer.is_valid():
                              matchSerializer.save()
                              i = i +1
               except Exception as e:
                    print(e)
          print("Done Bet-Winner: " + str(i))
     except Exception as e:
          print(e)

def ps38(timeStamp):
     # 'https://www.ps3838.com/sports-service/sv/compact/events?l=3&lv=&me=0&mk=1&sp=12&locale=en_US'
     url = constants.PS38_URL
     response = requests.get(url, headers={"Accept": "application/json"})
     datas = response.json()['n']
     matches_save = []
     i = 0
     for data in datas:
          if len(data) > 2:
               leagues = data[2]
               for league in leagues:
                    if len(league) > 2:
                         matches = league[2]
                         title = league[1]
                         title_split = title.split(' - ')
                         for match in matches:
                              if match[2].find('(Kills)') == -1:
                                   name1 = match[1]
                                   name2 = match[2]
                                   rates = match[8]['0']
                                   for rate in rates:
                                        if rate.__class__ == list:
                                             if len(rate) == 7:
                                                  bet = {
                                                       'team1': name1,
                                                       'team2': name2,
                                                       'odds1': rate[0],
                                                       'odds2': rate[1],
                                                       'site': constants.PS38,
                                                       'game': get_game_ps38(title_split[0]),
                                                       'dateTimeStamp': timeStamp,
                                                       'team1_tmp': change_name_to_tmp(name1),
                                                       'team2_tmp': change_name_to_tmp(name2)
                                                  }
                                                  matchSerializer = MatchSerializer(data=bet)
                                                  if matchSerializer.is_valid():
                                                       matchSerializer.save()
                                                       i = i + 1
                                                  else:
                                                       print(matchSerializer.errors)
                                                       print("Handicap or map", name1, name2)
                                             # else:
                                             #      print("Trash", name1, name2)

     print("Done PS38: " + str(i))

def change_name_to_tmp(team):
     result = team.upper().replace(" ", "").replace("TEAM", "").replace("GAMING", "")
     return result


def get_game_bet_winnner(game):
     if BW_CSGO in game:
          return BET_CSGO
     if BW_LOL in game:
          return BET_LOL
     if BW_STAR_CRAFT in game:
          return BET_STAR_CRAFT
     if BW_DOTA2 in game:
          return BET_DOTA2
     if BW_KOG in game:
          return BET_KOG
     if BW_VAL in game:
          return BET_VAL
     if BW_PUBG in game:
          return BET_PUBG
     if BW_AOR in game:
          return BET_AOR
     else:
          return None

def get_game_egb(game):
     if EGB_CSGO in game:
          return BET_CSGO
     if EGB_LOL in game:
          return BET_LOL
     if EGB_STAR_CRAFT in game:
          return BET_STAR_CRAFT
     if EGB_DOTA2 in game:
          return BET_DOTA2
     if EGB_KOG in game:
          return BET_KOG
     if EGB_VAL in game:
          return BET_VAL
     if EGB_PUBG in game:
          return BET_PUBG
     if EGB_AOR in game:
          return BET_AOR
     else:
          return None

def get_game_ps38(game):
     if PS38_CSGO in game:
          return BET_CSGO
     if PS38_LOL in game:
          return BET_LOL
     if PS38_STAR_CRAFT in game:
          return BET_STAR_CRAFT
     if PS38_DOTA2 in game:
          return BET_DOTA2
     if PS38_KOG in game:
          return BET_KOG
     if PS38_VAL in game:
          return BET_VAL
     if PS38_PUBG in game:
          return BET_PUBG
     if PS38_AOR in game:
          return BET_AOR
     else:
          return None