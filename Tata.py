import requests
from bs4 import BeautifulSoup as soup


def searchTata(name):
    header = {'Origin': 'https://www.1mg.com',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/83.0.4103.97 Safari/537.36 '
              }

    url = 'https://www.1mg.com/search/all?name=' + name
    html = requests.get(url=url, headers=header)

    bsobj = soup(html.content, "html.parser")
    product_price = []
    for name in bsobj.findAll('span', limit=None):
        if len(product_price) == 0:
            if name.has_attr('class') and len(name['class']) > 0 and name['class'][
                0].startswith(
                'style__discount-price'):
                product_price.append(name.text.replace('₹', '').replace('MRP', '').strip())
        else:
            break

    return product_price[0], url