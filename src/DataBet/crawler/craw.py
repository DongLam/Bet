from datetime import timezone,datetime
import requests
from celery.schedules import crontab
import pymongo
from crawler import constants
from crawler.Serializer.Serializer import MatchSerializer
from crawler.constants import *
from crawler.tele_bot import send_message


def egb(timeStamp):
     try:
          url = "https://egb.com/bets?st=0&ut=0&active=true"
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
                    match = sort_team_name(match)
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
                    if bet['O2'] == "LDLC" or bet['O1'] == "LDLC":
                         print()
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
                         match = sort_team_name(match)
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
                              try:
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
                                                            'odds1': rate[1],
                                                            'odds2': rate[0],
                                                            'site': constants.PS38,
                                                            'game': get_game_ps38(title_split[0]),
                                                            'dateTimeStamp': timeStamp,
                                                            'team1_tmp': change_name_to_tmp(name1),
                                                            'team2_tmp': change_name_to_tmp(name2)
                                                       }
                                                       bet = sort_team_name(bet)
                                                       matchSerializer = MatchSerializer(data=bet)
                                                       if matchSerializer.is_valid():
                                                            matchSerializer.save()
                                                            i = i + 1
                                                       else:
                                                            print(matchSerializer.errors)
                                                            print("Handicap or map", name1, name2)
                                                  # else:
                                                  #      print("Trash", name1, name2)
                              except:
                                   print("zzzzzzz")

     print("Done PS38: " + str(i))

def send_notice():
     query = [
          {
               '$project': {
                    'timestamp': {
                         '$subtract': [
                              '$dateTimeStamp', datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
                         ]
                    },
                    'team1': '$team1_tmp',
                    'team2': '$team2_tmp',
                    'game': '$game',
                    'odds1': '$odds1',
                    'odds2': '$odds2',
                    't': {
                         '$subtract': [
                              datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                              datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
                         ]
                    }
               }
          }, {
               '$group': {
                    '_id': {
                         'x': '$team1',
                         'y': '$team2',
                         'z': '$game',

                         'time': {
                              '$round': [
                                   '$timestamp', -6
                              ]
                         }
                    },
                    'a': {
                         '$max': '$odds1'
                    },
                    'b': {
                         '$max': '$odds2'
                    },
                    'c': {
                         '$min': '$odds1'
                    },
                    'd': {
                         '$min': '$odds2'
                    }
               }
          }, {
               '$sort': {
                    'a': 1
               }
          }, {
               '$project': {
                    'e': {
                         '$multiply': [
                              {
                                   '$subtract': [
                                        '$a', 1
                                   ]
                              }, {
                                   '$subtract': [
                                        '$b', 1
                                   ]
                              }
                         ]
                    },
                    'odd1': '$a',
                    'odd2': '$b'
               }
          }, {
               '$match': {
                    'e': {'$gt': 1.1}
               }
          }
     ]

     MONGODB_URI = "mongodb://localhost:27017/bet?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
     # Connect to your MongoDB cluster:
     client = pymongo.MongoClient(MONGODB_URI)
     # Get a reference to the "sample_mflix" database:
     db = client["Bet"]
     # Get a reference to the "movies" collection:
     collection = db["crawler_match"]

     items = collection.aggregate(query)
     for item in items:
          team1 = item['_id']['x']
          team2 = item['_id']['y']
          value = item['e']
          query2 = [
               {
                    '$match': {
                         'team1_tmp': team1,
                         'team2_tmp': team2,
                    }
               }
          ]
          teams = collection.aggregate(query2)
          max_odd1 = item['odd1']
          max_odd2 = item['odd2']

          check_egb = 0
          check_betwinner = 0
          check_ps38 = 0
          data = {}
          for i in teams:
               if i['site'] == 'EGB':
                    if str(i['odds1']) >= str(max_odd1) or str(i['odds2']) >= str(max_odd2):
                         data['egb'] = {}
                         check_egb = 1
                         data['egb']['team1'] = i['team1']
                         data['egb']['team2'] = i['team2']
                         if str(i['odds1']) >= str(max_odd1):
                              data['egb']['odd1'] = i['odds1']
                         else:
                              data['egb']['odd2'] = i['odds2']

               if i['site'] == 'BETWINNER':
                    if str(i['odds1']) >= str(max_odd1) or str(i['odds2']) >= str(max_odd2):
                         data['betwinner'] = {}
                         check_betwinner = 1
                         data['betwinner']['team1'] = i['team1']
                         data['betwinner']['team2'] = i['team2']
                         if str(i['odds1']) >= str(max_odd1):
                              data['betwinner']['odd1'] = i['odds1']
                         else:
                              data['betwinner']['odd2'] = i['odds2']

               if i['site'] == 'PS38':
                    if str(i['odds1']) >= str(max_odd1) or str(i['odds2']) >= str(max_odd2):
                         data['ps38'] = {}
                         check_ps38 = 1
                         data['ps38']['team1'] = i['team1']
                         data['ps38']['team2'] = i['team2']
                         if str(i['odds1']) >= str(max_odd1):
                              data['ps38']['odd1'] = i['odds1']
                         else:
                              data['ps38']['odd2'] = i['odds2']



          if check_egb + check_betwinner + check_ps38 > 1:

               str_send = "game: " + item['_id']['z'] + " value = " + str(value) + "\n"
               if data.get('egb') is not None:
                    str_send = str_send + 'EGB:\n\t ' + data_to_string(data['egb']) + "\n"
               if data.get('betwinner') is not None:
                    str_send = str_send + 'BETWINNER:\n\t ' + data_to_string(data['betwinner']) + "\n"
               if data.get('ps38') is not None:
                    str_send = str_send + 'PS38:\n\t ' + data_to_string(data['ps38']) + "\n"

               send_message(str_send)
               print(str_send)

def data_to_string(data):
     string = "team1: " + data['team1'] + ", team2: " + data['team2']
     if data.get('odd1') is not None:
          string = string + ', odd1: ' + str(data.get('odd1'))
     if data.get('odd2') is not None:
          string = string + ', odd2: ' + str(data.get('odd2'))
     return string

def change_name_to_tmp(team):
     result = team.upper().replace(" ", "").replace("-", "").replace("TEAM", "").replace("GAMING", "").\
          replace("ESPORTS", "").replace("ESPORT", "").replace("SPORTS", "").replace("(GAMBIT)", "").\
          replace("CHALLENGERS", "").replace("CHALL", "").replace("ECLUB", "").replace("CLAN", "")
     for item in MANUAL_NAME:
          if item[0] == result:
               result = item[1]
     return result


def get_game_bet_winnner(game):
     if BW_CSGO in game:
          return BET_CSGO
     if BW_LOL in game:
          return BET_LOL
     if BW_LOL2 in game:
          return BET_LOL
     if BW_STAR_CRAFT in game:
          return BET_STAR_CRAFT
     if BW_DOTA2 in game:
          return BET_DOTA2
     if BW_KOG in game:
          return BET_KOG
     if BW_KOG2 in game:
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

def sort_team_name(match):
     match['team1_tmp'] = (match['team1_tmp'].encode('ascii', 'ignore')).decode("utf-8")
     match['team2_tmp'] = (match['team2_tmp'].encode('ascii', 'ignore')).decode("utf-8")
     if match['team1_tmp'] > match['team2_tmp']:
          team_tmp = match['team1']
          match['team1'] = match['team2']
          match['team2'] = team_tmp

          odd_tmp = match['odds1']
          match['odds1'] = match['odds2']
          match['odds2'] = odd_tmp

          team_tmp = match['team1_tmp']
          match['team1_tmp'] = match['team2_tmp']
          match['team2_tmp'] = team_tmp
     return match
