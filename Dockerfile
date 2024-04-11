FROM python:3-alpine

RUN apk update && \
    apk add git bash gcc musl-dev linux-headers

WORKDIR /gr
COPY game-redirect.py /gr/
COPY requirements.txt /gr/
RUN cd /gr

RUN python -m pip install --no-cache-dir -r requirements.txt

CMD [ "python", "game-redirect.py" ]