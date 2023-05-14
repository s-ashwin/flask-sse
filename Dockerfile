FROM python

COPY . /sse
WORKDIR /sse/

RUN pip3 install -r requirements.txt
EXPOSE 3000
CMD python3 server.py