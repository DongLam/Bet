from datetime import datetime

from celery import shared_task

from crawler.craw import egb, bet_winner, ps38
from crawler.detect import detect, lam, detect_exception
from crawler.export import remove_data
from crawler.tele_bot import send_message
from crawler.views import get_data_bet_winner


@shared_task()
def crawl_egb():
    egb()

@shared_task()
def crawl_bet_winner():
    timeStamp = datetime.now()
    bet_winner(timeStamp)

@shared_task()
def crawl_task():
    remove_data()
    timeStamp = datetime.now()
    egb(timeStamp)
    bet_winner(timeStamp)
    ps38(timeStamp)
    detect_exception()


@shared_task()
def detect_task():
    lam()

@shared_task()
def remove_data_task():
    remove_data()

