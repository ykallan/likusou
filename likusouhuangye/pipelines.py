# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

pymysql.install_as_MySQLdb()


class LikusouhuangyePipeline(object):

    def __init__(self):
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            database='scrapy',
            user='root',
            passwd='root',
            charset='utf8',
        )

        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 写入spider传过来的具体数值
        # self.writer.writerow(item)
        # 写入完返回

        self.cursor.execute('''INSERT INTO likusou(quancheng, zhucediqu, lianxiren, dianhua, shouji, country_name, address) VALUES(%s, %s, %s, %s, %s, %s, %s)''',
                            (item['quancheng'], item['zhucediqu'], item['lianxiren'], item['dianhua'], item['shouji'], item['country_name'], item['address']))
        self.conn.commit()

        # item['quancheng'] = quancheng
        # item['zhucediqu'] = zhucediqu
        # item['lianxiren'] = lianxiren
        # item['dianhua'] = dianhua
        # item['shouji'] = shouji
        # item['country_name'] = country_name
        # item['address'] = address

    def close(self, spider):
        self.cursor.close()
        self.conn.close()
