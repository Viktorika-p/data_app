import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objs as go

# Load the data
data = pd.read_csv("world_population_data.csv")
ukraine_data = data[data['country'] == 'Ukraine'][["1970 population", "1980 population", "1990 population", "2000 population", "2010 population", "2015 population", "2020 population", "2022 population", "2023 population"]]
ukraine_data = ukraine_data.melt(var_name='Year', value_name='Population')
ukraine_data['Year'] = ukraine_data['Year'].str.extract('(\d+)').astype(int)
ukraine_data['Population'] = ukraine_data['Population'].astype(float)

# Load the predictions
predictions = pd.read_csv("ukraine_population_predictions.csv")

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Населення світу: з 1970 року до сьогодні"),
        html.P(
            children=(
               "З 1970 року населення планети Земля збільшилось фактично вдвічі. Це вражаюче зростання стало темою численних наукових дискусій та прогнозів."
                " Деякі науковці пророкують, що найближчі роки ми станемо свідками перенаселення та вичерпання основних природніх ресурсів."
                "Важливо зауважити, що більша частина населення планети зосереджена лише у двох країнах: Індії та Китаї. "
                "Лише у цих двох країнах проживає понад третина всіх людей на Землі, що не може не впливати на глобальні економічні, екологічні та соціальні процеси."
                "Якщо ж поглянути на дані щодо Європи, можна помітити, як європейське населення скорочується. Наш регіон відчуває демографічні зміни, що пов’язані зі старінням населення та низьким рівнем народжуваності."
                "Як зростало населення Землі на різних континентах, можна побачити на графіку."
                "Дані - worldpopulationreview.com"
            ),
        ),
         dcc.Graph(
            id='continent_population_graph',
            figure={
                "data": [
                    go.Scatter(
                        x=[1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022, 2023],
                        y=data.groupby('continent')[["1970 population", "1980 population", "1990 population", "2000 population", "2010 population", "2015 population", "2020 population", "2022 population", "2023 population"]].sum().loc[continent].values.flatten(),
                        mode='lines',
                        name=continent
                    ) for continent in data['continent'].unique()
                ],
                "layout": {"title": "Зростання населення у різних континентах"},
            },
        ),
        html.P(
            children=(
               "Детальніше поглянути на приріст населення по країнах можна на наступрому графіку:"                
            ),
        ),
        dcc.Graph(
            id='population_graph',
            figure={
                "data": [
                    go.Scatter(
                        x=[1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022, 2023],
                        y=data.loc[data['country'] == country, ["1970 population", "1980 population", "1990 population", "2000 population", "2010 population", "2015 population", "2020 population", "2022 population", "2023 population"]].values.flatten(),
                        mode='lines',
                        name=country
                    ) for country in data['country'].unique()
                ],
                "layout": {"title": "Населення у різних країнах з 1970 року до сьогодні"},
            },
        ), 
        html.H1(children="А що ж в Україні? "),
        html.P(
            children=(
               "Починаючи з 1990 року населення України продовжує зменшуватись."
               "Повномасштабне російське вторгнення значно посилило цю проблему."
                "Так, у 2023 році, за підрахунками worldpopulationreview, населення України становило трохи більше 36,7 мільнона людей."          
            ),
        ), 
        html.Div(
            style={
                'display': 'grid',
                'grid-template-columns': '1fr 1fr',
                'gap': '20px',
                'margin': '20px 0'
            },
            children=[ 
                dcc.Graph(
                    id='ukraine_population_graph_actual',
                    figure={
                        "data": [
                            go.Scatter(
                                x=ukraine_data['Year'],
                                y=ukraine_data['Population'],
                                mode='lines+markers',
                                name='Ukraine Actual Population',
                                marker=dict(size=8),
                                line=dict(width=2)
                            )
                        ],
                        "layout": {"title": "Населення України з 1970 року до сьогодні"},
                    },
                ),
                html.Div(
                    style={'border': '1px solid black', 'padding': '10px'},
                    children=[
                        html.H3("Кількість населення України"),
                        html.Table(
                            [
                                html.Thead(html.Tr([html.Th("Year"), html.Th("Population")])),
                                html.Tbody(
                                    [
                                        html.Tr([html.Td(year), html.Td(population)])
                                        for year, population in zip(ukraine_data['Year'], ukraine_data['Population'])
                                    ]
                                ),
                            ],
                            className='table'
                        ),
                    ]
                ),
            ]
        ),       
        html.P(
            children=(
            "Я спробувала передбачити кількість населення України у майбутньому за допомогою методів машинного навчання."           
            "Аналізуючи дані про населення за різні роки, "
            "модель лінійної регресії виявляє залежність між роками та кількістю людей, щоб робити припущення щодо майбутнього населення."
        ),
        ),
        html.P(
            children=(
            "За підрахунком алгоритму - наслення України продовжуватиме зменшуватись. "     
            "Так, у 2040 році, відповідно до підрахунків, населення України становитиме трохи більше 32 мільйонів людей."      
        ),
        ),
        html.Div(
            style={
                'display': 'grid',
                'grid-template-columns': '1fr 1fr',
                'gap': '20px',
                'margin': '20px 0'
            },
            children=[
                dcc.Graph(
                    id='ukraine_population_graph_predicted',
                    figure={
                        "data": [
                            go.Scatter(
                                x=predictions['Year'],
                                y=predictions['Predicted Population'],
                                mode='lines+markers',
                                name='Ukraine Predicted Population',
                                marker=dict(size=8, color='red'),
                                line=dict(width=2, color='red')
                            )
                        ],
                        "layout": {
                            "title": "Прогнозована кількість населення України",
                            "height": 600, 
                            "width": 800  
                        },
                    },
                ),
                html.Div(
                    style={'border': '1px solid black', 'padding': '10px'},
                    children=[
                        html.H3("Прогнозована кількість населення"),
                        html.Table(
                            [
                                html.Thead(html.Tr([html.Th("Year"), html.Th("Predicted Population")])),
                                html.Tbody(
                                    [
                                        html.Tr([html.Td(year), html.Td(population)])
                                        for year, population in zip(predictions['Year'], predictions['Predicted Population'])
                                    ]
                                ),
                            ],
                            className='table'
                        ),
                    ]
                ),
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
