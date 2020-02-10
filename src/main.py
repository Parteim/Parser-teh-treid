import requests
from bs4 import BeautifulSoup as BS
import time

url = 'http://teh-treid.com/'


def run():
    start = time.time()
    response = requests.get(url)

    soup = BS(response.content, 'html.parser')

    links_list = soup.find_all('div', class_='spisok')[1].find_all('a', class_='mobcatl')

    item_url = []

    for link in links_list:
        if 'Запчасти' in link.text:
            item_url.append(link)

    print(item_url)

    end = time.time()
    print(end - start)


if __name__ == '__main__':
    run()