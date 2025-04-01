import dash
from dash import dcc, html

import pandas as pd

# Load the data
world_cup_data = pd.DataFrame({
    'Team': ['Brazil', 'Germany', 'Italy', 'Argentina', 'France', 'Uruguay', 'England', 'Spain',
             'Netherlands', 'Hungary', 'Czechoslovakia'],
    'Winners': [5, 4, 4, 3, 2, 2, 1, 1, 0, 0, 0],
    'Runners-up': [2, 4, 2, 3, 2, 0, 0, 0, 3, 2, 2],
    'Total finals': [7, 8, 6, 6, 4, 2, 1, 1, 3, 2, 2],
    'Years won': ['1958, 1962, 1970, 1994, 2002',
                 '1954, 1974, 1990, 2014',
                 '1934, 1938, 1982, 2006',
                 '1978, 1986, 2022',
                 '1998, 2018',
                 '1930, 1950',
                 '1966',
                 '2010',
                 '-',
                 '1938, 1954',
                 '1934, 1962'],
    'Years runners-up': ['1950, 1998',
                         '1966, 1982, 1986, 2002',
                         '1970, 1994',
                         '1930, 1990, 2014',
                         '2006, 2022',
                         '-',
                         '-',
                         '-',
                         '1974, 1978, 2010',
                         '-',
                         '-']
})

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Pick a year to view the World Cup Winner and their Runner-up"),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{"label": year, "value": year} for year in sorted(set(
            sorted(set(sum([[int(year) for year in str(years).replace('-', '').split(',')] for years in world_cup_data['Years won'] if years != '-'], [])))))],
        placeholder="Select a year"
    ),
    html.Div(id="year-result-output"),
    html.H2("Pick a country to view World Cup wins"),
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": team, "value": team} for team in world_cup_data["Team"].tolist()],
        placeholder="Select a country"
    ),
    html.Div(id="country-wins-output"),
    html.H1("FIFA World Cup Winners"),
    html.Button("Show Winning Countries", id="show-winners-button", n_clicks=0),
    html.Div(id="output-div")
])

@app.callback(
    dash.Output("year-result-output", "children"),
    [dash.Input("year-dropdown", "value")]
)
def display_winner_and_runnerup(selected_year):
    if selected_year:
        selected_year = str(selected_year)
        winner = next((row['Team'] for _, row in world_cup_data.iterrows() if selected_year in row['Years won']), None)
        runner_up = next((row['Team'] for _, row in world_cup_data.iterrows() if selected_year in row['Years runners-up']), None)
        return f"In {selected_year}, Winner: {winner or 'Unknown'}, Runner-up: {runner_up or 'Unknown'}"
    return "Select a year to see the results."

@app.callback(
    dash.Output("country-wins-output", "children"),
    [dash.Input("country-dropdown", "value")]
)
def display_wins(selected_country):
    if selected_country:
        wins = world_cup_data[world_cup_data['Team'] == selected_country]['Winners'].values[0]
        return f"{selected_country} has won the World Cup {wins} times."
    return "Select a country to see the number of wins."

@app.callback(
    dash.Output("output-div", "children"),
    [dash.Input("show-winners-button", "n_clicks")]
)
def show_winners(n_clicks):
    if n_clicks > 0:
        winners = world_cup_data[world_cup_data['Winners'] > 0]['Team'].tolist()
        return html.Ul([html.Li(country) for country in winners])
    return "Click the button to see winning countries."

if __name__ == "__main__":
    app.run(debug=True)
