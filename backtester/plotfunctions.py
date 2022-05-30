import datetime as dt
import plotly.graph_objs as go


class BacktestPlots:

    def __init__(self, bets):

        self.bets = bets

    @staticmethod
    def make_hovertext(bet):

        return """
        team = {}<br>opponent = {}<br>winnings = {}<br>prediction = {}
        <br>money line = {}<br>implied probability = {}<br>bankroll = {}<br>game date={}
        """.format(
            bet['team'], bet['opponent'], bet['winnings'], bet['models_prediction'],
            bet['money_line'], bet['implied_probability'], bet['profit_loss'], bet['game_date']
            )

    @property
    def hovertext(self):

        return [self.make_hovertext(bet) for bet in self.bets]

    @property
    def game_titles(self):
        titles=[]
        for bet in self.bets:
            team, opp, date = bet['team'], bet['opponent'], bet['game_date']
            titles.append(f"""{team} vs. {opp}\t:\t{date}""")
        return titles

    @property
    def bets_plot(self):

        return go.Scatter(
            x=[bet['game_date'] for bet in self.bets],
            y=[bet['profit_loss'] for bet in self.bets],
            yaxis='y1',
            mode='lines+markers',
            line={'width': 4, 'color': '#d4af37'},
            marker={'symbol': 'star-diamond', 'size': 10},
            fill='tozeroy',
            hovertext=self.hovertext,
            hoverinfo='text',
            text=[bet['winnings'] for bet in self.bets],
            textposition='top center'
        )

    @property
    def bets_plot_layout(self):

        return {
            'title' : {'text' : '<b>Bankroll',
            'font' : {'size' : 24}},
            'yaxis' : {'title' : '<b>$', 'font' : {'size' : 96}},
            'xaxis' : {'range' : [self.bets[0]['game_date'], self.bets[int(len(self.bets) / 2)]['game_date'], self.bets[-1]['game_date']], 'showticklabels' : True},
            'hovermode' : 'closest',
            'showlegend' : False
            }

    @property
    def table(self):
        

        rowodd, roweven, = 'white', 'lightgrey'
        table_trace = go.Table(
            header={
            'values' : ['<b>game', '<b>winnings', '<b>win','<b>prediction', '<b>implied probability', '''<b>model's "edge"''','<b>money line', '<b>profit / loss'],
                'font' : {'size' : 14},
                'fill' : {'color' : 'rgb(255, 215, 0)'},
                'line' : {'color' : 'rgb(0, 0, 0)'},
                'align' : 'center',
                'height' : 40
            },
            cells={
                'values' : [
                    ['<b>' + game for game in self.game_titles],
                    ['<b>' + bet['winnings'] for bet in self.bets],
                    ['<b>' + str(bet['win_bet']) for bet in self.bets],
                    ['<b>' + str(bet['models_prediction']) for bet in self.bets],
                    ['<b>' + str(round(bet['implied_probability'], 5)) for bet in self.bets],
                    ['<b>' + str(round(bet['models_prediction'] - bet['implied_probability'], 5)) for bet in self.bets],
                    ['<b>' + str(int(bet['money_line'])) for bet in self.bets],
                    ['<b>' + bet['profit_loss'] for bet in self.bets]
                ],
                'fill' : {'color' : [[rowodd, roweven, rowodd, roweven, rowodd, roweven]*len(self.bets)]},
                'line' : {'color' : 'rgb(0, 0, 0)'},
                'font' : {'size' : 12},
                'height' : 30
            }
        )
        layout_table = {
            'title' : {'text' : '<b>Bets', 'font' : {'size' : '24'}}
        }

        return {'data' : [table_trace], 'layout' : layout_table}