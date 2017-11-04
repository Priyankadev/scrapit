#
# Script for scrapping products from Samsclub
#


import requests
from bs4 import BeautifulSoup
from utils import sleep_scrapper, get_request_headers


class Samsclub:

    def __init__(self):
        pass

    def run(self):

        for j in range(0, 2, 1):
            try:
                # url = base_url + str(j) + sufix
                url = 'https://www.samsclub.com/sams/coffee-tea-cocoa/1493.cp?xid=cat_sub&navAction=jump'
                print '[Samsclub] :: fetching data from url: ', url
                r = requests.get(url, headers=get_request_headers())

                if not r.status_code == 200:
                    print "[Samsclub] :: Failed to get content of url: %s" % url
                    return

                html_doc = r.content

                soup = BeautifulSoup(html_doc, 'html.parser')

                # parsing html content  to fet information about python developer
                for div in soup.find_all('div', class_='products-card'):
                    self.scrap_result_row(div)
                sleep_scrapper('Samsclub')

            except Exception as exp:
                print '[Samsclub] :: run() :: Got exception : %s' % exp

    def scrap_result_row(self, div):
        # name
        figure = div.find('figure', title='Full title')
        a = figure.find('a', class_='cardProdLink')
        figcaption = a.find('figcaption', class_='img-text').text.strip()
        print '[Samsclub] :: name: ', figcaption

        # rating
        rat = div.find('div', class_='cust-rating-details')
        cust_rating = rat.find('div', class_='cust-rating')
        rating_mem = cust_rating.find('span', class_='rating-mem').text.strip()
        print '[Samsclub] :: Rating: ', rating_mem

        # price
        prods_details = div.find('div', class_='prods-details')
        sc_price = prods_details.find('div', class_='sc-price-v2').text.strip()
        print '[Samsclub] :: price: ', sc_price

        # save Price
        prods_details = div.find('div', class_='prods-details')
        save = ''
        save_off = prods_details.find('div', class_='save-off-price')
        if save_off:
            save = save_off.text.strip()
            print '[Samsclub] :: save-price: ', save

if __name__ == '__main__':
    samsclub = Samsclub()
    samsclub.run()
