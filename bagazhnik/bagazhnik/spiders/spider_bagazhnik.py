import logging

import scrapy


class SpiderBagazhnik(scrapy.Spider):
    name = "bagazhnik"
    start_urls = ["https://bagazhnik.ua/bagazhnik-na-kryshu.html"]

    def parse(self, response):
        brands_urls = response.xpath('//li[@class="trunk-selection-item"]/a/@href').extract()
        brands_names = response.xpath('//span[@class="trunk-selection-name"]/text()').extract()
        # print(brands_urls)
        print(f"Urls brands count: {len(brands_urls)}")
        #print(brands_names)
        print(f"Names brands count: {len(brands_names)}")
        for ind, brand_url in enumerate(brands_urls):
            yield scrapy.Request(brand_url, callback=self.pares_models, cb_kwargs={'brand': brands_names[ind]})

    def pares_models(self, response, brand):
        urls = response.xpath('//li[@class="trunk-selection-item"]') #.extract()
        models = []
        for url in urls:
            model_name = url.xpath('.//span[@class="trunk-selection-name"]/text()').extract_first()
            url_model = url.xpath('.//a/@href').extract_first()
            if response.url.split("/")[-1].split(".")[0] in url_model:
                models.append({"brand":brand, "model": model_name, "url": url_model})

        if len(models)>1:
            models=models[1:]
        #print(f"Brand: {brand}  models: {models}")
        yield {brand:models}
        # for model in models_names: