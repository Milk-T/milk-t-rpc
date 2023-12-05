import sys
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import vnpy.trader.ui  # noqa
from vnpy_ctp import CtpGateway
from vnpy.event import EventEngine, Event
from vnpy.trader.engine import MainEngine
from vnpy_webtrader import WebEngine
from vnpy_algotrading import AlgoTradingApp


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

CTP_SETTING_FILENAME = "connect_ctp.json"
ctp_connection_setting: dict = load_json(get_file_path(CTP_SETTING_FILENAME))


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


def main():
    """Start VN Trader"""
    event_engine = EventEngine()
    event_engine.register_general(process_log_event)

    main_engine = MainEngine(event_engine)

    main_engine.add_gateway(CtpGateway)
    main_engine.add_app(AlgoTradingApp)

    main_engine.connect(ctp_connection_setting, "CTP")

    web_engine = WebEngine(main_engine, event_engine)

    logger.info("Start server:%s", REQ_ADDRESS)
    web_engine.start_server(REQ_ADDRESS, SUB_ADDRESS)


if __name__ == "__main__":
    main()
