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
            self.df = pd.read_excel("bagazhnik.xlsx")
        except:
            self.df = pd.DataFrame(columns=["bagzhnk_name", "bagzhnk_url", "brand", "model", "model_mod", "model_mod_url",
                                            "model_url", "status"])

    def process_item(self, item, spider):
        bgzhnk = item['name']
        # itm = self.df[(self.df['bagzhnk_url'] == bgzhnk.get('bagzhnk_url')) &
        #               (self.df['model_mod'] == bgzhnk.get('model_mod'))]
        # if len(itm.index)>0:
        #     return f"{bgzhnk.get('bagzhnk_name')} already exists in XLSX"
        self.df = pd.concat([self.df, pd.DataFrame.from_records([bgzhnk])])
        self.df = self.df.drop_duplicates()
        if len(self.df.index) % 500 == 0:
            self.df.to_excel("bagazhnik.xlsx", index=False)
        return f"Counts in XLSX: {len(self.df.index)}"
