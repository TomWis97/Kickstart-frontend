FROM alpine
RUN apk update && \
    apk add python3 uwsgi-python3 uwsgi-cgi uwsgi nginx
COPY conf/nginx.conf /etc/nginx/nginx.conf
COPY conf/uwsgi_config.ini /etc/uwsgi_config.ini
COPY src/www /var/www/
COPY src/cgi-bin /usr/lib/cgi-bin
COPY src/data /data
# Fixing permissions
RUN chown -R nginx:nginx /var/www && \
    rm -rf /var/www/localhost
# Creating testing database.
COPY src/tests.py /usr/lib/cgi-bin/tests.py
RUN cd /usr/lib/cgi-bin && python3 tests.py && rm tests.py
EXPOSE 80
CMD /usr/sbin/uwsgi /etc/uwsgi_config.ini & /usr/sbin/nginx -c /etc/nginx/nginx.conf
