import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

parties_data = {
    "Партія": ["Socialdemokratiet", "Venstre", "Moderaterne", "Socialistisk Folkeparti", "Danskdemokraterne", "Liberal Alliance", "Det Konservative Folkeparti", "Enhedslisten - De Rød-Grønne", "Radikale Venstre", "Nye Borgerlige", "Alternativet", "Dansk Folkeparti", "Frie Grønne", "KD - Kristendemokraterne"],
    "Відсоток голосів": [27.5, 13.32, 9.2, 8.3, 8.1, 7.8, 5.5, 5.1, 3.7, 3.6, 3.3, 2.6, 0.9, 0.5]
}

parties_df = pd.DataFrame(parties_data)

economy_data = {
    "Індикатор": ["GDP (in billion $)", "Unemployment Rate (%)", "Inflation Rate (%)"],
    "Значення": [370, 5.0, 1.2]
}

parliament_seats_data = {
    "Партія": ["Socialdemokratiet", "Venstre", "Moderaterne", "SF", "Danskdemokraterne", "Liberal Alliance", "Det Konservative Folkeparti", "Enhedslisten - De Rød-Grønne", "Radikale Venstre", "Nye Borgerlige", "Alternativet", "Dansk Folkeparti"],
    "Кількість місць": [50, 23, 16, 15, 14, 14, 10, 9, 7, 6, 6, 5]
}

parliament_seats_df = pd.DataFrame(parliament_seats_data)

economy_df = pd.DataFrame(economy_data)

app.layout = html.Div([
    html.Div([
        html.H4("Карта Данії"),
        dcc.Graph(
            id='map',
            figure=px.scatter_mapbox(
                lat=[56.26392],
                lon=[9.501785],
                zoom=5,
                mapbox_style="open-street-map"
            ).update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        )
    ], className='section'),

    html.Div([
        html.H4("Політична система"),
        dcc.Graph(
            id='parties',
            figure=px.pie(parties_data, names="Партія", values="Відсоток голосів", title="Результи виборів 2022")
        )
    ], className='section'),

    html.Div([
        html.H4("Економічне положення"),
        dcc.Graph(
            id='economy',
            figure=px.bar(economy_df, x="Індикатор", y="Значення", title="Економічне положення Данії")
        )
    ], className='section'),

    html.Div([
        html.H4("Логіка формування політичної влади"),
        html.P("Данія є парламентською конституційною монархією. Королева є головою держави, але її роль є переважно церемоніальною. Влада належить парламенту (Фолькетингу) та уряду, який очолює прем'єр-міністр. Вибори до парламенту проводяться кожні чотири роки."),
        html.P("Парламент (Фолькетинг) складається з 179 членів, обраних за пропорційною системою. Найпопулярніші партії та їх кількість місць у парламенті можна побачити нижче."),
        dcc.Graph(
            id='parliament_seats',
            figure=px.bar(parliament_seats_data, x="Партія", y="Кількість місць", title="Парламент Данії")
        )
    ], className='section')
], className='container')

if __name__ == '__main__':
    app.run_server(debug=True)
