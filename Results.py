import wikipedia
import tweepy
from flickrapi import FlickrAPI
import os


# 0: Twitter
# 1: Wikipedia
# 2: Flickr

def get_result(api_raw, search_text):


    result_text = []
    result_images = []

    api_raw = str(api_raw)
    api = get_api(api_raw.lower())
    if api == 0:
        # Twitter

        ACCESS_KEY = os.environ.get('ACCESS_KEY')
        ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
        CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
        CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')


        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)
        twitter_search = api.search(search_text)
        index = 0
        for result in twitter_search:
            if index <10:
                result_text.append(result.text)
                index += 1


    elif api == 1:
        # Wikipedia
        try:
            wikiPage = wikipedia.page(search_text)
            result_text = wikiPage.summary
            result_images = wikiPage.images
        #handles if a search term could have more than one result, chooses the first suggested one
        except wikipedia.exceptions.DisambiguationError as e:
            print(e.options)
            search_text = e.options[0]
            print(search_text)
            wikiPage = wikipedia.page(search_text)
            result_text = wikiPage.summary
            result_images = wikiPage.images


    elif api == 2:
        # Flickr
        FLICKR_PUBLIC = os.environ.get('FLICKR_PUBLIC')
        FLICKR_SECRET = os.environ.get('FLICKR_SECRET')
        flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
        extras = 'url_c,url_l,url_o'
        results = flickr.photos.search(tags=search_text, per_page=25, extras=extras)
        for rslt in results['photos']['photo']:
            if 'url_l' in rslt:
                result_images.append(rslt['url_l'])
            elif 'url_c' in rslt:
                result_images.append(rslt['url_c'])
            elif 'url_o' in rslt:
                result_images.append(rslt['url_o'])
            if 'title' in rslt:
                title = str(rslt['title'])
                if len(title) > 0:
                    lines = title.splitlines()



    return result_text,result_images


def get_api(api_raw):
    if api_raw.startswith('t'):
        return 0
    if api_raw.startswith('w'):
        return 1
    if api_raw.startswith('f'):
        return 2
    if api_raw.startswith('0'):
        return 0
    if api_raw.startswith('1'):
        return 1
    if api_raw.startswith('2'):
        return 2
