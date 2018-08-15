FROM python:3.6-alpine

# Allows you to add additional packages via build-arg
ARG ADDITIONAL_PACKAGE
ARG WATCHDOG_DL_URL=https://github.com/openfaas-incubator/of-watchdog/releases/download/0.2.6/of-watchdog

# Alternatively use ADD https:// (which will not be cached by Docker builder)
RUN apk --no-cache add curl ${ADDITIONAL_PACKAGE} \
    && echo "Pulling watchdog binary from Github." \
    && curl -sSLf ${WATCHDOG_DL_URL} > /usr/bin/fwatchdog \
    && chmod +x /usr/bin/fwatchdog \
    && apk del curl --no-cache

RUN apk --no-cache add musl-dev gcc make

WORKDIR /root/

COPY requirements.txt   .
RUN pip install -r requirements.txt
COPY index.py           .

RUN mkdir -p function
RUN touch ./function/__init__.py
WORKDIR /root/function/
COPY function/requirements.txt	.
RUN pip install -r requirements.txt

WORKDIR /root/
COPY function           function

ENV fprocess="python index.py"

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"


HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
