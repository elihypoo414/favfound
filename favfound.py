import argparse
import base64
import json
import mmh3
import os
import random
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from config import headers


class FavFound:
    def __init__(self, args):
        if args.auth:
            if os.path.exists('config/.apikey.auth'):
                exit("Active authentication detected. If you want to re-authenticate with another api key, delete/edit the current .apikey.auth file")
            else:
                with open('config/.apikey.auth', 'w') as file:
                    self.api_key = args.auth
                    file.write(self.api_key)
                    file.close()
                exit("api key is Successfully saved to the .apikey.auth file")
        else:
            with open('config/.apikey.auth', 'r') as file:
                self.api_key = file.readline().strip()

        self.url = 'https://api.criminalip.io/v1/banner/search'
        self.headers = {
            "x-api-key": self.api_key,
            "User-Agent": random.choice(headers.user_agents)
        }

        if args.ip:
            self.get_favicon_hash_from_ip()
        elif args.fav_hash_from_ip:
            self.get_favicon_ip_info()
        elif args.fav_hash_from_ico:
            self.get_favicon_hash_from_ico(args.fav_hash_from_ico)
        elif args.fav_hash_from_web:
            self.get_favicon_hash_from_web(args.fav_hash_from_web)

        if args.read:
            self.read_file(args.read)

    def get_favicon_hash_from_ip(self):
        params = {
            'query': 'ip : {}'.format(args.ip),
            'offset': 0,
        }
        res = requests.get(url=self.url, params=params, headers=self.headers)
        res = res.json()

        favicon_list = set()
        if res['status'] == 200 and res['data']['count'] > 0:
            for r in res['data']['result']:
                if r['favicons']:
                    favicon_list.update(favicon['hash'] for favicon in r['favicons'])

        print("{}'s favicon hex values are below : \n{}".format(args.ip, ', '.join(favicon_list)))

    def get_favicon_ip_info(self):
        params = {
            'query': 'favicon : {}'.format(args.fav_hash_from_ip),
            'offset': 0,
        }
        res = requests.get(url=self.url, params=params, headers=self.headers)
        res = res.json()

        ret_data = []
        if res['status'] == 200:
            for r in res['data']['result']:
                ret_data.append(
                    {
                        'status_code': r['status_code'],
                        'ip_address': r['ip_address'],
                        'open_port_no': r['open_port_no'],
                        'banner': r['banner'],
                        'product': r['product'],
                        'product_version': r['product_version'],
                        'scan_dtime': r['scan_dtime'],
                        'city': r['city'],
                        'country': r['country'],
                        'favicons': r['favicons'],
                        'title': r['title'],
                        'html_author': r['html_meta_author'],
                        'html_description': r['html_meta_description'],
                        'html_keywords': r['html_meta_keywords'],
                        'html_title': r['html_meta_title'],
                    }
                )

        if args.output:
            self.output(ret_data)

        pprint(ret_data)

    def get_favicon_hash_from_ico(self, ico_path):
        with open(ico_path, 'rb') as ico_file:
            ico_base64_data = base64.encodebytes(ico_file.read())

        hex_hash_val = hex(mmh3.hash(ico_base64_data))[2:]
        print("{}'s hashed favicon hex value is below : \n{}".format(ico_path, hex_hash_val))

    def get_favicon_hash_from_web(self, url):
        response = requests.get(url, stream=True, verify=False)
        bs = BeautifulSoup(response.content, 'html.parser')
        fav_icon = bs.find('link', rel='icon')

        if fav_icon:
            fav_icon_link = fav_icon.get('href')
            if not fav_icon_link.startswith('http'):
                fav_icon_link = '/'.join([args.fav_hash_from_web, fav_icon_link])

            res = requests.get(fav_icon_link, verify=False)
        else:
            exit("favicon from {} has not found".format(args.fav_hash_from_web))

        web_base64_data = base64.encodebytes(res.content).decode()
        hex_hash_val = hex(mmh3.hash(web_base64_data))
        if hex_hash_val.startswith('-'):
            hex_hash_val = '-' + hex_hash_val[3:]
        else:
            hex_hash_val = hex_hash_val[2:]

        print("{}'s hashed favicon hex value is below : \n{}".format(args.fav_hash_from_web, hex_hash_val))

    def output(self, result):
        file_path = "{}".format(args.output)

        with open(file_path, "w") as file:
            file.write("{}".format(json.dumps(result)))
            file.close()

    def read_file(self, file_path):
        with open("{}".format(args.read), "r") as file:
            for r in file:
                pprint(json.loads(r))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='{}'.format('Zvan - by criminalip'), epilog='{}'.format('TEST'))
    parser.add_argument('-A', '--auth', help='api authentication with a valid criminalip.io api key', metavar='<api_key>')
    parser.add_argument('-I', '--ip', help='Return favicon hash from an IP', metavar='<ip>')
    parser.add_argument('-F', '--fav-hash-from-ip', help='Return information about IP which has the favicon hash', metavar='<favicon_hash_from_ip>')
    parser.add_argument('-C', '--fav-hash-from-ico', help='Return converted favicon hash from favicon icon', metavar='<favicon_hash_from_ico>')
    parser.add_argument('-W', '--fav-hash-from-web', help='Return converted favicon hash from website', metavar='<favicon_hash_from_web>')
    parser.add_argument('-O', '--output', help='write output to a file', metavar='<path/to/file>')
    parser.add_argument('-R', '--read', help='read file and pretty print the information', metavar='<path/to/file>')

    args = parser.parse_args()

    favfound = FavFound(args)
