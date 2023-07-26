import requests
from lxml import html

def main():
    url = "https://bagazhnik.ua/bagazhnik-na-kryshu.html"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    response = requests.get(url, headers)
    print(response)

    tree = html.fromstring(response.content)

    brands = tree.xpath('//li[@class="trunk-selection-item"]/a/@href')
    print(brands)
    print(len(brands))


if __name__ == '__main__':
    main()