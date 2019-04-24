FROM python:2.7-slim
ADD . /opt/code
WORKDIR /opt/code
RUN apt-get update && apt-get install make
RUN pip install -r dependencies/dev.txt
CMD [ "python", "setup.py", "test"]
