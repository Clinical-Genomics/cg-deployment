FROM python:3.8-slim

LABEL base_image="python:3.8-slim"
LABEL about.tags="Deployment API"


ENV GUNICORN_WORKERS=1
ENV GUNICORN_THREADS=1
ENV GUNICORN_BIND="0.0.0.0:8000"
ENV GUNICORN_TIMEOUT=400

ENV AUTHORIZATION_TOKEN="fqojqfjqnoffnqop2e"
ENV WEBHOOK_TOKEN="fjofj2ofj23o"
ENV TRIGGERS_DIR="/path/to/triggers/dir"
ENV ENVIRONMENTS="stage"

EXPOSE 8000

WORKDIR /home/worker/app
COPY . /home/worker/app

# Install app requirements
RUN pip install -r requirements.txt

# Install app
RUN pip install -e .

CMD gunicorn \
    --workers=$GUNICORN_WORKERS \
    --bind=$GUNICORN_BIND  \
    --threads=$GUNICORN_THREADS \
    --timeout=$GUNICORN_TIMEOUT \
    --proxy-protocol \
    --forwarded-allow-ips="10.0.2.100,127.0.0.1" \
    --log-syslog \
    --access-logfile - \
    --log-level="debug" \
    --worker-class=uvicorn.workers.UvicornWorker \
     cg_deployment:app