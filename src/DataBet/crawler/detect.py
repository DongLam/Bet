from datetime import datetime, timezone

import pymongo

from crawler.tele_bot import send_message


def detect():
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
        print(item)
