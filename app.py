from flask import Flask, render_template
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Crear la aplicación Flask
app = Flask(__name__)  # Cambié 'server' a 'app' para que Gunicorn lo reconozca

# Ruta principal de Flask (tu CV)
@app.route('/')
def cv():
    return render_template('cv.html')

# Crear la aplicación Dash dentro de Flask
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/')

# Datos de ejemplo: Habilidades técnicas y nivel de competencia
df = pd.DataFrame({
    "Habilidad": ["Python", "SQL", "Machine Learning", "Flask", "Pandas"],
    "Nivel": [8, 7, 6, 5, 9]  # Nivel de competencia (0-10)
})

# Layout del dashboard
dash_app.layout = html.Div(children=[
    html.H1(children='Mis Habilidades Técnicas'),

    # Gráfico de barras: Habilidades y nivel de competencia
    dcc.Graph(
        id='habilidades-graph',
        figure=px.bar(df, x="Habilidad", y="Nivel", title="Nivel de Competencia en Habilidades Técnicas")
    ),

    # Dropdown para seleccionar una habilidad
    dcc.Dropdown(
        id='habilidad-dropdown',
        options=[{'label': i, 'value': i} for i in df['Habilidad'].unique()],
        value='Python',  # Valor por defecto
        clearable=False
    ),

    # Gráfico de pastel: Distribución del nivel de competencia
    dcc.Graph(id='nivel-pie-chart')
])

# Callback para actualizar el gráfico de pastel
@dash_app.callback(
    Output('nivel-pie-chart', 'figure'),
    [Input('habilidad-dropdown', 'value')]
)
def update_pie_chart(selected_habilidad):
    filtered_df = df[df['Habilidad'] == selected_habilidad]
    fig = px.pie(filtered_df, values='Nivel', names='Habilidad', title=f'Nivel de Competencia en {selected_habilidad}')
    return fig

# No es necesario el bloque `if __name__ == '__main__':` para Flask cuando usas Gunicorn
