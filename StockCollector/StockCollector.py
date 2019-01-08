'''
daum 웹사이트에서 주식가격정보를 읽어온다.

'''

from .Lib import NaverStock
from Data.ElasticData import ElasticSearchData


def work_collect():

    '''
    KOSPI 주식 정보 수집를 Naver 주식 사이트를 통해 수집하고,
    ElasticSearch 에 저장한다.
    '''

    m_list_stock_kind = ['kospi', 'kosdaq']
    for i in m_list_stock_kind:
        # 주식 정보 리턴 (주식코드 / 주식명)
        m_dic_stock = NaverStock.get_stock_list(i)

        # 주식 상세정보 리턴 (종가 / 거래량 / 등락률 / 외국인 비율)
        for key, value in m_dic_stock.items():
            # key= 주식코드, value = 주식명
            m_dic_detail = NaverStock.get_stock_detail_list(key, 0)

            es = ElasticSearchData()
            es.insert_stock_info(i, key, m_dic_detail)








