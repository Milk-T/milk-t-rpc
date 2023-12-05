FROM python:3.9-bullseye

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    supervisor \
    && rm -rf /var/lib/apt/lists/* \
    && pip install vnpy vnpy_rpcservice \
    && pip install git+https://github.com/Milk-T/vnpy_webtrader.git \
    && pip install git+https://github.com/Milk-T/vnpy_algotrading.git

# Copy supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set work directory and copy app contents
WORKDIR /app
COPY . /app

# Volume and port configuration
VOLUME ["/root/.vntrader"]
EXPOSE 8000

# Set the default command to run when starting the container
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
