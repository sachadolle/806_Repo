#LIBRARIES

import requests as r
import pandas as pd
import json
from pandas.io.json import json_normalize
import re
from bs4 import BeautifulSoup
import math

#GET DATA

headers="""accept: */*
accept-encoding: gzip, deflate, br
accept-language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7
cache-control: no-cache
cookie: PHPSESSID=5v0907emsmhjb91ab8af2uvu1q; locale_code=fr-FR; platform=desktop; par_sess=h%3D-%26c%3D%26v%3D%26t%3D0%26s%3D; partner_expires=2678400; partner_id=-; cur=EUR; visitor_id=4H8ABT3TO1R9Z46DVEXN6GS3OMQ43SF6; browser_support=modern; AP-VID=c73c70fc349b026bf93853cdfbae8931; _gcl_au=1.1.146597312.1593160775; HIA=IPv4-FR-00000002-9b4357007c325c99a0ada28b47f0e79025fe2b12834a1e76899d8c4f15a0e1229639237d592f46c6c4ba4c1807814c8fba99ca121a439f14acca54aa7074793b; isMobile=false; is_office_ip=false; TFE_DATE_FROM=; ab.storage.deviceId.32b57c7b-1181-4973-9f07-79cdd6d2c403=%7B%22g%22%3A%224850bf39-d263-58da-544a-779c0e1e6310%22%2C%22c%22%3A1593160777028%2C%22l%22%3A1593160777028%7D; ab.storage.sessionId.32b57c7b-1181-4973-9f07-79cdd6d2c403=%7B%22g%22%3A%223d8936ee-6572-9a1e-23f1-28f6f777f563%22%2C%22e%22%3A1593162577098%2C%22c%22%3A1593160777020%2C%22l%22%3A1593160777098%7D; __ssid=5da2157da6677e7046f2a10f8816cf5; one_tap_first_access=2020-06-26T08:39:39.227Z; OptanonConsent=isIABGlobal=false&datestamp=Fri+Jun+26+2020+10%3A40%3A02+GMT%2B0200+(heure+d%E2%80%99%C3%A9t%C3%A9+d%E2%80%99Europe+centrale)&version=6.0.0&landingPath=https%3A%2F%2Fwww.getyourguide.fr%2Fdiscovery%2F%3Futm_force%3D0&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0003%3A1&hosts=&legInt=&consentId=27af5126-9eb2-4fc1-b5c0-879037c5e899&interactionCount=0; SESSDATA=XvW0YQ.eyIxIjoiZnItRlIiLCIxOCI6ImRlc2t0b3AiLCIyIjoiRlIiLCIzIjoyNiwiNiI6IjI0LWhvdXIiLCI0IjoxLCI1IjoiNEg4QUJUM1RPMVI5WjQ2RFZFWE42R1MzT01RNDNTRjYiLCIyNCI6IklQdjQtRlItMDAwMDAwMDItOWI0MzU3MDA3YzMyNWM5OWEwYWRhMjhiNDdmMGU3OTAyNWZlMmIxMjgzNGExZTc2ODk5ZDhjNGYxNWEwZTEyMjk2MzkyMzdkNTkyZjQ2YzZjNGJhNGMxODA3ODE0YzhmYmE5OWNhMTIxYTQzOWYxNGFjY2E1NGFhNzA3NDc5M2IiLCIxOSI6ImIyNjk2Zjg4OGEwYjZlNzUzNzlmMDQyZWQ4Njc4M2Q4ODM4ODA2ZTYxNjViODVjNTExOTc5ZDA2NGM3ZWJhOTA1YWU2YTgyOWM1MzQzMzcyZWFlODhkYTYwMGQ5YmEwZDg5NDVhMTE5M2U3YzBlYjA5YzBiYzFhMTkxNDVlZTY4In0.ZivZN7IzZmPRbsEML2dh2VVJZofV8DJRDDO4JBFfcZc
pragma: no-cache
referer: https://www.getyourguide.fr/s/?q=France&searchSource=2
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
x-csrf-token: b2696f888a0b6e75379f042ed86783d8838806e6165b85c511979d064c7eba905ae6a829c5343372eae88da600d9ba0d8945a1193e7c0eb09c0bc1a19145ee68
x-gyg-ap-cntnr: Search
x-gyg-ap-vid: f996b1003ac662e5ec4945fb63fd5976
x-requested-with: XMLHttpRequest"""

headers=dict(i.split(': ') for i in headers.split('\n'))

import time

df=pd.DataFrame()
step=0
total_elements=1610
element_p_page=20
pagination=math.ceil(total_elements/element_p_page)+1

for i in range(pagination):
    j=math.floor(i/3.01)
    url=f'https://www.getyourguide.fr/s/results.json?&q=France&searchSource=2&p={i}&page={j}'    
    resp=r.get(url, headers=headers)
    
    if step%5==0:
        time.sleep(2.4) # sleep every five parsed page
        print (step, 'pages loaded')
        
    results=resp.json()
    data=json_normalize(results['searchResults']['tours'])
    df=df.append(data)

    step+=1
    

# COLUMNS

df=df.drop_duplicates(subset='tourId')

df=df.drop(columns=['tourId', 'horizontalImageUrl', 'verticalImageUrl', 'mobileImageUrl', 'horizontalSlimImageUrl', \
                 'description', 'isBestseller', 'isFeatured', 'hasDeal', 'dealMaxPercentage', 'isBoostedNewTour', 'hasBanner', \
                 'hasRibbon', 'priceTag', 'detailsLink', 'isCertifiedPartner', 'isEcoCertified', 'isFirstTicket', 'isAuthorizedReseller', \
                 'isGygOriginal', 'imageUrl', 'imageAlt', 'isFreeCancellation', 'smallGroup', 'privateTour', 'hasRating', \
                 'maxPossibleRating', 'totalRating', 'totalRatingTitle', 'averageRatingClass', 'ratingLink', 'languageIds',
                 'ratingStyleModifier', 'ratingStarsClasses', 'ratingTitle', 'hasDuration', 'useValidity', 'validFrom', \
                 'displayAbstract', 'displayDuration', 'displayDate', 'displayWishlist', 'isWishlistAccountWallEnabled', \
                 'displayRemoveButton', 'extraBadges', 'referrerViewPosition', 'hasDiscountedRecommendation', 'urlDetailsBtn', \
                 'hideImage', 'isLikelyToSellOut', 'cardBannerMessage', 'cardBannerType', 'isPromoted', 'isElevated', \
                 'isOutdoors', 'isFamilyFriendly', 'showSkywards', 'skywardsMiles', 'assetsPath', 'isSpecialOffer', \
                 'collectionIdentifier', 'id', 'activityCardVersion', 'limit', 'isLoggedIn', 'timeSlotsExperimentEnabled', \
                 'freeCancellationFlag', 'resultSetPosition', 'highlightedOrientation', 'price.type', \
                 'experiments.hasOriginalsMoneyBackLabel','keyDetails.cancellation_policy.label', 'keyDetails.duration.label',
                 'keyDetails.cancellation_policy.description', 'keyDetails.skip_the_line.label', 'keyDetails.duration.description',
                 'keyDetails.skip_the_line.description', 'keyDetails.instant_confirmation.label', 'keyDetails.instant_confirmation.description'])

df=df.rename(columns={'smallDescription': 'description',
                      'price.original': 'price_original', 'price.min':'price_min',
                      'averageRating':'rating'})

#DATA CLEANING

df['title']=df['title'].str.replace('&#039;', '\'')
df['title']=df['title'].str.replace('&quot;', '\"')
df['title']=df['title'].astype('str')

df['price_min']=df['price_min'].str.replace(" ", "").str.strip('€\xa0\n').str.replace(',', '.').astype('float')

df['price_original']=df['price_original'].str.replace(" ", "").str.strip('€\xa0\n').str.replace(',', '.').astype('float')

df['rating']=df['rating'].fillna('Not rated yet')

df['duration']=df['duration'].str.replace('heures', 'h')
df['duration']=df['duration'].str.replace('heure', 'h')
df['duration']=df['duration'].str.replace('jour', 'day')
df['duration']=df['duration'].str.replace('minutes', 'min')
df['duration']=df['duration'].str.replace(' - ', ' to ')
df['duration']=df['duration'].str.replace(',5 h', 'h30')
df['duration']=df['duration'].str.replace(',5', 'h30')
df['duration']=df['duration'].str.replace('2 880,00 min', '2 days')
df['duration']=df['duration'].str.replace('1 440,00 min', '1 day')
df['duration']=df['duration'].str.replace('90 min', '1h30')

"""
#GET CITIES
country=list()
region=list()
city=list()

for urls in df['url']:
    more_infos=r.get(urls, headers=headers)
    soup=BeautifulSoup(more_infos.content)
    place=str(soup.select('.activity__breadcrumbs ul li a'))
    names=re.findall(r'(>[A-z].*?<)', place)
    
    if names==True:  
        country.append(names[0].strip('><'))
        region.append(names[1].strip('><'))
        city.append(names[2].strip('><'))
    else:
        country.append(0)
        region.append(0)
        city.append(0)
        
df['country']=country
df['region']=region
df['city']=city        
"""


cols = df.columns.tolist()
"""
cols.insert(1, cols.pop(cols.index('country')))
cols.insert(2, cols.pop(cols.index('region')))
cols.insert(3, cols.pop(cols.index('city')))
"""
cols.insert(1, cols.pop(cols.index('title')))
cols.insert(2, cols.pop(cols.index('description')))
cols.insert(3, cols.pop(cols.index('price_min')))
cols.insert(4, cols.pop(cols.index('price_original')))
cols.insert(5, cols.pop(cols.index('rating')))
cols.insert(6, cols.pop(cols.index('duration')))
cols.insert(7, cols.pop(cols.index('url')))
df = df[cols]

df.reset_index(drop = True, inplace = True)

