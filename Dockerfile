# --- First Stage: Python/uWSGI setup ---

FROM python:3.10.2-slim-buster as builder

COPY . /srv/flask_app
WORKDIR /srv/flask_app

# Only update and clean up, no need to install build tools
RUN apt-get clean \
    && apt-get -y update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt --src /usr/local/src
RUN pip install -Iv uWSGI==2.0.17.1 --src /usr/local/src

# --- Second Stage: Nginx setup ---

FROM nginx:stable

# Copy uWSGI app from the previous stage
COPY --from=builder /srv/flask_app /srv/flask_app

# Copy the Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Specify intended port
EXPOSE 80

# Start command
WORKDIR /srv/flask_app
RUN chmod +x ./start.sh
CMD ["./start.sh"]
