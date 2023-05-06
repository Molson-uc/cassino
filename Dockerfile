FROM python:3.10.0-slim
COPY . /app
WORKDIR /app
RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install -r requirements.txt

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt

WORKDIR /app/api
CMD /opt/venv/bin/gunicorn api.wsgi:application --bind "0.0.0.0:8000"
