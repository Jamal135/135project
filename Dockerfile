FROM python:3.10.2-slim-buster

RUN adduser --disabled-password --gecos '' --shell /usr/sbin/nologin user

WORKDIR /srv/flask_app

COPY . .

RUN apt-get update && apt-get install -y \
    nginx \
    python3-dev \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install -Iv uWSGI==2.0.21

RUN apt-get remove -y python3-dev build-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY nginx.conf /etc/nginx
RUN chown -R user:user /usr/share/nginx/html
RUN chown -R user:user /tmp

RUN chmod +x ./start.sh \
    && chown -R user:user /srv/flask_app

EXPOSE 80

RUN chown -R user:user /srv/flask_app

USER user

CMD ["./start.sh"]