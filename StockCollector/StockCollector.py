'''
naver 웹사이트에서 주식가격정보를 읽어온다.

'''
import time
from .Lib.NaverStock import NaverStock
from Data.ElasticData import ElasticData

class StockCollector:
    def __init__(self, p_logger):
        self.logger = p_logger
        self.sleep = 60 * 60 * 12  #12시간

    def work_collect(self):
        '''
        KOSPI, KOSDAQ 주식 정보 수집를 Naver 주식 사이트를 통해 수집하고,
        ElasticSearch 에 저장한다.
        '''

        c_es = ElasticData()
        c_ns = NaverStock()

        self.logger.info('work_collect start')
        m_list_stock_kind = ['kospi', 'kosdaq']
        for i in m_list_stock_kind:
            # 주식 정보 리턴 (주식코드 / 주식명)
            m_dic_stock = c_ns.get_stock_list(i)

            self.logger.info(i + ' search count:' + str(len(m_dic_stock)))

            # 주식 상세정보 리턴 (종가 / 거래량 / 등락률 / 외국인 비율)
            for key, value in m_dic_stock.items():
                # key= 주식코드, value = 주식명
                try:
                    self.logger.info('search start - kind:' + i + ', code:' + key + ', name:' + value)
                    m_dic_detail = c_ns.get_stock_detail_list(key, 0)
                    self.logger.info('insert start - kind:' + i + ', code:' + key + ', name:' + value)
                    c_es.insert_stock_info(i, key, value, m_dic_detail)
                    self.logger.info('insert complete - kind:' + i + ', code:' + key + ', name:' + value + ', count:' + str(len(m_dic_detail)))
                except Exception as ex:
                    self.logger.exception(ex)

        self.logger.info('work_collect end')
        time.sleep(self.sleep)






