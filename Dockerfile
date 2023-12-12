#######
# Python dependencies builder
#
FROM python:3.9-slim as builder

WORKDIR /opt/code

COPY ./dependencies/dev.txt /opt/code/dependencies/dev.txt
COPY ./dependencies/install.txt /opt/code/dependencies/install.txt
COPY ./dependencies/test.txt /opt/code/dependencies/test.txt
COPY ./setup.py /opt/code/setup.py
COPY ./VERSION /opt/code/VERSION
COPY ./README.rst /opt/code/README.rst

RUN apt-get update && \
    apt-get install -y --no-install-recommends make \
    git \
    build-essential

RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -e .[develop] && \
    pip install -r dependencies/dev.txt

########
# Python app specific config
#
FROM python:3.9-slim as app

WORKDIR /opt/code

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHON_VERSION=3.9.1 \
    PYTHON_PIP_VERSION=21.0.1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ADD . /opt/code/

EXPOSE 8080

CMD ["python", "setup.py", "test"]