import os
from datetime import datetime, timezone

import pymongo
import requests
from django.http import HttpResponse

from .Serializer.Serializer import MatchSerializer
from rest_framework.views import APIView
from . import constants
from .models import Match


class Crawl(APIView):
    def get(self, request):
        url = "https://egb.com/bets?st=0&ut=0"
        response = requests.get(url, headers={"Accept": "application/json"})
        bets = response.json()['bets']
        matches = []
        for bet in bets:
            match = {
                'team1': bet['gamer_1']['nick'],
                'team2': bet['gamer_2']['nick'],
                'odds1': bet['coef_1'],
                'odds2': bet['coef_2'],
                'site': constants.EGB
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
                    'site': constants.BET_WINNER

                }
                matches.append(match)
                matchSerializer = MatchSerializer(data=match)

                if matchSerializer.is_valid():
                    matchSerializer.save()


class Trieu(APIView):
    def get(self, request):
        query = [
            {
                '$project': {
                    'timestamp': {
                        '$subtract': [
                            '$dateTimeStamp', datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
                        ]
                    },
                    'team1': '$team1',
                    'team2': '$team2',
                    'odds1': '$odds1',
                    'odds2': '$odds2'
                }
            }, {
                '$group': {
                    '_id': {
                        'x': '$team1',
                        'y': '$team2',
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
                    }
                }
            }, {
                '$match': {
                    'e': {
                        '$gt': 1
                    },
                    'dateTimeStamp': {
                        '$gt': {
                            '$subtract': [
                                '$dateTimeStamp', datetime(1970, 0, 1, 0, 0, 30, tzinfo=timezone.utc)
                            ]
                        }
                    }
                }
            }
        ]

        MONGODB_URI = "mongodb://localhost:27017/bet?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
        # Connect to your MongoDB cluster:
        client = pymongo.MongoClient(MONGODB_URI)
        # Get a reference to the "sample_mflix" database:
        db = client["Bet"]
        # Get a reference to the "movies" collection:
        collection = db["EGB_match"]

        items = collection.aggregate(query)
        for item in items:
            print(item)
        return HttpResponse(items)

        # [
        #     {
        #         '$project': {
        #             'time_diff': {
        #                 '$subtract': [
        #                     datetime(2021, 11, 23, 17, 18, 0, tzinfo=timezone.utc), '$dateTimeStamp'
        #                 ]
        #             }
        #         }
        #     }, {
        #     '$match': {
        #         'time_diff': {
        #             '$lt': 30000
        #         }
        #     }
        # }
        # ]
