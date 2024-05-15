import requests
from bs4 import BeautifulSoup as soup


def searchPE(name):
    header = {'Origin': 'https://pharmeasy.in/',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/83.0.4103.97 Safari/537.36 '
              }

    url = 'https://pharmeasy.in/search/all?name=' + name
    html = requests.get(url=url, headers=header)

    bsobj = soup(html.content, "html.parser")
    product_price = []
    for name in bsobj.findAll('div', limit=None):
        if len(product_price) == 0:
            if name.has_attr('class') and len(name['class']) > 0 and name['class'][
                0].startswith(
                    'ProductCard_ourPrice'):
                product_price.append(name.text.replace('₹', '').replace('MRP', '').replace('*', '').strip())
        else :
            break

    return product_price[0], url

