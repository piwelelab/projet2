FROM debian:latest

ADD files/ * ./

RUN apt update && apt install python3-pip -y && pip install -r requirements.txt

EXPOSE 8000

CMD uvicorn main:api --host 0.0.0.0 
