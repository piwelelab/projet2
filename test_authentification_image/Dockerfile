# Dockerfile pour le test d'authentification
# ===========================================

FROM debian:latest
    
RUN apt-get update && apt-get install python3-pip -y && pip3 install pytest requests

ADD test_authentification.py ./


CMD python3 -m pytest test_authentification.py > rains_logs/api_test_authentification.log
