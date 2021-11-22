import requests
from celery.schedules import crontab

from crawler import constants
from crawler.Serializer.Serializer import MatchSerializer

def egb():
     try:
          url = "https://egb.com/bets?st=0&ut=0"
          response = requests.get(url, headers={"Accept": "application/json"})
          bets = response.json()['bets']
          matches = []
          for bet in bets:
               if bet['game'] and 'CS:GO' in bet['game']:
                    match = {
                         'team1': bet['gamer_1']['nick'],
                         'team2': bet['gamer_2']['nick'],
                         'odds1': bet['coef_1'],
                         'odds2': bet['coef_2'],
                         'site': constants.EGB,
                         'game': bet['game']
                    }
                    matches.append(match)
                    matchSerializer = MatchSerializer(data=match)
                    if matchSerializer.is_valid():
                         matchSerializer.save()
          print("True")
     except Exception as e:
          print(e)


def bet_winner():
     try:
          url = constants.BET_WINNER_URL
          response = requests.get(url, headers={"Accept": "application/json"})
          bets = response.json()['Value']
          matches = []
          for bet in bets:
               if bet['L'] and 'CS:GO' in bet['L']:
                    match = {
                         'team1': bet['O1'],
                         'team2': bet['O2'],
                         'odds1': bet['E'][0]['C'],
                         'odds2': bet['E'][1]['C'],
                         'site': constants.BET_WINNER,
                         'game': 'CS:GO'
                    }
                    matches.append(match)
                    matchSerializer = MatchSerializer(data=match)

                    if matchSerializer.is_valid():
                         matchSerializer.save()
          print("True")
     except Exception as e:
          print(e)

