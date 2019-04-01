# -*- coding:utf-8 -*-


from douban.items import DoubanItem
from .sql import Sql


class DoubanPipeline(object):

    # def process_item(self, item, spider):
    #     # pass
    #     serial_number = item['serial_number']
    #     evaluate = item['evaluate']
    #     introduce = item['introduce']
    #     movie_name = item['movie_name']
    #     m_describe = item['m_describe']
    #     star = item['star']
    #
    #     Sql.insert_dd_name(serial_number, movie_name, introduce, star, evaluate, m_describe)


    def process_item(self, item, spider):
        Sql.insert_dd_name(item)

