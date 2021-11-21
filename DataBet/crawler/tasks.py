from celery import shared_task

from crawler.craw import egb, bet_winner


@shared_task()
def crawl_egb():
    egb()

@shared_task()
def crawl_bet_winner():
    bet_winner()