from bs4 import BeautifulSoup
import requests

# Url to scrape data
url = 'http://alertas.mma.gob.cl/santiago/'


def get_air_status(url=url):
    req = requests.get(url)

    # Make a soup
    soup = BeautifulSoup(req.content, 'html.parser')

    h4s = soup.find_all('h4')[1]
    air_status = h4s.text

    # Parse double spaces
    air_status = air_status.replace('  ', ' ')

    return air_status


if __name__ == '__main__':
    air_status = get_air_status(url)
    print(air_status)
