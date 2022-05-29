from sklearn.ensemble import GradientBoostingClassifier as XGmodel
import json, sys
import datetime as dt
from backtester import Backtest
from connect import db


terms=[
    'pts_per_shot',
    'opp_pts_per_shot',
    'threes_made',
    'opp_threes_made',
    'def_reb',
    'opp_def_reb', 
    ]

model = XGmodel(random_state=0, learning_rate=0.0025, n_estimators=125)
date_obj=dt.datetime(2022, 2, 14)
params = {
    'league': 'NBA', 'model': model, 'predict_function': model.predict_proba, 
    'refit': True, 'start_date': date_obj, 'terms': terms, 'required_edge': .149,
    'threshold' : .375, 'model_type' : 'classification',
    }

backtest = Backtest(params=params)
for bet in backtest.basketball():

    print(bet, "\n")