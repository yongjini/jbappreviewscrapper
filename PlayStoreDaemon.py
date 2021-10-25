from pprint import pprint
from google_play_scraper import app, Sort, reviews, reviews_all

#appId = 'kr.co.jbbank.smartbank'
appId = 'kr.co.jbbank.privatebank'
result = app(
    appId,
    lang='ko', # defaults to 'en'
    country='kr' # defaults to 'us'
)
print (result)

"""
result, continuation_token = reviews(
   appId,
   lang='ko', # defaults to 'en'
   country='kr', # defaults to 'us'
   sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
   count=3 # defaults to 100
    #filter_score_with=5 # defaults to None(means all score)
)
print(result)

"""

# If you pass `continuation_token` as an argument to the reviews function at this point,
# it will crawl the items after 3 review items.
#result, _ = reviews(
#    appId,
#    continuation_token=continuation_token # defaults to None(load from the beginning)
#)

#print(result)

### all review 
#result = reviews_all(
#    appId,
#    sleep_milliseconds=0, # defaults to 0
#    lang='ko', # defaults to 'en'
#    country='kr', # defaults to 'us'    
#    sort=Sort.NEWEST # defaults to Sort.MOST_RELEVANT
#    #, count=3
#    #filter_score_with=5 # defaults to None(means all score)
#)

