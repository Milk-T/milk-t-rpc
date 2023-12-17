import os
import sys
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import vnpy_crypto
vnpy_crypto.init()

from vnpy_ctp import CtpGateway
from vnpy_binance import (
    BinanceSpotGateway,
    BinanceUsdtGateway,
    BinanceInverseGateway
)
from vnpy.event import EventEngine, Event
from vnpy.trader.engine import MainEngine
from vnpy_webtrader import WebEngine
from vnpy_algotrading import AlgoTradingApp
from vnpy.trader.utility import get_file_path, load_json


logger = logging.getLogger("Milk-T-RPC")
logger.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

# Web服务运行配置
APP_SETTING_FILENAME = "web_trader_setting.json"
app_setting: dict = load_json(get_file_path(APP_SETTING_FILENAME))
REQ_ADDRESS = app_setting["req_address"]  # 请求服务地址
SUB_ADDRESS = app_setting["sub_address"]  # 订阅服务地址


def to_dict(o: dataclass) -> dict:
    """将对象转换为字典"""
    data: dict = {}
    for k, v in o.__dict__.items():
        if isinstance(v, Enum):
            data[k] = v.value
        elif isinstance(v, datetime):
            data[k] = str(v)
        else:
            data[k] = v
    return data


def process_log_event(event: Event):
    """"""
    logger.info("event=%s", to_dict(event))


def connect_gateway(main_engine,gateway_class, setting_filename):
    setting = load_json(get_file_path(setting_filename))
    main_engine.add_gateway(gateway_class)
    main_engine.connect(setting, gateway_class.default_name)


def main():
    """Start VN Trader"""
    event_engine = EventEngine()
    event_engine.register_general(process_log_event)

    main_engine = MainEngine(event_engine)

    if os.path.exists(get_file_path("connect_ctp.json")):
        connect_gateway(main_engine, CtpGateway, "connect_ctp.json")
        logger.info("connect ctp")

    if os.path.exists(get_file_path("connect_binance.json")):
        connect_gateway(main_engine, BinanceSpotGateway, "connect_binance.json")
        connect_gateway(main_engine, BinanceUsdtGateway, "connect_binance.json")
        connect_gateway(main_engine, BinanceInverseGateway, "connect_binance.json")
        logger.info("connect binance")

    main_engine.add_app(AlgoTradingApp)

    logger.info("Start server:%s", REQ_ADDRESS)
    web_engine = WebEngine(main_engine, event_engine)
    web_engine.start_server(REQ_ADDRESS, SUB_ADDRESS)


if __name__ == "__main__":
    main()
