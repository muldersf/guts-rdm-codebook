import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import os

# load measure overview
file_path = os.path.join("data", "guts-measure-overview_gh.xlsx")
df = pd.read_excel(file_path, index_col=0)

# get unique data types
unique_data_types = df['data_type'].unique()
unique_cohorts = df['cohort'].unique()

# create app
app = dash.Dash(__name__)

server = app.server

# create layout app
app.layout = html.Div([
    # create header
    #html.H1("GUTS measures", style={'font-family': 'sans-serif'}),

    html.Div([
    # create dropdown menu 1
    html.Div([
        html.P("Choose your data type:", style={'margin-top': '10px'}),
        dcc.Dropdown(
            id='data-type-dropdown',
            options=[{'label': 'all data types', 'value': 'all'}] +
                    [{'label': data_type, 'value': data_type} for data_type in unique_data_types],
            value='all',  
            multi=False,
            style={'width': '150px', 'margin-left': '2px', 'font-family': 'sans-serif'}
        ),
    ], style={'display': 'flex', 'flexDirection': 'row', 'font-family': 'sans-serif'}),

    # create dropdown menu 2
    html.Div([
        html.P("Choose your cohort:", style={'margin-top': '10px'}),
        dcc.Dropdown(
            id='cohort-dropdown',
            options=[
            {'label': 'A', 'value': 'A'},
            {'label': 'B', 'value': 'B'},
            {'label': 'C', 'value': 'C'},
            {'label': 'D', 'value': 'D'},
            {'label': 'only overlapping cohorts', 'value': 'overlapping'},
            {'label': 'all cohorts', 'value': 'all'}
            ],
            value=None,  
            multi=False,
            style={'width': '150px', 'margin-left': '2px', 'font-family': 'sans-serif'}
        ),
    ], style={'display': 'flex', 'flexDirection': 'row', 'font-family': 'sans-serif'}),

    # create search bar for measure
    html.Div([
        html.P("Search by measure name:", style={'margin-top': '10px'}),
        dcc.Input(
            id='measure-search',
            type='text',
            placeholder='Enter measure name...',
            style={'width': '180px', 'height': '30px', 'margin-left': '2px', 'margin-bottom': '2px', 'font-family': 'sans-serif', 'borderRadius': '5px'}
        ),
    ], style={'display': 'flex', 'flexDirection': 'row', 'paddingBottom': '10px', 'font-family': 'sans-serif'}),
    
    
    # create default data table and style it
    dash_table.DataTable(
        id='table',
        # set column names
        columns=[
            {'name': 'Measure', 'id': 'long_name'},
            {'name': 'Short name', 'id': 'short_name'},
            {'name': 'Data type', 'id': 'data_type'},
            {'name': 'Cohort', 'id': 'cohort'}
        ],
        # set data to measure overview
        data=df.to_dict('records'),
        style_as_list_view=True,
        # style table
        style_header={'backgroundColor': 'gray',
                       'fontWeight': 'bold',
                        'color': 'black',
                        'font-family': 'sans-serif'},
        style_cell={
            'textAlign': 'left',
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px',  
            'font_size': '14px' ,
            'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
        },
        style_data={
        'color': 'black',
        'backgroundColor': 'white',
        'fontFamily': 'sans-serif'
    },
    # set alternating cell colors
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        },
        {
            'if': {'column_id': 'long_name'},
            'width': '50%'
        },
        {   'if': {'column_id': 'cohort'},
            'width': '20%'
        },
    ],
    style_cell_conditional=[
    {'if': {'column_id': 'long_name'},
     'paddingLeft': '20px'},
  
    ],
        style_table={'height': '500px', 
                     'overflowY': 'auto',
                     'width': '800px',
                     'boxShadow': '0px 0px 10px 0px rgba(0, 0, 0, 0.1)',
                     'borderRadius': '10px' },
    ),
])
], style={'width': '850px', 'paddingLeft': '20px', 'paddingTop': '20px', 'paddingBottom': '20px'})

# set call back based on input values of dropdown menus
@app.callback(
    Output('table', 'data'),
    [Input('data-type-dropdown', 'value'),
     Input('cohort-dropdown', 'value'),
     Input('measure-search', 'value')]
)
# make function to update table
def update_table(selected_data_type, selected_cohort, search_value):
    filtered_df = df
    
    # filter by data type if selected
    if selected_data_type and selected_data_type != 'all':
        filtered_df = filtered_df[filtered_df['data_type'] == selected_data_type]

    # filter by cohort if selected
    if selected_cohort and selected_cohort != 'all':
        if selected_cohort == 'overlapping':
            # Select rows where 'cohort' column contains more than one letter
            filtered_df = filtered_df[filtered_df['cohort'].apply(lambda x: len(x) > 1)]
        else:
            # Select rows where 'cohort' column exactly matches selected cohort
            filtered_df = filtered_df[filtered_df['cohort'].str.contains(selected_cohort)]
    
    # filter by measure name using search value
    if search_value:
        filtered_df = filtered_df[filtered_df['long_name'].str.contains(search_value, case=False)]

    return filtered_df.to_dict('records')

# run app
if __name__ == '__main__':
    app.run(debug=True)
