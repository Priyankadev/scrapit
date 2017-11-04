#
# script for scrapping missing chlidren from missingkids
#


import requests
import traceback
from bs4 import BeautifulSoup
from utils import sleep_scrapper, get_request_headers


class MissingKids:

    def __init__(self):
        pass

    def run(self):
        try:
            url = 'https://api.missingkids.org/missingkids/servlet/PubCaseSearchServlet?' \
                  'act=usMapSearch&missState=VA&searchLang=en_US&casedata=latest'
            r = requests.get(url, headers=get_request_headers())
            if not r.status_code == 200:
                print '[MissingKids] :: faild to get content of url: %s' % url
                return
            html_doc = r.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            for td in soup.find_all('td', width="40%"):
                # print '--------td', td
                self.scrap_result_row(td)
            # sleep_scrapper('MissingKids')
        except Exception as exp:
            print '[MissingKids] :: run() :: Got exception: %s' % exp
            print(traceback.format_exc())

    def scrap_result_row(self, td):
        a = td.find('a')

        # name
        b = a.find('b').text.strip()
        print '[MissingKids] :: Name: ', b

        # bs = td.find_all('b')
        bs = td.find_all('b')
        # y = bs.strip().split(",")
        print '[MissingKids] :: details', bs

        # alerts
        span = td.find('span', class_='alerts').text.strip()
        print '[MissingKids] :: span: ', span

if __name__ == '__main__':
    scraper = MissingKids()
    scraper.run()
