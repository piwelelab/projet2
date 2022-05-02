# Dockerfile pour les tests de prediction des modèles
# ===========================================

FROM ubuntu:20.04
    
RUN apt-get update && apt-get install python3-pip -y && pip3 install pytest requests

ADD test_model_prediction.py ./


CMD python3 -m pytest test_model_prediction.py > rains_logs/api_test_model_prediction.log
