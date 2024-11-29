import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash.dash_table
import plotly.express as px
import plotly.graph_objs as go

from Analytics.analytics import prepare_data, calculate_key_metrics
from Analytics.load_data import load_data
from sql_analytics.sql_queries import *
from sql_analytics.load_data import load_data_sql

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Load and prepare data
df = load_data()
df = prepare_data(df)

data2, spark = load_data_sql()
top_ten_customer = get_top_ten_customer(spark=spark)
top_five_products_df = get_top_five_products(spark=spark)
top_five_cities_df = get_top_five_cities(spark=spark)
most_purchased_products = get_most_purchased_products(spark=spark)
revenue_by_month = get_revenue_by_month(spark=spark)
less_purchased_products = get_less_purchased_products(spark=spark)

top_ten_customer_df = top_ten_customer.toPandas()
top_five_products_df = top_five_products_df.toPandas()
top_five_cities_df = top_five_cities_df.toPandas()
most_purchased_products = most_purchased_products.toPandas()
revenue_by_month = revenue_by_month.toPandas()
less_purchased_products = less_purchased_products.toPandas()

# Calculate key metrics
total_revenue, total_customers, total_transactions, avg_order_value = calculate_key_metrics(df)

# App layout
app.layout = html.Div([
    html.Div([
        html.H1('E-commerce Analytics Dashboard', 
                style={
                    'textAlign': 'center', 
                    'color': '#2c3e50', 
                    'fontWeight': 'bold', 
                    'marginBottom': '20px',
                    'borderBottom': '2px solid #3498db',
                    'paddingBottom': '10px'
                })
    ]),
    
    # Tabs
    dcc.Tabs([
        # First Tab: Overview
        dcc.Tab(label='Overview', children=[
            # Key Metrics Section
            html.Div([
                html.Div([
                    html.H4('Total Revenue', style={'color': '#34495e'}),
                    html.H3(f'${total_revenue:,.2f}', style={'color': '#3498db'})
                ], className='metric-box'),
                html.Div([
                    html.H4('Total Customers', style={'color': '#34495e'}),
                    html.H3(f'{total_customers:,}', style={'color': '#3498db'})
                ], className='metric-box'),
                html.Div([
                    html.H4('Total Transactions', style={'color': '#34495e'}),
                    html.H3(f'{total_transactions:,}', style={'color': '#3498db'})
                ], className='metric-box'),
                html.Div([
                    html.H4('Avg Order Value', style={'color': '#34495e'}),
                    html.H3(f'${avg_order_value:.2f}', style={'color': '#3498db'})
                ], className='metric-box'),
            ], style={
                'display': 'flex', 
                'justifyContent': 'space-around', 
                'margin': '20px',
                'backgroundColor': '#f0f2f5',
                'padding': '15px',
                'borderRadius': '10px'
            }),
            
            # First Row of Charts
            html.Div([
                html.Div([
                    html.H3('Sales Distribution by Customer Type', style={'color': '#2c3e50'}),
                    dcc.Graph(id='customer-type-pie')
                ], style={'width': '40%', 'display': 'inline-block', 'padding': '10px'}),
                
                html.Div([
                    html.H3('Sales by Category', style={'color': '#2c3e50'}),
                    dcc.Graph(id='category-bar')
                ], style={'width': '60%', 'display': 'inline-block', 'padding': '10px'})
            ], style={'display': 'flex', 'justifyContent': 'space-between'})
        ]),
        
        # Second Tab: Time-based Sales Trends
        dcc.Tab(label='Time-based Sales Trends', children=[
            # Filters
            html.Div([
                html.Div([
                    html.Label('Customer Type', style={'fontWeight': 'bold'}),
                    dcc.RadioItems(
                        id='customer-type-filter',
                        options=[{'label': ct, 'value': ct} for ct in df['customer_type'].unique()],
                        value=df['customer_type'].unique()[0],
                        labelStyle={'display': 'block'},
                        style={'width': '100%'},
                    )
                ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px'}),
                
                html.Div([
                    html.Label('Time Period', style={'fontWeight': 'bold'}),
                    dcc.RadioItems(
                        id='time-filter',
                        options=[
                            {'label': 'Daily', 'value': 'day'},
                            {'label': 'Monthly', 'value': 'month'},
                            {'label': 'Hourly', 'value': 'hour'}
                        ],
                        value='day',
                        labelStyle={'display': 'block'},
                        style={'width': '100%'}
                    )
                ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px'})
            ], style={'textAlign': 'center', 'margin': '20px'}),
            
            # Second Row of Charts
            html.Div([
                html.Div([
                    dcc.Graph(id='time-series')
                ], style={'width': '100%', 'padding': '10px'})
            ]),

                   ]),

        dcc.Tab(label='SQL Queries', children=[
            html.Div([
                # Top 10 Customers Table
                html.H3('Top 100 Customers by Total Spent', style={'color': '#2c3e50'}),
                dash.dash_table.DataTable(
                    id='sql-queries-table',
                    columns=[
                        {"name": "Customer Name", "id": "customer_name"},
                        {"name": "Total Spent", "id": "total_spent"}
                    ],
                    data=top_ten_customer_df.to_dict('records'),
                    style_table={'overflowX': 'auto', 'maxHeight': '300px', 'overflowY': 'scroll'},  # Scrollable table
                    style_cell={
                        'textAlign': 'left',
                        'padding': '5px',
                        'backgroundColor': '#f0f2f5',
                        'border': '1px solid #ddd',
                    },
                    style_header={
                        'fontWeight': 'bold',
                        'backgroundColor': '#3498db',
                        'color': 'white',
                        'textAlign': 'center',
                    },
                    page_size=10
                )
            ], style={'padding': '20px'}),

            # Most Purchased Products Table
            html.Div([
                html.H3('Most Purchased Products', style={'color': '#2c3e50'}),
                dash.dash_table.DataTable(
                    id='most-purchased-products-table',
                    columns=[
                        {"name": "Product Name", "id": "product_name"},
                        {"name": "Total Quantity", "id": "total_quantity"}
                    ],
                    data=most_purchased_products.to_dict('records'),
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '5px',
                        'backgroundColor': '#f0f2f5',
                        'border': '1px solid #ddd',
                    },
                    style_header={
                        'fontWeight': 'bold',
                        'backgroundColor': '#2ecc71',
                        'color': 'white',
                        'textAlign': 'center',
                    },
                    page_size=10
                )
            ], style={'padding': '20px'}),

            # Less Purchased Products Table
            html.Div([
                html.H3('Less Purchased Products', style={'color': '#2c3e50'}),
                dash.dash_table.DataTable(
                    id='less-purchased-products-table',
                    columns=[
                        {"name": "Product Name", "id": "product_name"},
                        {"name": "Total Quantity", "id": "total_quantity"}
                    ],
                    data=less_purchased_products.to_dict('records'),
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '5px',
                        'backgroundColor': '#f0f2f5',
                        'border': '1px solid #ddd',
                    },
                    style_header={
                        'fontWeight': 'bold',
                        'backgroundColor': '#e74c3c',
                        'color': 'white',
                        'textAlign': 'center',
                    },
                    page_size=10
                )
            ], style={'padding': '20px'}),

            # Top 5 Products by Revenue Table
            html.Div([
                html.H3('Top 5 Products by Revenue', style={'color': '#2c3e50'}),
                dash.dash_table.DataTable(
                    id='top-five-products-table',
                    columns=[
                        {"name": "Product Name", "id": "product_name"},
                        {"name": "Total Revenue", "id": "total_revenue"}
                    ],
                    data=top_five_products_df.to_dict('records'),
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '5px',
                        'backgroundColor': '#f0f2f5',
                        'border': '1px solid #ddd',
                    },
                    style_header={
                        'fontWeight': 'bold',
                        'backgroundColor': '#9b59b6',
                        'color': 'white',
                        'textAlign': 'center',
                    },
                    page_size=10
                )
            ], style={'padding': '20px'}),

            # Monthly Revenue Candlestick Chart
            html.Div([
            html.H3('Monthly Revenue Trends', style={'color': '#2c3e50'}),
            dcc.Graph(
                id='revenue-by-month-chart',
                figure={
                    'data': [
                        go.Bar(
                            x=revenue_by_month['month'],
                            y=revenue_by_month['total_revenue'],
                            name='Revenue',
                            marker_color='#3498db'
                        )
                    ],
                    'layout': {
                        'title': 'Monthly Revenue Trends',
                        'xaxis': {'title': 'Month'},
                        'yaxis': {'title': 'Revenue'},
                        'plot_bgcolor': '#f9f9f9',
                        'paper_bgcolor': '#f9f9f9',
                    }
                }
            )
        ], style={'padding': '20px'})
        ])
    ], style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f0f2f5'
    })
], style={'backgroundColor': '#f0f2f5', 'padding': '20px'})

# Callbacks for Overview Tab Charts
@app.callback(
    [Output('customer-type-pie', 'figure'),
     Output('category-bar', 'figure')],
    [Input('customer-type-filter', 'value')]
)
def update_overview_charts(customer_type):
    # Filter data based on customer type
    filtered_df = df if customer_type is None else df[df['customer_type'] == customer_type]
    
    # Customer Type Pie Chart
    customer_type_fig = px.pie(
        df,
        names='customer_type',
        values='total_amount',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    customer_type_fig.update_traces(textposition='inside', textinfo='percent+label')
    
    # Category Performance Bar Chart
    category_fig = px.bar(
        filtered_df.groupby('category')['total_amount'].sum().reset_index(),
        x='category',
        y='total_amount',
        color='category',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    category_fig.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return customer_type_fig, category_fig

# Callbacks for Advanced Analytics Tab Charts
@app.callback(
    Output('time-series', 'figure'),
    [Input('customer-type-filter', 'value'),
     Input('time-filter', 'value')]
)
def update_advanced_charts(customer_type, time_period):
    # Filter data based on customer type
    filtered_df = df if customer_type is None else df[df['customer_type'] == customer_type]
    
    # Time Series Chart
    time_col = 'hour' if time_period == 'hour' else 'month' if time_period == 'month' else 'day_of_week'
    time_series_fig = px.line(
        filtered_df.groupby(time_col)['total_amount'].mean().reset_index(),
        x=time_col,
        y='total_amount',
        title=f'{customer_type}\'s average Sales by {time_period.title()}',
        color_discrete_sequence=['#3498db']
    )
    time_series_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return time_series_fig

# Add some global styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>E-commerce Analytics Dashboard</title>
        {%css%}
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f2f5;
            }
            .metric-box {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }
            
        </style>
    </head>
    <body>
        {%app_entry%}
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
'''

if __name__ == '__main__':
    app.run_server(debug=True)
