import json
from datetime import date, datetime, timedelta
from pprint import pprint
import time, logging, os, signal, argparse
import daemon

import telegram
from app_store_scraper import AppStore
from google_play_scraper import app, Sort, reviews, reviews_all

from tinydb import Query, TinyDB


ios_app_list = ["1071766252"]
aos_app_list = ["kr.co.jbbank.smartbank"]
str_stars = "★★★★★"

telegram_bot_tokens = '1426590377:AAH7IYl_vZdfcClQcw-PcCkvfkF7cu0S4LQ' #토큰을 설정해 줍니다.
pid_file = './pidfile.pid'

def main():
    try:
        if sys.argv[1] == 'start':
            start_daemon()
        
        elif sys.argv[1] == 'stop':
            pid = '999999'
            f = open(pid_file, 'r')
            for line in f:
                pid = line = line.strip()

            f.close()
            cmd = 'kill '+ pid
            os.system(cmd)
            
    except Exception as e:
        print(e)
        
def start_daemon():
    print('Start Daemon')
    with daemon.DaemonContext(
        working_directory = '/tmp',
        umask = 0o002,
        pidfile = pidfile.TimeoutPIDLockFile(pid_file),
        ) as context:
        do_scrap_review()

if __name__ == "__main__":
    main()

def send_message(txt):
    bot = telegram.Bot(token = telegram_bot_tokens) #봇을 생성합니다.
    bot.sendMessage(chat_id='@JBSmbReview', text=str(txt))#review 채널로 메시지 전송

def do_scrap_review():
    for i in ios_app_list:
        ios_review_scrap('kr', i, 20, 10)
    
    for j in aos_app_list:
        aos_review_scrap('kr','ko', j, 10)

def ios_review_scrap(countryCode, appId, reviewCount, afterDay):
    review_db = TinyDB('ios_reviews.json')
    appReview = review_db.table('review_'+appId)
    previous_date = datetime.now() - timedelta(days=afterDay)

    jbsmartbank = AppStore(country=countryCode, app_name="", app_id=appId)
    jbsmartbank.review(how_many=reviewCount, after=previous_date)
    jbreview = sorted(jbsmartbank.reviews, key=(lambda x: x['date']),reverse=False)

    for review in jbreview:
        review['date'] = review['date'].strftime('%Y-%m-%d %H:%M:%S')    
        if not (appReview.search(Query().date == review['date'])):
            reviewStr = "🍎앱스토어(뉴스마트뱅킹) 리뷰 등록!\r\n";
            reviewStr += "일  시 : " + review['date']          + "\r\n";
            reviewStr += "평  점 : " + str_stars[0:(review['rating'])] + "\t수정여부 : " + str(review['isEdited']) + "\r\n\r\n"
            reviewStr += "작성자 : " + review['userName']      + "\r\n"
            reviewStr += "제  목 : " + review['title']         + "\r\n"
            reviewStr += "내  용 : " + review['review']       ;
            appReview.insert(review)
            send_message(reviewStr)

def aos_review_scrap(countryCode,langCode,appId,reviewCount):
    review_db = TinyDB('aos_reviews.json')
    appReview = review_db.table('review_'+appId)

    aosReviews, continuation_token = reviews(
        appId,
        lang=langCode, # defaults to 'en'
        country=countryCode, # defaults to 'us'
        sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
        count=reviewCount # defaults to 100
        #filter_score_with=5 # defaults to None(means all score)
    )
    print(aosReviews)

    for review in aosReviews:
        if not (appReview.search(Query().at == review['at'])):
            reviewStr = "플레이스토어(뉴스마트뱅킹) 리뷰 등록!\r\n";
            reviewStr += "일  시 : " + review['at']          + "\r\n";
            reviewStr += "평  점 : " + str_stars[0:(review['score'])] 
            reviewStr += "앱버전 : " + review['reviewCreatedVersion'] + "\r\n\r\n"
            reviewStr += "작성자 : " + review['userName']      + "\r\n"
            #reviewStr += "제  목 : " + review['title']         + "\r\n"
            reviewStr += "내  용 : " + review['content']       ;

            appReview.insert(review)
            send_message(reviewStr)
