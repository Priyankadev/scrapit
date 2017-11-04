#
# Script for scrapping products from HomeDepot
#


import requests
from bs4 import BeautifulSoup
from utils import sleep_scrapper, get_request_headers


class HomeDepot:

    def __init__(self, product):
        self.product = product.replace(" ", "-")

    def run(self):

        base_url = 'https://www.homedepot.com/b/' \
                   '%s/N-5yc1vZbm79?Nao=' % (self.product)
        sufix = '&Ns=None'

        for j in range(0, 1000, 12):
            url = ''
            try:
                url = base_url + str(j) + sufix
                print '[HomeDepot] :: fetching data from url: ', url
                r = requests.get(url, headers=get_request_headers())
                if not r.status_code == 200:
                    print "[HomeDepot] :: Failed to get " \
                          "content of url: %s" % url
                    return
                html_doc = r.content

                soup = BeautifulSoup(html_doc, 'html.parser')

                for div in soup.find_all('div', class_='pod-inner'):
                    self.scrap_result_row(div)
                sleep_scrapper('HomeDepot')
            except Exception as exp:
                print '[HomeDepot] :: run() :: Got exception : ' \
                      '%s and fetching data from url: %s' % (exp, url)

    def scrap_result_row(self, div):

        try:
            # name
            name = div.find('div', class_='pod-plp__description '
                                      'js-podclick-analytics').text.strip()
            print '[HomeDepot] :: name: ', name

            # model
            model = div.find('div', class_='pod-plp__model').text.strip()
            print '[HomeDepot] :: model: ', model

            # price
            price = div.find('div', class_='price').text.strip()
            print '[HomeDepot] :: price: ', price

            # stock
            stock = div.find('div', class_='pod-plp__shipping-message__'
                                           'wrapper-boss-bopis').text.strip()
            print '[HomeDepot] :: stock: ', stock
        except Exception as exp:
            print '[HomeDepot] :: scrap_result_row() :: ' \
                  'Got exception : %s' % exp

if __name__ == '__main__':
    homedepot = HomeDepot('Holiday Decorations Fall Decorations Fall Garland-Wreaths')
    homedepot.run()
