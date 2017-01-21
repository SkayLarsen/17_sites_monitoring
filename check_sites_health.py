import argparse
import os
import pythonwhois
import requests
import urllib.parse
from datetime import datetime, timedelta


def load_urls4check(path):
    if not os.path.exists(path):
        return None
    with open(path) as url_file:
        return url_file.read().splitlines()


def is_server_respond_with_200(url):
    return requests.get(url).status_code == 200


def get_domain_expiration_date(domain):
    exp_date = pythonwhois.get_whois(domain).get('expiration_date', None)
    if exp_date:
        return exp_date[0]


def is_domain_paid(url, days=30):
    domain = urllib.parse.urlparse(url).netloc
    exp_date = get_domain_expiration_date(domain)
    if exp_date:
        return datetime.now() + timedelta(days) < exp_date


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Проверка состояния сайта')
    argparser.add_argument('filepath', help='Путь к файлу с адресами')
    args = argparser.parse_args()
    urls = load_urls4check(args.filepath)
    for url in urls:
        if is_server_respond_with_200(url):
            if is_domain_paid(url):
                print("Сайт {} доступен и доменное имя сайта проплачено как минимум на 1 месяц вперед".format(url))
            else:
                print("Сайт {} доступен, но доменное имя сайта не проплачено на следующий месяц".format(url))
        else:
            print('Сайт {} недоступен'.format(url))
