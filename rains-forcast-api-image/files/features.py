# features.py
import numpy as np
import pandas as pd



day = 24*60*60
month = 30*day
year = (365.2425)*day

def build_timeFeatures(db):
    db = db.sort_values('date')
    timestamp_s = db.date.map(pd.Timestamp.timestamp)
    
    db['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))

    db['Month cos'] = np.cos(timestamp_s * (2 * np.pi / month))
    db['Month sin'] = np.sin(timestamp_s * (2 * np.pi / month))

    db['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
    db['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))
    
    return db

