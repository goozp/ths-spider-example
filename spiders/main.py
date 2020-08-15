
import os
import time
import schedule


def job():
    os.system("scrapy crawl ths-stock")
    os.system("scrapy crawl ths-stock-daily")
    os.system("scrapy crawl ths-stock-news")

def newsJob():
    os.system("scrapy crawl ths-news")

if __name__ == "__main__":
    newsJob()
    job()
    schedule.every().day.at('21:00').do(job)
    schedule.every(2).minutes.do(newsJob)
    while True:
        schedule.run_pending()
        time.sleep(1)