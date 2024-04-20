FROM python:3.10

RUN apt-get update && \
    apt-get install -y build-essential wget cron vim

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    wget -O config.guess 'http://git.savannah.gnu.org/cgit/config.git/plain/config.guess' && \
    wget -O config.sub 'http://git.savannah.gnu.org/cgit/config.git/plain/config.sub' && \
    ./configure --prefix=/usr && \
    make && \
    make install

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /work
