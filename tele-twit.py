import json 
import requests
import urllib
import tweepy
import json
from tweepy import OAuthHandler

TOKEN = ""
URL = "https://api.telegram.org/bot{fill api token}/".format(TOKEN)


def config_twitt():
    fo = open("config.json", "r")
    str = fo.read()
    d = json.loads(str)
    fo.close()
    return  d

def config_cache():
    fo = open("cache.json", "r")
    str = fo.read()
    d = json.loads(str)
    fo.close()
    return  d

dict_cache=config_cache()

twit_c = config_twitt()
print twit_c

consumer_key = twit_c['consumer_key']
consumer_secret = twit_c['consumer_secret']
access_token = twit_c['access_token']
access_secret = twit_c['access_secret']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)




def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    print text
    get_url(url)

def put_db_cache(config):
    fo = open("cache.json", "wb")
    fo.write(json.dumps(config))
    fo.close()

def get_db_cache():
    pass


# status = tweepy.Cursor(api.home_timeline).items(10)
# print status
db_cache = {}

for status in tweepy.Cursor(api.home_timeline).items(10):
    # print json.dumps(status)
    print status.id
    if status.id in dict_cache:
        print "already exist"
    else:
        print "send tele"
        n = status._json["user"]["screen_name"]
        s = str(status.text.encode('utf-8'))
        text = str("@".encode('utf-8'))+str(n.encode('utf-8')) + " said " + s
        send_message(text, "@tesgahol")

    db_cache[status.id] = "1"

put_db_cache(db_cache)