FROM python:3.8-slim-buster
ENV HASURA_URL=
ENV SECRET_KEY=
ENV API_KEY=
ENV BOT_TOKEN=
ENV WEBHOOK_URL=
WORKDIR /python-docker
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "app.py"]
