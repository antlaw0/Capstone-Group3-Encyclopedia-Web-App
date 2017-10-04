import tweepy
import json


def getTweet():
    ACCESS_KEY = "2925298300-BJWap1LPjwmIstGymM8YmatE2SwvIE2VcWCObR0"
    ACCESS_SECRET = "99x1P3GY71iIQQ82Nqs4pyRas8A4937dgfuX1JHmV6ZH6"
    CONSUMER_KEY = "NXPlKLEEXY5rIXbDIXMKoxS9r"
    CONSUMER_SECRET = "jLD3RMlsISibKCszIkHkhGFLPdpAtH63xbH1kTo1T83XBna1hH"
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    bannas = api.search("Bananas")
    for b in bannas:
        print(b.text)