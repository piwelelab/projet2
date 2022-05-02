# Rains api # Test Authentification # athentification_test.py
import base64
import requests
import pytest
from time import sleep

@pytest.mark.parametrize("login", [('alice:wonderland'), ('bob:builder'), ('clementine:mandarine')])
def test_get_athentification(login: str):
    api_address = 'rains-forcast-api'
    api_port = 8000
    login = base64.encodebytes('{}'.format(login).encode()).decode().strip()
    sleep(5)
    r = requests.get(f'http://{api_address}:{api_port}/authentification', headers={'Authorization': f'Basic {login}'})
    #sleep(10)
    assert r.status_code == 200
