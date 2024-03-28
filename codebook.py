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
unique_cohorts = ['A', 'B', 'C', 'D']

# create app
app = dash.Dash(__name__)

server = app.server

# create layout app
app.layout = html.Div([
    # create header
    #html.H1("GUTS measures", style={'font-family': 'sans-serif'}),

    html.Div([
        html.Div([
            # create checkbox for cohorts
            html.Div([
                html.P("Choose cohort:", style={'font-weight': 'bold','height': '17px','paddingLeft': '10px', 'paddingTop': '5px', 'paddingBottom': '5px', 'margin-top': '10px','borderRadius': '5px', 'backgroundColor': 'gray'}),
                dcc.Checklist(
                    id='cohort-checkboxes',
                    options=[
                        {'label': 'all cohorts', 'value': 'all'},
                        {'label': 'only overlapping cohorts', 'value': 'overlapping'}
                    ] + [{'label': cohort, 'value': cohort} for cohort in unique_cohorts],
                    style={'font-family': 'sans-serif', 'paddingBottom': '10px'}
                ),
            ], style={'margin-left': '10px','display': 'flex', 'flexDirection': 'column', 'font-family': 'sans-serif'}),

            # create dropdown menu 1
            html.Div([
                html.P("Choose data type:", style={'font-weight': 'bold','height':'17px','paddingLeft': '10px', 'paddingTop': '5px', 'paddingBottom': '5px', 'margin-top': '10px','borderRadius': '5px', 'backgroundColor': 'gray'}),
                dcc.Dropdown(
                    id='data-type-dropdown',
                    options=[{'label': 'all data types', 'value': 'all'}] +
                            [{'label': data_type, 'value': data_type} for data_type in unique_data_types],
                    value='all',  
                    multi=False,
                    style={'width': '150px', 'margin-left': '2px', 'font-family': 'sans-serif'}
                ),
            ], style={'display': 'flex', 'flexDirection': 'column', 'margin-left': '15px', 'margin-right': '15px', 'font-family': 'sans-serif'}),

            # create search bar for measure
            html.Div([
                html.P("Search by measure name:", style={'font-weight': 'bold','height':'17px','paddingLeft': '10px', 'paddingTop': '5px', 'paddingBottom': '5px', 'margin-top': '10px','borderRadius': '5px', 'backgroundColor': 'gray', 'width': '200px'}),
                dcc.Input(
                    id='measure-search',
                    type='text',
                    placeholder='Enter measure name...',
                    style={'margin-top': '1px','height': '30px', 'margin-left': '2px', 'margin-bottom': '2px', 'font-family': 'sans-serif', 'borderRadius': '5px'}
                ),
            ], style={'display': 'flex', 'flexDirection': 'Column', 'paddingBottom': '10px', 'font-family': 'sans-serif'}),
        ], style = {'fontSize': '14px','fontFamily': 'sans-serif','paddingBottom': '10px','marginBottom':'10px','display': 'flex', 'flexDirection': 'row', 'backgroundColor': 'rgb(211,211,211)', 'width': '680px', 'borderRadius': '5px', 'boxShadow': '0px 0px 10px 0px rgba(0, 0, 0, 0.1)'}),
    
    
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
                     'width': '680px',
                     'boxShadow': '0px 0px 10px 0px rgba(0, 0, 0, 0.1)',
                     'borderRadius': '10px' },
    ),
])
], style={'width': '850px', 'paddingLeft': '20px', 'paddingTop': '20px', 'paddingBottom': '20px'})

# set call back based on input values of dropdown menus
@app.callback(
    Output('table', 'data'),
    [Input('data-type-dropdown', 'value'),
     Input('cohort-checkboxes', 'value'),
     Input('measure-search', 'value')]
)
# make function to update table
def update_table(selected_data_type, selected_cohort, search_value):
    filtered_df = df
    print("Selected data type:", selected_data_type)
    print("Selected cohort:", selected_cohort)
    print("Search value:", search_value)
    
    # filter by data type if selected
    if selected_data_type and selected_data_type != 'all':
        filtered_df = filtered_df[filtered_df['data_type'] == selected_data_type]
    
    if selected_cohort and 'all' not in selected_cohort:
        if 'overlapping' in selected_cohort:
            filtered_df = filtered_df[filtered_df['cohort'].apply(lambda x: len(x) > 1)]
        else:
            filtered_df = filtered_df[filtered_df['cohort'].str.contains('|'.join(selected_cohort))]

    # filter by measure name using search value
    if search_value:
        filtered_df = filtered_df[filtered_df['long_name'].str.contains(search_value, case=False)]

    return filtered_df.to_dict('records')

# run app
if __name__ == '__main__':
    app.run(debug=True)
