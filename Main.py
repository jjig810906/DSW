# -*- coding: utf-8 -*-
'''
주식 정보 수집

'''
import logging
import time
from logging.handlers import RotatingFileHandler
from StockCollector.StockCollector import StockCollector

def get_logger(p_logger_name):
    m_log_path = '/dsw/Log/' + p_logger_name + '.log'
    m_logger = logging.getLogger(p_logger_name)
    m_file_handler = RotatingFileHandler(m_log_path, maxBytes=1024 * 1024 * 1, backupCount=2)
    m_file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)s] >> %(message)s'))
    m_logger.addHandler(m_file_handler)
    m_logger.setLevel(logging.DEBUG)

    return m_logger

def dowork():
    m_logger = get_logger('StockCollector')
    m_logger.debug("start StockCollector")
    c_sc = StockCollector(m_logger)
    while True:
        try:
            c_sc.work_collect()
        except Exception as ex:
            m_logger.exception(ex)
        time.sleep(10)




dowork()




