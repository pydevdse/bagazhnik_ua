import scrapy


class SpiderBagazhnik(scrapy.Spider):
    name = "bagazhnik"
    start_urls = ["https://bagazhnik.ua/bagazhnik-na-kryshu.html"]

    def parse(self, response):
        brands_urls = response.xpath('//li[@class="trunk-selection-item"]/a/@href').extract()
        brands_names = response.xpath('//span[@class="trunk-selection-name"]/text()').extract()
        # print(brands_urls)
        print(len(brands_urls))
        print(brands_names)
        print(len(brands_names))
        for ind, brand_url in enumerate(brands_urls):
            yield scrapy.Request(brand_url, callback=self.pares_models, cb_kwargs={'brand': brands_names[ind]})

    def pares_models(self, response, brand):
        models = response.xpath('//li[@class="trunk-selection-item"]/a/@href').extract()
        print(f"Brand: {brand}  models: {models}")
        print(f"Brand {brand} models count: {len(models)}")