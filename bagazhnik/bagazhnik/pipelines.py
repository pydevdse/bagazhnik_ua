# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class BagazhnikPipeline:
    def __init__(self):
        try:
            self.df = pd.read_excel("bugazhnik.xlsx")
        except:
            self.df = pd.DataFrame(columns=["bagzhnk_name", "bagzhnk_url", "brand", "model", "model_mod", "model_mod_url",
                                            "model_url", "status"])

    def process_item(self, item, spider):
        bgzhnk = item['name']
        self.df = pd.concat([self.df, pd.DataFrame.from_records([bgzhnk])])
        self.df.to_excel("bgzhs.xlsx", index=False)
        return item
