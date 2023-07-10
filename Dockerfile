FROM python:3.8.14-slim-bullseye

WORKDIR /opt/src

COPY requirements.txt .
RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]