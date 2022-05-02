from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import base64, requests
from typing import Optional
from pydantic import BaseModel
from models_core import *


api = FastAPI(
    title="Rains Forcast",
    description="Predict rains in Australia cities",
    version="1.0.0"
)

security = HTTPBasic()
model = Predict()

users = {
  "alice": {
      "username": "alice",
      "hashed_password": base64.encodebytes(b"wonderland")
  },
    
 "bob": {
      "username": "bob",
      "hashed_password": base64.encodebytes(b"builder")
  },
    
 "clementine": {
     "username": "clementine",
      "hashed_password": base64.encodebytes(b"mandarine")
  },
    
 "admin": {
     "username": "admin",
     "hashed_password": base64.encodebytes(b"4dm1N")
  }
}

class Makepred(BaseModel):
    """
    Url du fichier .csv contenant les données 
    Choix du modèle de prédiction
    """
    data_url = 'https://storage.googleapis.com/datascientest-projet2-storage/rains_new_partition.csv'
    
    data_url: Optional[str] = data_url
    model: Optional[str] = 'v1'
        
class Testdata(BaseModel):
    """
    x_test_url: Url du fichier .csv de la partition de de test
    y_test_url: Url du fichier .csv contenant les labels de la partiton de test 
    """
    test_url = 'https://storage.googleapis.com/datascientest-projet2-storage/x_test_partition.csv'
    label_url = 'https://storage.googleapis.com/datascientest-projet2-storage/y_test_partition.csv'
    
    test_url: Optional[str] = test_url
    label_url: Optional[str] = label_url
        

async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not(users.get(username)) or not(base64.encodebytes(credentials.password.encode()) == users[username]['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@api.get("/authentification")
async def current_user(username: str = Depends(get_current_user)):
    result = {
            'status' : 'success',
            'message' : (f"Hello {username} ! Welcome to Australia Rains Forcast API.")
        }
    return result

@api.post('/predict')
async def make_predictions(params: Makepred):
    """
    Effectuer des prédictions sur de nouvelles données en provenance d'un fichier .csv
    """
    new_data_url = params.data_url
    old_data_url = 'https://storage.googleapis.com/datascientest-projet2-storage/rains_old_partition.csv'
    
    db_old, db_new = model.load_data(new_data_url, old_data_url)
    db = model.preprocess_data(db_old, db_new)
    db = model.buildFeatures(db)
    output = model.predict(db, model = params.model)
    return output

@api.post('/performance')
async def get_model_performance(params: Testdata):
    x_test_url = params.test_url
    y_test_url = params.label_url
    return model.perfomance(x_test_url, y_test_url)
