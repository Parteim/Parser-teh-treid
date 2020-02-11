import requests
from bs4 import BeautifulSoup as BS

url = 'http://teh-treid.com/catalog-zapchasti/zapchasti-k-dvigatelyam-honda/zapchasti-honda-gxh50/'

soup = BS(requests.get(url).content, 'html.parser')

category_url = soup.find('div', class_='breadcrumbs')

main_category = category_url.find_all('a')[2].text
category = category_url.find('div', class_='wire').text.split('|')[-1]

print(category_url)