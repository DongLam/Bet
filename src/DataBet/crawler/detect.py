from datetime import datetime, timezone, timedelta

import pymongo

from DataBet.settings import DATABASE_HOST
from crawler.Serializer.Serializer import MatchSerializer
from crawler.models import Match
from crawler.tele_bot import send_message


def detect():
    query = [
        {
            '$sort': {
                'dateTimeStamp': -1
            }
        }, {
            '$group': {
                '_id': {
                    't1': '$team1',
                    't2': '$team2',
                    's': '$site',
                    'dt': '$dateTimeStamp'
                },
                'docs': {
                    '$push': '$$ROOT'
                }
            }
        }, {
            '$project': {
                'match': {
                    '$slice': [
                        '$docs', 1
                    ]
                }
            }
        }, {
            '$sort': {
                'team1': -1,
                'team2': -1
            }
        }
    ]

    MONGODB_URI = DATABASE_HOST
    # Connect to your MongoDB cluster:
    client = pymongo.MongoClient(MONGODB_URI)
    # Get a reference to the "sample_mflix" database:
    db = client["Bet"]
    # Get a reference to the "movies" collection:
    collection = db["crawler_match"]
    list = []
    items = collection.aggregate(query)
    for item in items:
        matchSerializer = MatchSerializer(data=item['match'][0])

        if (matchSerializer.is_valid()):
            list.append(str(matchSerializer.data))
        else:
            print(matchSerializer.errors)
    list.sort()

    for result in list:
        print(result)


def lam():
    try:
        query = [
            {
                '$project': {
                    'timestamp': {
                        '$subtract': [
                            '$dateTimeStamp', datetime.now()
                        ]
                    },
                    'team1': '$team1',
                    'team2': '$team2',
                    'odds1': '$odds1',
                    'odds2': '$odds2',
                    'site': '$site',
                    'game': '$game',
                    'dateTimeStamp': '$dateTimeStamp',
                    'team1_tmp': '$team1_tmp',
                    'team2_tmp': '$team2_tmp',
                }
            }, {
                '$match': {
                    'timestamp': {
                        '$gt': -60000
                    }
                }
            }
        ]
        MONGODB_URI = DATABASE_HOST
        # Connect to your MongoDB cluster:
        client = pymongo.MongoClient(MONGODB_URI)
        # Get a reference to the "sample_mflix" database:
        db = client["Bet"]
        # Get a reference to the "movies" collection:
        collection = db["crawler_match"]
        items = collection.aggregate(query)

        list = []
        for item in items:
            matchSerializer = MatchSerializer(data=item)
            if matchSerializer.is_valid():
                list.append(matchSerializer.data)
        list = sorted(list, key=lambda d: (d['game'], d['team1_tmp']), reverse=True)

        lam = []
        for i in range(0, len(list) - 1):
            if list[i]['team2_tmp'] == list[i+1]['team2_tmp'] and list[i]['site'] != list[i+1]['site']:
                lam.append(list[i])
                lam.append(list[i+1])

        message = ''
        for result in lam:
            message = message + str(result) + '\n'
        # send_message(message)
        print(message)
    except Exception as e:
        print(e)
