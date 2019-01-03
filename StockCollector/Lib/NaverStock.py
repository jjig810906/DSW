'''
daum 포털사이트에서 주식 정보 수집

'''
import requests
from bs4 import BeautifulSoup


g_url_kospi = "http://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page={0}"             # 코스피 주식 종목 정보
g_url_kosdaq = "http://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page={0}"            # 코스닥 주식 종목 정보
g_url_stockinfo = "http://finance.naver.com/item/frgn.nhn?page={0}&code={1}"                   # 주식 상세 가격정보


#주식코드 정보와 주식명 Dict를 만들어 리턴한다. (p_type = kospi or kosdaq)
#m_dic_stock[주식코드] = 주식명
def get_stock_list(p_type):

    m_url = ''
    if p_type == "kospi":
        m_url = g_url_kospi
    else:
        m_url = g_url_kosdaq

    m_page = 1

    while m_page <= 100:
        m_response = requests.get(m_url.format(m_page))
        m_html = m_response.text
        m_soup = BeautifulSoup(m_html, 'html.parser')
        m_a_tag = m_soup.find_all('a', {'class': 'tltle'})
        m_a_len = len(m_a_tag)
        if m_a_len == 0:
            break

        m_dic_stock = {}
        for i in m_a_tag:
            try:
                m_href = i.get("href")
                m_name = i.text
                m_code = ""
                if m_href is not None:
                    if m_href.find('/item/main.nhn?code=') == 0:
                        m_code = m_href.replace('/item/main.nhn?code=', '')
                        m_dic_stock[m_code] = m_name

            except Exception as ex:
                print("-------------------------")
                print(ex)
                print("-------------------------")

        m_page = m_page + 1

    return m_dic_stock

#주식 상세정보 리턴(일별 가격 / 거래량 / 외국인 보유량)
#m_dic_stock[날짜(2018055)] = (종가 / 거래량 / 등락률 / 외국인 비율)
def get_stock_detail_list(p_code, p_early_stop_date):

    m_dic_stock = {}

    # 주식 가격정보 수집
    m_page = 1
    while m_page <= 300:
        m_url = g_url_stockinfo.format(m_page, p_code)
        m_response = requests.get(m_url)
        m_html = m_response.text
        m_soup = BeautifulSoup(m_html, 'html.parser')
        m_tr_tag = m_soup.find_all('tr', {'onmouseover': 'mouseOver(this)', 'onmouseout': 'mouseOut(this)'})

        m_tr_len = len(m_tr_tag)
        if m_tr_len == 0:
            break

        for i in m_tr_tag:
            try:
                m_contents = i.contents
                if m_contents[1].text.strip() == '':
                    m_page = 300
                    break
                else:
                    if int(m_contents[1].text[:4]) < 2000:  # 2000년도 이전 데이터는 제외한다.
                        break
                    elif int(m_contents[1].text.replace('.', '')) < p_early_stop_date:
                        break
                    else:
                        # <class 'list'>: ['', '2018.05.21', '11,000', '', '', '20', '', 7-'', 8-'', 9-'', 10-'+0.18%', 11-'', 12-'', 13-'2,885', 14-'-1,085', 15-'0', 16-'0', 17-'0.00%', 18-'']
                        # <class 'list'>: ['', '2017.04.27', '9,655', '', '0', '', '', '0.00%', '', '3,446', '+35', '0', '0', '0.00%', '']
                        m_att1 = int(m_contents[3].text.replace(',', '').strip())                                                       #종가
                        m_att2 = int(m_contents[9].text.replace(',', '').strip())                                                       #거래량
                        m_att3 = float(m_contents[7].text.replace('%', '').replace('\n', '').replace('\t', '').strip())                 #등락률
                        m_att4 = float(m_contents[17].text.replace(',', '').replace('%', '').strip())                                   #외국인 보유율
                        #m_dic_stock[m_contents[1].text.replace('.', '')] = '{0} {1} {2} {3}'.format(m_att1, m_att2, m_att3, m_att4)

                        m_key = m_contents[1].text.replace('.', '')
                        m_att = [m_att1, m_att2, m_att3, m_att4]
                        m_dic_stock[m_key] = m_att

                        #print(m_contents[1].text + " = " + m_dic_stock[m_contents[1].text.replace('.', '')])

            except Exception as ex:
                print("-------------------------")
                print(ex)
                print("-------------------------")

        m_page = m_page + 1


    return m_dic_stock


