import numpy as np
import datetime as dt


def get_implied_probability(money_line):
    """takes American formated odds and returns the implied probability"""
    return np.abs(money_line) / (np.abs(money_line) + 100) if money_line < 0 else 100 / (money_line + 100)

def get_payout(money_line):
    """takes in american formatted money line and returns the payout of a $100 bet"""
    return np.abs((100 / money_line)) * 100 if money_line < 0 else money_line

def get_data(data, team, date_obj):
    """move inside the Backtester class"""
    #print(team, date_obj)
    return [doc for doc in data if doc['game_date'] < date_obj and doc['team'] == team]

def get_refit(Backtest, data):
    """move inside backtester class"""
    return Backtest.params['model'].fit(
        [[np.mean(dict[term]) for term in Backtest.params['terms']] for dict in data],
        [dict['win'] for dict in data]
        )

def string_to_dt(string: str):

    date, time = string.split("T")[0].split("-"), string.split("T")[1].split(":") if "T" in string else ["0", "0"]
    return dt.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]))

def get_predict(Backtest, docs, team, opp, date_obj):
        
    values, predictors = [], []
    for term in Backtest.params['terms']:
        for doc in docs:
            values.append(doc[term])
        predictors.append(np.mean(values))
    if Backtest.params['model_type'] == 'classification':
        pred = Backtest.params['model'].predict_proba([predictors])[0][1]
    else:
        pred = Backtest.params['model'].predict([predictors])[0]

    return pred

def eval_result(Backtest, result_doc, team, opp, date_obj, prob, imp_prob):
        
    result, money_line, winnings, unit = result_doc['win'], result_doc['money_line'], None, 100
    if result is True:
        if money_line > 0:
            winnings = money_line
            Backtest.bankroll += winnings
        else:
            winnings = (unit/(money_line * -1)) * 100
            Backtest.bankroll += winnings
    else:
        winnings = -100
        Backtest.bankroll -= unit

    return {
        'team' : team,
        'opponent' : opp,
        'game_date' : date_obj,
        'win_bet' : result,
        'money_line' : money_line,
        'implied_probability' : imp_prob,
        'models_prediction' : round(prob, 5),
        'winnings' : '${:,.2f}'.format(winnings),
        'profit_loss' : '${:,.2f}'.format(Backtest.bankroll)
        }

def get_group_doc(team, terms):
    terms=[term for term in terms if 'opp_' not in term]
    dict = {"$group": { "_id": "$team", "game_date": {"$last": "$game_date"}}}
    for term in terms:

        dict['$group'][term] = {"$avg": f"${term}"}
    return dict

def get_group_opp_doc(opp, terms):
    terms=[term for term in terms if 'opp_' in term]
    dict = {"$group": { "_id": "$team", "game_date": {"$last": "$game_date"}}}
    for term in terms:
        
        key = term.split('opp_')[1]
        dict['$group'][f'opp_{key}'] = {"$avg": f"${key}"}
    return dict

def get_prediction_doc(team, terms, season):

    return [{"$match": {"team": team, "season": season}}, get_group_doc(team, terms)]

def get_prediction_opp_doc(opp, terms, season):

    return [{"$match": {"team": opp, "season": season}}, get_group_opp_doc(opp, terms)]

def fmt_line(line):

    return f"+{int(line)}" if line > 0 else int(line)