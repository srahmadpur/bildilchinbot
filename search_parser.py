import requests
import json
import simplejson
from random import randint
from bs4 import BeautifulSoup

word_list = []

class word_info:
    def __init__(self, name, w_info, dict_name):
        self.name = name
        self.w_info = w_info
        self.dict_name = dict_name
        parsed_html = BeautifulSoup(self.w_info, 'html.parser')   
        self.w_info = parsed_html.get_text()




def dict_search(word="", lang="", encoding="utf-8"):
    url = 'https://bildilchin.az:8888/bildilchin/get/description?selectedWord=' + str(word.lower()) + '&indexLang='
    lang_list = ["az", "ru", "en"]
    if lang not in lang_list:
        raise ValueError("Lang not in lang_list [az,ru,en]")
        # pass
    else:
        try:
            response = requests.get(url + lang)
            data = response.json()
            global word_list
            if len(data) > 0:
                for i in data:
                    word_list.append(word_info(randint(1,50), i["description"] , i["dictionary"]["name{}".format(lang.capitalize())]))
                return word_list
            else:
                return "Word_Not_Found"
        except simplejson.errors.JSONDecodeError:
            return "Word_Not_Found"
        except requests.exceptions.RequestException:
            return "Word_Not_Found"

