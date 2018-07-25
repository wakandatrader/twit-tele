import json 
import requests
import urllib
import tweepy
import json
from tweepy import OAuthHandler

TOKEN = ""
URL = "https://api.telegram.org/bot{fill api key}/".format(TOKEN)
path = ""

def config_twitt():
    fo = open(path+"config.json", "r")
    str = fo.read()
    d = json.loads(str)
    fo.close()
    return  d

def config_cache():
    fo = open(path+"cache.json", "r")
    str = fo.read()
    d = json.loads(str)
    fo.close()
    return  d

def  whitelist_text():
    fo = open(path+"whitelist.txt", "r")
    str = fo.read()
    d = str.splitlines()
    fo.close()
    return  d


dict_cache=config_cache()

twit_c = config_twitt()
whitelist_arr = whitelist_text()


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
    get_url(url)

def put_db_cache(config):
    fo = open(path+"cache.json", "wb")
    fo.write(json.dumps(config))
    fo.close()


db_cache = {}
whitelist_arr = whitelist_text()
print whitelist_arr
for status in tweepy.Cursor(api.home_timeline).items(10):
    if str(status.id) in dict_cache:
        print str(status.id) + " already exist"
    else:
        #if "listing" in status.text:
        n = status._json["user"]["screen_name"]
        s = str(status.text.encode('utf-8'))
        if [status.text for wtext in whitelist_arr if(wtext in status.text)]:
            text = str("@".encode('utf-8'))+str(n.encode('utf-8')) + " said " +$
            send_message(text, "@tesgahol")
            print str(status.id) + " send tele"
        else:
            print str(status.id) + " not in list"
    db_cache[status.id] = status.id

put_db_cache(db_cache)

