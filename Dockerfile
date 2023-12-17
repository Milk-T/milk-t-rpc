FROM python:3.9-bullseye

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /app
COPY . /app

RUN sed -i "s|http://deb.debian.org/debian|http://mirror.sjtu.edu.cn/debian|g" /etc/apt/sources.list \
    &&  apt-get update && apt-get install -y \
    ca-certificates \
    apt-transport-https \
    curl \
    wget \
    git \
    supervisor \
    locales \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib/ \
    && ./configure --prefix=/usr \
    && make \
    && make install \
    && cd .. \
    && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz \
    && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen \
    && sed -i '/zh_CN.GB18030/s/^# //g' /etc/locale.gen \
    && locale-gen

RUN pip config set global.index-url https://mirror.sjtu.edu.cn/pypi/web/simple \
    && pip install vnpy vnpy_rpcservice vnpy_ctp vnpy_rest vnpy_crypto vnpy_websocket vnpy_binance \
    && pip install git+https://github.com/Milk-T/vnpy_webtrader.git \
    && pip install git+https://github.com/Milk-T/vnpy_algotrading.git \
    && mkdir -p /app/logs

VOLUME ["/root/.vntrader"]
EXPOSE 8000

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
