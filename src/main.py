import requests
from bs4 import BeautifulSoup as BS
import time
import xlwt

urls_items_list = []

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

ws.write(0, 0, '_ID_')
ws.write(0, 1, '_MAIN_CATEGORY_')
ws.write(0, 2, '_CATEGORY_')
ws.write(0, 3, '_NAME_')
ws.write(0, 4, '_SKU_')
ws.write(0, 5, '_MANUFACTURER_')
ws.write(0, 6, '_PRICE_')
ws.write(0, 7, '_QUANTITY_')
ws.write(0, 8, '_DESCRIPTION_')
ws.write(0, 9, '_IMAGE_')
ws.write(0, 10, '_STATUS_')
ws.write(0, 11, '_ATTRIBUTES_')
ws.write(0, 12, '_IMAGES_')


def request(url, **kwargs):
    response = requests.get(
        url,
        params=kwargs
    )
    return response.content


# def writer(items_list, base_url):
#     wb = xlwt.Workbook()
#     ws = wb.add_sheet('A Test Sheet')
#
#     ws.write(0, 0, '_ID_')
#     ws.write(0, 1, '_MAIN_CATEGORY_')
#     ws.write(0, 2, '_CATEGORY_')
#     ws.write(0, 3, '_NAME_')
#     ws.write(0, 4, '_SKU_')
#     ws.write(0, 5, '_MANUFACTURER_')
#     ws.write(0, 6, '_PRICE_')
#     ws.write(0, 7, '_QUANTITY_')
#     ws.write(0, 8, '_DESCRIPTION_')
#     ws.write(0, 9, '_IMAGE_')
#     ws.write(0, 10, '_STATUS_')
#     ws.write(0, 11, '_ATTRIBUTES_')
#     ws.write(0, 12, '_IMAGES_')
#
#     for num, item in enumerate(items_list, 1):
#
#         try:
#             soup = BS(
#                 request(
#                     base_url + item
#                 ),
#                 'html.parser',
#             )
#
#             category_url = soup.find_all('div', class_='breadcrumbs')[0].find_all('a')
#
#             main_category = category_url[2].text
#             category = category_url[3].text
#             name = soup.find('div', class_='zagolovok').text
#             sku = soup.find('div', class_='articul').text.split(' ')[1]
#             price = soup.find('div', class_='price').text
#
# print(
#     f'main_category: {main_category}\n'
#     f'category: {category}\n'
#     f'name: {name}\n'
#     f'sku: {sku}\n'
#     f'price: {price}\n'
# )
#
# ws.write(num, 0, num)
# ws.write(num, 1, main_category)
# ws.write(num, 2, category)
# ws.write(num, 3, name)
# ws.write(num, 4, sku)
# ws.write(num, 6, price)

#             wb.save('items.xls')
#         except:
#             pass


def get_items(url):
    number = 1
    while True:
        try:
            soup = BS(
                request(
                    url,
                    PAGEN_1=number
                ),
                'html.parser',
            )

            articul = soup.find_all('div', class_='articul')

            for item in articul:
                item_url = item.parent.find('a').attrs['href']
                if item_url not in urls_items_list:
                    urls_items_list.append(item_url)

                    num = len(urls_items_list)

                    category_url = soup.find_all('div', class_='breadcrumbs')[0]

                    main_category = category_url.find('div', class_='wire').text.split('|')[-1]
                    category = soup.find('div', class_='zagolovok').text
                    name = item.parent.find('div', class_='name').text
                    sku = item.parent.find('div', class_='articul').text.split(' ')[1]
                    price = item.parent.find('div', class_='price').find('span').text

                    print(
                        f'main_category: {main_category}\n'
                        f'category: {category}\n'
                        f'name: {name}\n'
                        f'sku: {sku}\n'
                        f'price: {price}\n'
                    )

                    ws.write(num, 0, num)
                    ws.write(num, 1, main_category)
                    ws.write(num, 2, category)
                    ws.write(num, 3, name)
                    ws.write(num, 4, sku)
                    ws.write(num, 6, price)

                    wb.save('items.xls')

                    print(item_url, '\n', len(urls_items_list))

            number += 1
            if number == 7:
                return urls_items_list
        except:
            pass


def get_urls_items_page(soup):
    links_list = soup.find_all('a')

    for i in links_list:
        if i.text == 'Запчасти и расходные материалы ':
            items_url = i.parent.find_all('a', class_='mobcatl')
            return items_url


def get_item_info(soup):
    name = soup.find('div', class_='zagolovok').text
    SKU = soup.find('div', class_='articul').text
    price = soup.find('div', class_='price').text

    return {
        'name': name,
        'SKU': SKU,
        'price': price,
    }


def run():
    url = 'http://teh-treid.com'
    start = time.time()

    items_list = []
    soup = BS(request(url), 'html.parser')

    pages_item_urls = get_urls_items_page(soup)

    for counter, item in enumerate(pages_item_urls, 1):
        if counter == 1:
            pass
        elif len(urls_items_list) >= 7000:
            break
        else:
            print(f'============================\n{item}')
            items_list.extend(get_items(
                url + item.attrs['href']
            ))

            print(items_list)

    # writer(urls_items_list, url)

    end = time.time()
    print(end - start)


if __name__ == '__main__':
    run()
