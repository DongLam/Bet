from datetime import timezone, datetime

import pymongo
import requests
from django.http import HttpResponse

from rest_framework.views import APIView
from crawler import constants
from crawler.Serializer.Serializer import MatchSerializer
from crawler.constants import BET_WINNER
from crawler.models import Match
from crawler.tele_bot import send_message

from crawler.detect import lam


class Crawl(APIView):
    def get(self, request):
        url = "https://egb.com/bets?st=0&ut=0"
        response = requests.get(url, headers={"Accept": "application/json"})
        bets = response.json()['bets']
        matches = []
        i = 1
        j = 1
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
        return (response.json()['user_time'])


class Lam(APIView):
    def get(self, request):
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
                    'game': 'CS:GO',
                    'site': constants.BET_WINNER

                }
                matches.append(match)
                matchSerializer = MatchSerializer(data=match)

                if matchSerializer.is_valid():
                    matchSerializer.save()


def get_data_bet_winner():
    datas=Match.objects.filter(site=BET_WINNER)
    message=''
    i=0
    for data in datas:
        i = i + 1
        message += '\n' + str(MatchSerializer(data).data)
        if i > 20:
            break

    send_message(message)


class Trieu(APIView):
    def get(self, request):
        lam()
        return HttpResponse(1)
