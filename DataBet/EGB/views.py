
import pymongo
import requests

from .Serializer.Serializer import MatchSerializer
from rest_framework.views import APIView

class Crawl(APIView):
     def get(self, request):
          url = "https://egb.com/bets?st=0&ut=0"
          response = requests.get(url, headers={"Accept": "application/json"})
          bets = response.json()['bets']
          matches = []
          print("111111111111")
          for bet in bets:
               match = {
                    'team1': bet['gamer_1']['nick'],
                    'team2': bet['gamer_2']['nick'],
                    'odds1': bet['coef_1'],
                    'odds2': bet['coef_2']
               }
               matches.append(match)
               matchSerializer = MatchSerializer(data=match)
               if matchSerializer.is_valid():
                    matchSerializer.save()

          return(response.json()['user_time'])