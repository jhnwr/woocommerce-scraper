from requests_html import HTMLSession
import csv
import time

s = HTMLSession()
url = 'https://barefootbuttons.com/product-category/version-1/'

def get_links(url):
    r = s.get(url)
    items = r.html.find('div.product-small.box')
    links = []
    for item in items:
        links.append(item.find('a', first=True).attrs['href'])
    return links

def get_productdata(link):
    r = s.get(link)
    title = r.html.find('h1', first=True).full_text
    price = r.html.find('span.woocommerce-Price-amount.amount bdi')[1].full_text
    tag = r.html.find('a[rel=tag]', first=True).full_text
    sku = r.html.find('span.sku', first=True).full_text

    product = {
        'title': title.strip(),
        'price': price.strip(),
        'tag': tag.strip(),
        'sku': sku.strip()
    }
    print(product)
    return product

results = []
links = get_links(url)

for link in links:
    results.append(get_productdata(link))
    time.sleep(1)

with open('version1.csv', 'w', encoding='utf8', newline='') as f:
    fc = csv.DictWriter(f, fieldnames=results[0].keys(),)
    fc.writeheader()
    fc.writerows(results)%
