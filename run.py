import sys
import logging

import vnpy.trader.ui  # noqa
from vnpy_ctp import CtpGateway
from vnpy.event import EventEngine, Event
from vnpy.trader.engine import MainEngine
from vnpy.trader.event import EVENT_LOG
from vnpy_rpcservice.rpc_service.engine import EVENT_RPC_LOG
from vnpy_webtrader import WebEngine
from vnpy_algotrading import AlgoTradingApp


logger = logging.getLogger("Milk-T-RPC")
logger.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)


def process_log_event(event: Event):
    """"""
    log = event.data
    logger.info("Log event:%s\t%s", log.time, log.msg)


def main():
    """Start VN Trader"""
    event_engine = EventEngine()
    event_engine.register(EVENT_LOG, process_log_event)
    event_engine.register(EVENT_RPC_LOG, process_log_event)

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
