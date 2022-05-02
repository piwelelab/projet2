# Dockerfile pour le test obtention des performances des modèles
# ===========================================

FROM ubuntu:20.04
    
RUN apt-get update && apt-get install python3-pip -y && pip3 install pytest requests

ADD test_model_performance.py ./


CMD python3 -m pytest test_model_performance.py > rains_logs/api_test_model_performance.log
