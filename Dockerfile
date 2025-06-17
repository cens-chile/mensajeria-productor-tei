FROM python:3.12-bookworm
RUN pip3 install --upgrade setuptools
# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY docker_conf/nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
# copy source and install dependencies
RUN mkdir -p /code
RUN mkdir -p /code/pip_cache
COPY requirements.txt start-server.sh /code/
COPY . /code/
WORKDIR /code
RUN pip3 install -r requirements.txt
RUN chmod +x start-server.sh

# start server
EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["/code/start-server.sh"]
