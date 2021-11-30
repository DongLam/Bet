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
                    'time_dif': {
                        '$subtract': [
                            '$dateTimeStamp', datetime.now()
                        ]
                    },
                    'team1': '$team1',
                    'team2': '$team2',
                    'odds1': '$odds1',
                    'odds2': '$odds2',
                    'site': '$site'
                }
            }, {
                '$sort': {
                    'time_dif': -1
                }
            }, {
                '$match': {
                    'time_dif': {
                        '$gte': -99404800,
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        't1': '$team1',
                        't2': '$team2'
                    },
                    'o1': {
                        '$max': '$odds1'
                    },
                    'o2': {
                        '$max': '$odds2'
                    },
                    'docs': {
                        '$push': '$$ROOT'
                    }
                }
            }, {
                '$redact': {
                    '$cond': {
                        'if': {
                            '$or': [
                                {
                                    '$eq': [
                                        {
                                            '$ifNull': [
                                                '$odds1', '$$ROOT.o1'
                                            ]
                                        }, '$$ROOT.o1'
                                    ]
                                }, {
                                    '$eq': [
                                        {
                                            '$ifNull': [
                                                '$odds2', '$$ROOT.o2'
                                            ]
                                        }, '$$ROOT.o2'
                                    ]
                                }
                            ]
                        },
                        'then': '$$DESCEND',
                        'else': '$$PRUNE'
                    }
                }
            }, {
                '$project': {
                    'est': {
                        '$multiply': [
                            {
                                '$subtract': [
                                    '$o1', 1
                                ]
                            }, {
                                '$subtract': [
                                    '$o2', 1
                                ]
                            }
                        ]
                    },
                    'docs': '$docs'
                }
            },
        ]
        MONGODB_URI = DATABASE_HOST
        # Connect to your MongoDB cluster:
        client = pymongo.MongoClient(MONGODB_URI)
        # Get a reference to the "sample_mflix" database:
        db = client["Bet"]
        # Get a reference to the "movies" collection:
        collection = db["bet"]
        items = collection.aggregate(query)

        list = []
        dem = 0
        for item in items:
            if(dem == 0):
                print(item)
                print(1111111111111111111)
                dem = dem + 1
            print(item['_id'])
            print(item['est'])
            for i in item['docs']:
                matchSerializer = MatchSerializer(data=i)
                if matchSerializer.is_valid():
                    print(str(matchSerializer.data))


    except Exception as e:
        print(e)
