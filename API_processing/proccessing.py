import requests
from langdetect import detect
import random
from config import API_TOKEN as API
from config import API_LINK_TRENDING as TRENDING
from config import API_LINK_RANDOM as RANDOM
from config import API_LINK_SEARCH as SEARCH


async def rating_proccess(message):
    if message == 'Любые':
        return 'r'
    elif message == 'Умеренно адекватные':
        return 'pg-13'
    else:
        return 'g'


async def trending_process():
    params = {"api_key": API, "limit": 50}
    response = requests.get(TRENDING, params=params)
    gif_number = random.randrange(0, len(response.json()['data']), 1)
    data = response.json()['data'][gif_number]
    link = str(data["images"]["original"]["url"])
    return link


async def random_process():
    params = {"api_key": API}
    response = requests.get(RANDOM, params=params)
    data = response.json()["data"]
    link = str(data["images"]["original"]["url"])
    return link


'''async def search_process(data):
    params = {"api_key": API, "q": data['query'], "limit": 80, "offset": 0, "rating": data['rating'],
              "lang": detect(data['query'])}
    response = requests.get(SEARCH, params=params)
    if len(response.json()['data']) > 0:
        gif_number = random.randrange(0, len(response.json()['data']), 1)
        data = response.json()['data'][gif_number]
        link = str(data["images"]["original"]["url"])
        return link
    else:
        return False #Старый и плохой код'''


async def get_response(data):
    try:
        lang = detect(data['query'])
    except:
        lang = "en"

    params = {"api_key": API, "q": data['query'], "limit": 75, "offset": 0, "rating": data['rating'],
              "lang": lang}
    response = requests.get(SEARCH, params=params)
    return response.json()


async def get_gif_link(response):
    if len(response['data']) > 0:
        gif_number = random.randrange(0, len(response['data']), 1)
        gif = response['data'][gif_number]
        link = str(gif["images"]["original"]["url"])
        response['data'].pop(gif_number)
        return link
    else:
        return False

#Сделать бд где хранить кол-во гифок для юзера и можно статистику вызывать