from funcs import get_data, get_predict, get_refit, eval_result, get_implied_probability, string_to_dt
from connect import db
import datetime as dt
import numpy as np


class Backtest:
    
    def __init__(self, params):

        self.cursor = db.cursor()
        self.params = params
        self.date = params["start_date"] + dt.timedelta(hours=8)
        self.bets = []
        self.bankroll = 0
    
    @property
    def games(self):

        self.cursor.execute(
            """
            SELECT
                row_to_json(t)
            FROM
            (
                SELECT
                    game.*, game_advanced.*,
                    game_opp.*, game_opp_advanced.*
                FROM
                    game
                JOIN
                    game_advanced
                        ON
                    game.money_line is not null
                        AND
                    game.game_id = game_advanced.game_id
                        AND
                    game.team = game_advanced.team
                JOIN
                    game_opp
                        ON
                    game.game_id = game_opp.game_id
                        AND
                    game.team = game_opp.team
                JOIN
                    game_opp_advanced
                        ON
                    game.game_id = game_opp_advanced.game_id
                        AND
                    game.team = game_opp_advanced.team
                ORDER BY
                    game.game_date
            )
            t;
            """
        )
        return [_[0] for _ in self.cursor.fetchall()]

    @property
    def data(self):

        return 
    def basketball(self):
        dates, games = [], self.games

        contests = [dict for dict in games if string_to_dt(dict["game_date"]) > self.date]
        for idx in range(0, len(contests)):
            
            game_doc, result_doc, data = contests[idx], None, [dict for dict in games if string_to_dt(dict["game_date"]) < self.date]
            team, opp = game_doc['team'], game_doc['opp'] 
            date_obj, imp_prob = game_doc['game_date'].split("T")[0], get_implied_probability(game_doc['money_line'])

            if self.params['refit'] is True and date_obj not in dates:
                dates.append(date_obj)
                self.date = string_to_dt(date_obj)
                self.model = get_refit(self, get_data(data, team, date_obj))

            pred = get_predict(self, data, team, opp, date_obj)
            if imp_prob + self.params['required_edge'] < pred > self.params['threshold']:
                result_doc = game_doc
            else:
                result_doc = None
            if result_doc:
                self.bets.append(eval_result(self, result_doc, team, opp, date_obj, pred, imp_prob))
            else:
                pass
            
        return self.bets
