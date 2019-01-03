# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import datetime
import Config.SystemConfig as sc

class ElasticSearchData:
    def __init__(self):
        self.es = Elasticsearch([sc.server_info["elasticsearch_ip"]], port=int(sc.server_info["elasticsearch_port"]))

    #주식 데이터 저장
    def insert_stock_info(self, p_stock_code, p_stock_dioc):

        m_loop_len = len(p_stock_dioc)
        m_loop_cnt = 0

        m_datas = []
        for x in p_stock_dioc:
            m_data = {
                "_index": "stock",
                "_type": "stock_info",
                "_id": p_stock_code + '_' + x,
                "_source": {
                    "code": p_stock_code,
                    "date": x,
                    "price": p_stock_dioc[x][0],
                    "volume": p_stock_dioc[x][1],
                    "price_percent": p_stock_dioc[x][2],
                    "foreigner_percent": p_stock_dioc[x][3]
                }
            }
            m_datas.append(m_data)
            print(p_stock_code + '_' + x)
            m_loop_cnt = m_loop_cnt + 1
            if (m_loop_cnt % 20) == 0 or m_loop_cnt == m_loop_len:
                helpers.bulk(self.es, m_datas)
                m_datas.clear()

