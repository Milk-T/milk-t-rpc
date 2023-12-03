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

    setting = {
        "用户名": "60111805",
        "密码": "123321",
        "经纪商代码": "4300",
        "交易服务器": "61.183.150.151:41205",
        "行情服务器": "61.183.150.151:41213",
        "产品名称": "rainmaker_coffee_1.0",
        "授权编码": "5S58RS2AS24WJNQ2",
        "产品信息": "",
    }
    main_engine.connect(setting, "CTP")

    web_engine = WebEngine(main_engine, event_engine)
    req_address = "tcp://127.0.0.1:2014"
    sub_address = "tcp://127.0.0.1:4102"
    logger.info("Start server:%s", req_address)
    web_engine.start_server(req_address, sub_address)


if __name__ == "__main__":
    main()
