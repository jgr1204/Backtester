import dash, json
from dash import html, dcc
from dash.dependencies import Input, Output
from plotfunctions import BacktestPlots
from modeltest import backtest


sheets = [r'']
backtest_plots = BacktestPlots(backtest.basketball())
line_plot = {'data': [backtest_plots.bets_plot], 'layout': backtest_plots.bets_plot_layout}

app = dash.Dash(__name__,external_stylesheets=sheets)
app.layout = html.Div(
    [
        html.Div([
            dcc.Graph(id='line', figure=line_plot)
            ]),
        html.Div([
            dcc.RadioItems(
                id='radio',
                options=[{'label': 'bets', 'value': 'bets'}, {'label' : 'wins', 'value' : 'wins'}, {'label' : 'losses', 'value' : 'losses'}],
                value='bets',
                labelStyle={'display': 'inline-block'}
            )
        ]),
        html.Div([
            dcc.Graph(id='table', figure=backtest_plots.table)
        ])
    ]
)
'''
@app.callback(
    Output('table', 'figure'),
    [Input('radio', 'value')]
)
def table_choice(radio_value):
    choice, choice_map = None, {'bets' : 'bets', 'wins' : True, 'losses' : False}
    radio_value = choice_map[radio_value]
    if radio_value == 'bets':
        choice=make_table(dicts)
    else:
        bets = []
        for bet in dicts:
            if bet['win_bet'] is radio_value:
                bets.append(bet)
            else:
                pass
        choice=make_table(dicts)
    
    return choice'''
    
if __name__ == '__main__':
    app.run_server(debug=True)