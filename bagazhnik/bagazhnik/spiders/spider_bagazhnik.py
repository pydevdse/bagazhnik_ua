import logging
from ..items import BagazhnikItem
import scrapy


class SpiderBagazhnik(scrapy.Spider):
    name = "bagazhnik"
    start_urls = ["https://bagazhnik.ua/bagazhnik-na-kryshu.html"]

    def parse(self, response):
        brands_urls = response.xpath('//li[@class="trunk-selection-item"]/a/@href').extract()
        brands_names = response.xpath('//span[@class="trunk-selection-name"]/text()').extract()
        print(f"Urls brands count: {len(brands_urls)}")
        print(f"Names brands count: {len(brands_names)}")
        for ind, brand_url in enumerate(brands_urls):
            yield scrapy.Request(brand_url, callback=self.pares_models, cb_kwargs={'brand': brands_names[ind]})

    def pares_models(self, response, brand):
        urls = response.xpath('//li[@class="trunk-selection-item"]')
        models = []
        for url in urls:
            model_name = url.xpath('.//span[@class="trunk-selection-name"]/text()').extract_first()
            url_model = url.xpath('.//a/@href').extract_first()
            if url_model == response.url: continue
            if response.url.split("/")[-1].split(".")[0] in url_model:
                model = {"brand":brand, "model": model_name, "model_url": url_model}
                models.append(model)
                yield scrapy.Request(url_model, callback=self.parse_mosel_mod, cb_kwargs={"model":model})

    def parse_mosel_mod(self, response, model):
        urls = response.xpath('//li[@class="trunk-selection-item"]')
        model_mods = []
        for url in urls:
            model_mod_name = url.xpath('.//span[@class="trunk-selection-name"]/text()').extract_first()
            url_model_mod = url.xpath('.//a/@href').extract_first()
            if url_model_mod == response.url: continue
            if response.url.split("/")[-1].split(".")[0] in url_model_mod:
                model.update({"model_mod": model_mod_name, "model_mod_url":url_model_mod})
                model_mods.append(model)
                yield scrapy.Request(url_model_mod, callback=self.parse_bagazhnik, cb_kwargs={"model":model})

    def parse_bagazhnik(self, response, model):
        all_items_url = response.xpath('//div[@class="product-item more-link"]/a/@href').extract_first()
        if all_items_url:
            yield scrapy.Request(all_items_url, callback=self.parse_bagazhnik, cb_kwargs={"model":model})
        bgzhnks = response.xpath('//div[@class="catalog-section portal-level section"]')
        if len(bgzhnks)>0:
            active = bgzhnks[0].xpath('.//div[@class="product-item"]/div[@class="product-img"]')
            disable = bgzhnks[0].xpath('.//div[@class="product-item disabled"]/div[@class="product-img"]')
        else:
            active = response.xpath('.//div[@class="product-item"]/div[@class="product-img"]')
            disable = response.xpath('.//div[@class="product-item disabled"]/div[@class="product-img"]')
        logging.info(f"Mod: {model.get('model_mod')} active count: {len(active)}")
        logging.info(f"Mod: {model.get('model_mod')} disable count: {len(disable)}")
        for act in active:
            mod = model.copy()
            bagzhnk_url = act.xpath('.//a/@href').extract_first()
            if "boksy-i-korziny" in bagzhnk_url:
                continue
            bagzhnk_name = act.xpath('.//a/img/@alt').extract_first()
            mod.update({"bagzhnk_name":bagzhnk_name, "bagzhnk_url":bagzhnk_url, "status":"active"})
            item = BagazhnikItem()
            item['name'] = mod
            yield item

        for dis in disable:
            mod = model.copy()
            bagzhnk_url = dis.xpath('.//a/@href').extract_first()
            bagzhnk_name = dis.xpath('.//a/img/@alt').extract_first()
            mod.update({"bagzhnk_name": bagzhnk_name, "bagzhnk_url": bagzhnk_url, "status": "disabled"})
            item = BagazhnikItem()
            item['name'] = mod
            yield item
