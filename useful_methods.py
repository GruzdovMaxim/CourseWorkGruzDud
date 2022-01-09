import codecs
import json

import requests
from bs4 import BeautifulSoup


def get_all_city_names_wiki():
    link = \
        "https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%A3%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D1%8B"

    response = requests.get(link).text

    the_soup = BeautifulSoup(response, 'lxml')

    blocks = the_soup.find('div',
                           class_=
                           "mw-parser-output").find_all('tr')

    whole_data = {}
    for one_city_name in [temp.text.split("\n")[3] for temp in blocks[60:520]]:
        temp_rus_name = one_city_name.split("(укр. ")[0]
        if temp_rus_name[-4:] == "[30]":
            temp_rus_name = temp_rus_name[:-4]
        whole_data[temp_rus_name] = one_city_name.split("(укр. ")[1][:-1]

    return whole_data


def set_info_files():
    with codecs.open("all_city_names.json", "w", encoding='utf-8') as outfile:
        json.dump(get_all_city_names_wiki(), outfile, indent=4, ensure_ascii=False)


def get_ukr_city_name_by_rus(arg_rus_city_name):
    arg_rus_name = arg_rus_city_name.lower().title()
    with codecs.open("all_city_names.json", "r", encoding='utf-8') as data_file:
        data_dict = json.load(data_file)
    if arg_rus_name in data_dict.keys():
        return data_dict[arg_rus_name]
    elif arg_rus_name in data_dict.values():
        return arg_rus_name


def get_busyness_num(arg_name):
    if arg_name == "Полная занятость":
        return 1
    if arg_name == "Неполная занятость":
        return 2
    if arg_name == "Удаленная работа":
        return 3


def func(temp_var):
    temp_var = temp_var.lower().title()
    with codecs.open("all_city_names.json", "r", encoding='utf-8') as data_file:
        data = json.load(data_file)
        if temp_var in data.keys() or temp_var in data.values():
            return True
    return False


if __name__ == '__main__':
    print(get_ukr_city_name_by_rus("Киев"))
