import requests
import pytest
from time import sleep

url = 'https://storage.googleapis.com/datascientest-projet2-storage/rains_new_partition.csv'

@pytest.mark.parametrize('data_url, model', [(url, 'v1'), (url, 'v2')])
def test_post_predict(data_url: str, model: str):
    api_address = 'rains-forcast-api'
    api_port = 8000
    json = {
        'data_url': data_url,
        'model': model
    }
    sleep(5)
    r = requests.post(f'http://{api_address}:{api_port}/predict', json = json)

    assert r.status_code == 200

    if model == 'v1':
        assert 'logr_model_prediction' in r.json()[0].keys()
    else:
        assert 'lgbm_model_prediction' in r.json()[0].keys()
