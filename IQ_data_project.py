import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_table

# Load the dataset
df = pd.read_csv('archive/International_IQ.csv')

# Sort the DataFrame by average IQ in descending order
sorted_df = df.sort_values(by='Average IQ', ascending=False)

# Get the top 10 highest average IQ scores
top_10_df = sorted_df.head(10)

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("International IQ Scores by Country", className="text-center mb-4"), width=12)
    ),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='country-dropdown',
                options=[
                    {'label': 'All Countries', 'value': 'All'},  # Add an option for all countries
                ] + [{'label': country, 'value': country} for country in df['Country'].dropna().unique()],
                value='All',  # Set the initial value to 'All'
                className="mb-4",
            ),
            width={'size': 4, 'offset': 4}
        ),
    ]),
    dbc.Row(
        dbc.Col(dcc.Graph(id='world-map'), width=12)
    ),
   dbc.Row(
        dbc.Col(html.H1("Top 10 Highest Average IQ Scores by Country", className="text-center mb-4"), width=12)
    ),
    dbc.Row(
        dbc.Col(dash_table.DataTable(
            id='table',
            columns=[{"name": col, "id": col} for col in top_10_df.columns],
            data=top_10_df.to_dict('records'),
                        style_table={'height': '400px', 'overflowY': 'auto', 'width': '50%', 'margin': '0 auto'},  # Adjust the width here
        ), width=12)
    )
], fluid=True)

# Define a callback to update the world map based on the selected country
@app.callback(
    Output('world-map', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_world_map(selected_country):
    if selected_country == 'All':
        # Display all countries without filtering
        fig = px.choropleth(
            df,
            locations='Country',
            locationmode='country names',
            color='Average IQ',
            hover_name='Country',
            color_continuous_scale=px.colors.sequential.Plasma,
            title=f'Average IQ Scores for All Countries'
        )
    else:
        # Filter the dataset for the selected country
        filtered_df = df[df['Country'] == selected_country]

        # Create the world map using Plotly Express
        fig = px.choropleth(
            filtered_df,
            locations='Country',
            locationmode='country names',
            color='Average IQ',
            hover_name='Country',
            color_continuous_scale=px.colors.sequential.Plasma,
            title=f'Average IQ Scores for {selected_country}'
        )
    
    # Customize the layout
    fig.update_geos(projection_type="natural earth")
    fig.update_coloraxes(colorbar_title="Average IQ")

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
