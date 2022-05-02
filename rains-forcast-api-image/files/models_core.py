# models_core.py
import features as feature_help
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, balanced_accuracy_score, accuracy_score

class Predict:
    @staticmethod
    def load_data(new_data_url: str, old_data_url: str):
        db_old = pd.read_csv(old_data_url).drop(['raintomorrow'], axis=1)
        db_new = pd.read_csv(new_data_url)
        db_old['origin'], db_new['origin'] = 0, 1
        
        columns_name = [col.lower() for col in db_new.columns.tolist()]
        db_new = db_new.rename(columns = dict(zip(db_new.columns.tolist(), columns_name)))
        
        db_new['date'] = pd.to_datetime(db_new.date, format='%Y-%m-%d')
        db_old['date'] = pd.to_datetime(db_old.date, format='%Y-%m-%d')
        return db_old, db_new
    
    @staticmethod
    def preprocess_data(db_old: pd.DataFrame, db_new: pd.DataFrame):
        bimodal_num_vars = ['rainfall', 'cloud3pm', 'cloud9am']
        cat_vars = [name for name in db_old.select_dtypes(include = 'O').columns.tolist() if name not in ['location', 'origin']]
        num_vars = [name for name in db_old.describe().columns.tolist() if name not in bimodal_num_vars]
        
        # Dicitonaire de remplissage des valeurs maquantes par ville et type de variables
        num_vars_fna = pd.DataFrame(db_old.groupby(['location'])[num_vars].agg(pd.Series.mean).to_dict()).T.to_dict()
        bimodal_num_vars_fna = pd.DataFrame(db_old.groupby(['location'])[bimodal_num_vars].agg(pd.Series.mode)).T.to_dict()
        cat_vars_fna = pd.DataFrame(db_old.groupby(['location'])[cat_vars].agg(pd.Series.mode)).T.to_dict()
        
        
        for location in db_new.location.unique():
            db_new.loc[db_new['location'] == location, num_vars] = db_new.groupby(['location']).get_group(location)[num_vars].fillna(num_vars_fna[location])
            db_new.loc[db_new['location'] == location, bimodal_num_vars] = db_new.groupby(['location']).get_group(location)[bimodal_num_vars].fillna(bimodal_num_vars_fna[location])
            db_new.loc[db_new['location'] == location, cat_vars] = db_new.groupby(['location']).get_group(location)[cat_vars].fillna(cat_vars_fna[location])
            
        db = pd.concat([db_old, db_new]).reset_index(drop=True)
        return db
    
    @staticmethod
    def buildFeatures(db: pd.DataFrame):
        cat_df = pd.DataFrame()
        dfs = []
        
        for label in db['windgustdir'].unique():
            cat_df[label] = np.where(db['windgustdir'] == label, 1, 0)
            
        db = pd.concat([db, cat_df], axis=1)

        for location in db.location.unique():
            globals()[f'{location}'] = feature_help.build_timeFeatures(db.groupby(['location']).get_group(location))
            dfs.append(globals()[f'{location}'])
            
        db = pd.concat(dfs).reset_index(drop=True)
        db = pd.concat([db, pd.get_dummies(db['location'])], axis = 1)
        cat_vars = db.select_dtypes(include = 'O').columns.tolist()
        cat_vars.pop(0)
        db = db.drop(cat_vars, axis = 1)
        db = db.drop(['pressure3pm', 'temp9am', 'maxtemp'], axis = 1)
        
        
        _ = cat_df.columns.tolist() + db.location.unique().tolist() + ['origin', 'date', 'location']
        norm_vars = [var for var in db.columns.tolist() if var not in _]

        db[norm_vars] = db[norm_vars].apply(lambda x: (x - x.mean() / x.std()), axis = 1)
        return db
    
    @staticmethod
    def predict(db, model: str = 'v1'):
        lgbm_model = joblib.load('models/lgbm_model.pkl')
        logr_model = joblib.load('models/logr_model.pkl')
        
        db_new = db.loc[db['origin'] == 1].reset_index(drop=True)
        features = [name for name in db_new.columns if name not in ['date', 'location', 'origin']]
        
        db_new['lgbm_model_prediction'] = lgbm_model.predict(db_new[features])
        db_new['logr_model_prediction'] = logr_model.predict(db_new[features].values)
        db_new['date'] = [date.split()[0] for date in db_new['date'].astype(str).tolist()]
        
        if model == 'v1':
            return db_new[['date', 'location', 'logr_model_prediction']].sort_values('logr_model_prediction', ascending=False).to_dict(orient = 'records')
        else:
            return db_new[['date', 'location', 'lgbm_model_prediction']].sort_values('lgbm_model_prediction', ascending=False).to_dict(orient = 'records')
        
    @staticmethod
    def perfomance(x_test_url, y_test_url):
        def compute_scores(model, x_test, y_test):
            preds = model.predict(x_test.values)
            confusion_matrix = pd.crosstab(y_test['raintomorrow'], preds).to_dict()
            accuracy = accuracy_score(y_test, preds)
            balanced_accuracy = balanced_accuracy_score(y_test, preds)
            return confusion_matrix, accuracy, balanced_accuracy
    
        lgbm_model = joblib.load('models/lgbm_model.pkl')
        logr_model = joblib.load('models/logr_model.pkl')

        x_test = pd.read_csv(x_test_url)
        y_test = pd.read_csv(y_test_url)

        confusion_matrix, accuracy, balanced_accuracy = compute_scores(logr_model, x_test, y_test)
        confusion_matrix_, accuracy_, balanced_accuracy_ = compute_scores(lgbm_model, x_test, y_test)

        scores = {
            'Faux Positif': confusion_matrix[1][0],
            'Faux Négatif': confusion_matrix[0][1],
            'Vrai Négatif': confusion_matrix[0][0],
            'Vrai Positif': confusion_matrix[1][1],
            'accuracy': accuracy,
            'balanced_accuracy': balanced_accuracy
        }
        scores_ = {
            'Faux Positif': confusion_matrix_[1][0],
            'Faux Négatif': confusion_matrix_[0][1],
            'Vrai Négatif': confusion_matrix_[0][0],
            'Vrai Positif': confusion_matrix_[1][1],
            'accuracy': accuracy_,
            'balanced_accuracy': balanced_accuracy_
        }

        score_final = {
            'Logistic Regression (v1)': scores,
            'Ligth Gradient Boosting (v2)': scores_
        }
        return score_final
