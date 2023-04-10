FROM python:3.10-buster

# install nginx posgtes and gdal
RUN apt-get update -y && apt-get upgrade -y && apt-get install nginx vim \
    postgresql-common libpq-dev python3-gdal rabbitmq-server -y
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY nginx.default /etc/nginx/sites-available/default
# copy source and install dependencies

RUN mkdir -p /opt/app
COPY requirements.txt start-server.sh /opt/app/
RUN pip install -U pip \
    && pip install -r /opt/app/requirements.txt --no-cache-dir \
    && pip install gunicorn --no-cache-dir
COPY . /opt/app
WORKDIR /opt/app
RUN mkdir -p /opt/app/media && /opt/app/to_ingest
RUN python fetch_data.py
RUN mv /opt/app/to_ingest /opt/app/media/tei_out && ls /opt/app/media/tei_out
# start server
EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]