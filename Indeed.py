#
# Script for scrapping jobs details from Indeed
#


import requests
from bs4 import BeautifulSoup
from utils import sleep_scrapper, get_request_headers


class Indeed:

    def __init__(self, pos, location):

        self.post = pos.replace(" ", "+")
        self.location = location.replace(" ", "+")

    def run(self):

        base_url = 'https://www.indeed.co.in/jobs?q=' \
              '%s&l=%s&start=' % (self.post, self.location)
        for j in range(0, 1000, 10):
            url = ''
            try:
                url = base_url + str(j)
                print '[Indeed] :: fetching data from url:', url
                r = requests.get(url, headers=get_request_headers())

                if not r.status_code == 200:
                    print "[Indeed] :: Failed to " \
                          "get content of url: %s" % url
                    return

                html_doc = r.content

                soup = BeautifulSoup(html_doc, 'html.parser')

                for div in soup.find_all('div'):
                    # ignore divs with classes
                    if not div.attrs.has_key('class'):
                        continue

                    cls = div.attrs['class']
                    if 'row' in cls and 'result' in cls:
                        self.scrap_result_row(div)
                        # break
                sleep_scrapper('IndeedScraper')
            except Exception as exp:
                print '[IndeedScraper] :: run() :: Got exception : ' \
                      '%s and fetching data from url: %s' % (exp, url)

    def scrap_result_row(self, div):

        try:
            # title
            title = div.find('span', class_='company').text.strip()
            print "[Indeed] :: title: %s" % title

            # location
            span = div.find('span', class_='location')
            location = span.text.strip()
            print "[Indeed] :: location: %s" % location

            # salary
            sal = ''
            span = div.find('span', class_='no-wrap')
            if span:
                sal = span.text.strip()
                print "[Indeed] :: salary: %s" % sal

            # summary
            span = div.find('span', class_='summary')
            summary = span.text.strip()
            print "[Indeed] :: summery: %s" % summary
        except Exception as exp:
            print '[Indeed] :: scrap_result_row() :: ' \
                  'Got exception : %s' % exp

if __name__ == '__main__':
    scraper = Indeed('java', 'mohali punjab')
    scraper.run()
