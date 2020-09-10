FROM python:3.6.9-alpine

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache netcat-openbsd curl

RUN mkdir /lib64 && ln -s /lib/libc.musl-x86_64.so.1 /lib64/ld-linux-x86-64.so.2

WORKDIR /code

COPY requirements.txt .
RUN apk add --no-cache postgresql-libs
RUN \
 apk add --no-cache --virtual .build-deps gcc g++ libstdc++ musl-dev postgresql-dev libffi-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . /code

HEALTHCHECK --interval=5s --timeout=3s \
    CMD curl --fail http://0.0.0.0:8000/health || exit 1

CMD /code/run.sh
