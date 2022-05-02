# Rains api # Test model performance # test_model_performance.py

import requests
import pytest
from time import sleep

test_url = 'https://storage.googleapis.com/datascientest-projet2-storage/x_test_partition.csv'
label_url = 'https://storage.googleapis.com/datascientest-projet2-storage/y_test_partition.csv'

@pytest.mark.parametrize('test_url, label_url', [(test_url, label_url)])
def test_post_performance(test_url: str, label_url: str):
    api_address = 'rains-forcast-api'
    api_port = 8000
    json = {
        'test_url': test_url,
        'label_url': label_url
    }
    sleep(5)
    r = requests.post(f'http://{api_address}:{api_port}/performance', json = json)
    assert r.status_code == 200
    assert ['Logistic Regression (v1)', 'Ligth Gradient Boosting (v2)'] == list(r.json().keys())
    
    
