# dashboard.py
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Crear una aplicación Dash
app = Dash(__name__)

# Datos de ejemplo
df = pd.DataFrame({
    "Categoría": ["A", "B", "C", "D"],
    "Valores": [4, 1, 2, 3]
})

# Gráfico interactivo
fig = px.bar(df, x="Categoría", y="Valores", title="Gráfico de Barras Interactivo")

# Layout del dashboard
app.layout = html.Div(children=[
    html.H1(children='Dashboard Interactivo'),

    # Gráfico de barras
    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    # Dropdown para seleccionar categorías
    dcc.Dropdown(
        id='categoria-dropdown',
        options=[{'label': i, 'value': i} for i in df['Categoría'].unique()],
        value='A',  # Valor por defecto
        clearable=False
    ),

    # Gráfico de pastel interactivo
    dcc.Graph(id='pie-chart')
])

# Callback para actualizar el gráfico de pastel
@app.callback(
    dash.dependencies.Output('pie-chart', 'figure'),
    [dash.dependencies.Input('categoria-dropdown', 'value')]
)
def update_pie_chart(selected_category):
    filtered_df = df[df['Categoría'] == selected_category]
    fig = px.pie(filtered_df, values='Valores', names='Categoría', title=f'Distribución para {selected_category}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)