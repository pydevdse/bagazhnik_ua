import requests
from lxml import html
from get_headers import get_headers

def main():
    # url = "https://bagazhnik.ua/bagazhnik-na-kryshu.html"
    url = "https://bagazhnik.ua/bagazhnik-na-kryshu/alfa-romeo/156.html"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    # headers = get_headers("headers_acura.txt")
    response = requests.get(url, headers)
    print(response)
#    print(response.text)

    tree = html.fromstring(response.content)
    # a class="trunk-selection-link" href=
    mods = tree.xpath('//li[@class="trunk-selection-item"]/a/@href')
    mods = [model for model in mods if "156" in model]
    print(mods)
    print(len(mods))


if __name__ == '__main__':
    main()