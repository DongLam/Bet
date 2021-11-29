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
          matches = []
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
                    matches.append(match)
                    matchSerializer = MatchSerializer(data=match)
                    if matchSerializer.is_valid():
                         matchSerializer.save()
          print("True")
     except Exception as e:
          print(e)


def bet_winner(timeStamp):
     try:
          url = constants.BET_WINNER_URL
          response = requests.get(url, headers={"Accept": "application/json"})
          bets = response.json()['Value']
          matches = []
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
                         matches.append(match)
                         matchSerializer = MatchSerializer(data=match)

                         if matchSerializer.is_valid():
                              matchSerializer.save()
               except Exception as e:
                    print(e)
          print("True")
     except Exception as e:
          print(e)

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