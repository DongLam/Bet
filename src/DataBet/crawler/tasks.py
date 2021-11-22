from celery import shared_task

from crawler.craw import egb, bet_winner
from crawler.detect import detect
from crawler.tele_bot import send_message
from crawler.views import get_data_bet_winner


@shared_task()
def crawl_egb():
    egb()

@shared_task()
def crawl_bet_winner():
    bet_winner()

@shared_task()
def detect_task():
    get_data_bet_winner()

