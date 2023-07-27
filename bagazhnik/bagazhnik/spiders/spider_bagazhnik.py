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
            if url_model == response.url: continue
            if response.url.split("/")[-1].split(".")[0] in url_model:
                model = {"brand":brand, "model": model_name, "url": url_model}
                models.append(model)
                yield scrapy.Request(url_model, callback=self.parse_mosel_mod, cb_kwargs={"model":model})

        #print(f"Brand: {brand}  models: {models}")
        # yield {brand:models}

    def parse_mosel_mod(self, response, model):
        urls = response.xpath('//li[@class="trunk-selection-item"]')
        model_mods = []
        for url in urls:
            model_mod_name = url.xpath('.//span[@class="trunk-selection-name"]/text()').extract_first()
            url_model_mod = url.xpath('.//a/@href').extract_first()
            # print(model_mod_name, url_model_mod)
            if url_model_mod == response.url: continue
            if response.url.split("/")[-1].split(".")[0] in url_model_mod:
                model.update({"model_mod": model_mod_name, "url_mod": url_model_mod})
                model_mods.append(model)
                yield model