FROM python:3.6


ADD . /opt/code
WORKDIR /opt/code
ADD . /opt/code
WORKDIR /opt/code
RUN apt-get update && apt-get install make
RUN pip install -r dependencies/dev.txt
RUN pip install -e .[develop]
CMD ["python", "setup.py", "test"]
