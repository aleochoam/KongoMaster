FROM alpine:edge

RUN apk update \
&& apk add --no-cache \
  ca-certificates \
  ffmpeg \
  opus \
  python3 \

# Install build dependencies
&& apk add --no-cache --virtual .build-deps \
  gcc \
  git \
  libffi-dev \
  libsodium-dev \
  make \
  musl-dev \
  python3-dev

WORKDIR /app

ADD src /app
ADD requirements.txt /app/

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python3", "bot.py"]
