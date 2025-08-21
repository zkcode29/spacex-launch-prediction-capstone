import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import os
import requests
from datetime import datetime, timedelta
import numpy as np

# --- 1. Initialize  App ---
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
    ]
)
server = app.server

#  CSS Styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * { 
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            body { 
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                color: #2d3748;
                min-height: 100vh;
            }
            .dashboard-header {
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
                color: white;
                border-radius: 12px;
                padding: 32px;
                margin-bottom: 32px;
                box-shadow: 0 4px 20px rgba(30, 64, 175, 0.15);
            }
            .metric-card {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 24px;
                margin-bottom: 24px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .metric-value {
                font-size: 2rem;
                font-weight: 700;
                color: #1a202c;
                margin: 0;
            }
            .metric-label {
                font-size: 0.875rem;
                font-weight: 500;
                color: #718096;
                margin: 4px 0 0 0;
                text-transform: uppercase;
                letter-spacing: 0.025em;
            }
            .filter-container {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 24px;
                margin-bottom: 32px;
            }
            .chart-container {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 24px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .section-title {
                font-size: 1.125rem;
                font-weight: 600;
                color: #2d3748;
                margin-bottom: 16px;
            }
            .Select-control, .dropdown {
                border: 1px solid #d1d5db !important;
                border-radius: 6px !important;
                font-size: 14px !important;
            }
            .rc-slider-rail {
                background-color: #e2e8f0 !important;
            }
            .rc-slider-track {
                background-color: #4f46e5 !important;
            }
            .rc-slider-handle {
                border-color: #4f46e5 !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# --- 2. Data Loading ---
def load_and_prepare_data():
    """Load and prepare SpaceX data"""
    # Sample  data
    np.random.seed(42)
    
    # Realistic launch sites
    launch_sites = {
        'KSC-LC-39A': 'Kennedy Space Center LC-39A',
        'CCAFS-SLC-40': 'Cape Canaveral SLC-40', 
        'VAFB-SLC-4E': 'Vandenberg AFB SLC-4E',
        'CCAFS-SLC-37': 'Cape Canaveral SLC-37'
    }
    
    sample_data = {
        'class': np.random.choice([0, 1], size=150, p=[0.12, 0.88]),  
        'LaunchSite': np.random.choice(list(launch_sites.keys()), size=150),
        'PayloadMass': np.random.normal(8000, 3500, 150).clip(500, 22000),
        'Orbit': np.random.choice(['LEO', 'GTO', 'SSO', 'ISS', 'GEO', 'MEO'], 
                                 size=150, p=[0.4, 0.25, 0.15, 0.1, 0.05, 0.05]),
        'BoosterVersion': np.random.choice([
            'Falcon 9 Block 5', 'Falcon 9 v1.2', 'Falcon Heavy', 'Falcon 9 v1.1'
        ], size=150, p=[0.6, 0.25, 0.1, 0.05]),
        'Date': pd.date_range(start='2018-01-01', end='2024-12-31', periods=150),
        'Customer': np.random.choice([
            'NASA', 'SpaceX', 'Commercial Satellite', 'U.S. Military', 'International'
        ], size=150),
        'Mission': [f'Mission-{i:03d}' for i in range(1, 151)]
    }
    
    df = pd.DataFrame(sample_data)
    df['PayloadMass'] = df['PayloadMass'].astype(int)
    df['Launch Outcome'] = df['class'].apply(lambda x: 'Success' if x == 1 else 'Failure')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    
    return df, launch_sites

df, launchpad_map = load_and_prepare_data()

# Filter Options
site_options = [{'label': 'All Launch Sites', 'value': 'ALL'}] + \
               [{'label': name, 'value': site_id} for site_id, name in launchpad_map.items()]

booster_options = [{'label': 'All Booster Versions', 'value': 'ALL'}] + \
                  [{'label': booster, 'value': booster} for booster in sorted(df['BoosterVersion'].unique())]

orbit_options = [{'label': 'All Target Orbits', 'value': 'ALL'}] + \
                [{'label': orbit, 'value': orbit} for orbit in sorted(df['Orbit'].unique())]

# --- 3.  Layout ---
def create_metric_card(title, value, change=None):
    """Create professional metric card"""
    return html.Div([
        html.H2(value, className="metric-value"),
        html.P(title, className="metric-label"),
        html.P(change, style={'color': '#10b981', 'font-size': '0.75rem', 'margin': '8px 0 0 0'}) if change else None
    ], className="metric-card")

app.layout = dbc.Container([
    #  Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("SpaceX Launch Analytics", 
                       style={
                           'color': '#1a202c', 
                           'font-weight': '700', 
                           'font-size': '2.25rem',
                           'margin': '0'
                       }),
                html.P("Mission Performance Dashboard", 
                      style={
                          'color': '#718096', 
                          'font-size': '1rem',
                          'margin': '4px 0 0 0'
                      })
            ], className="dashboard-header")
        ], width=12)
    ]),
    
    # Key Metrics
    dbc.Row([
        dbc.Col([
            create_metric_card("Total Missions", f"{len(df):,}", "+12% vs last year")
        ], width=3),
        dbc.Col([
            create_metric_card("Success Rate", f"{df['class'].mean()*100:.1f}%", "+2.1% vs last year")
        ], width=3),
        dbc.Col([
            create_metric_card("Active Launch Sites", f"{df['LaunchSite'].nunique()}", "Across 2 states")
        ], width=3),
        dbc.Col([
            create_metric_card("Total Payload", f"{df['PayloadMass'].sum()/1000:.0f}t", "+45t vs last year")
        ], width=3)
    ]),
    
    # Filters Section
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("Filters", className="section-title"),
                
                dbc.Row([
                    dbc.Col([
                        html.Label("Launch Site", style={'font-weight': '500', 'margin-bottom': '8px', 'display': 'block'}),
                        dcc.Dropdown(
                            id='site-dropdown',
                            options=site_options,
                            value='ALL',
                            clearable=False,
                            style={'margin-bottom': '16px'}
                        )
                    ], width=3),
                    
                    dbc.Col([
                        html.Label("Booster Version", style={'font-weight': '500', 'margin-bottom': '8px', 'display': 'block'}),
                        dcc.Dropdown(
                            id='booster-dropdown',
                            options=booster_options,
                            value='ALL',
                            clearable=False,
                            style={'margin-bottom': '16px'}
                        )
                    ], width=3),
                    
                    dbc.Col([
                        html.Label("Target Orbit", style={'font-weight': '500', 'margin-bottom': '8px', 'display': 'block'}),
                        dcc.Dropdown(
                            id='orbit-dropdown',
                            options=orbit_options,
                            value='ALL',
                            clearable=False,
                            style={'margin-bottom': '16px'}
                        )
                    ], width=3),
                    
                    dbc.Col([
                        html.Label("Date Range", style={'font-weight': '500', 'margin-bottom': '8px', 'display': 'block'}),
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date=df['Date'].min(),
                            end_date=df['Date'].max(),
                            display_format='MMM DD, YYYY',
                            style={'width': '100%'}
                        )
                    ], width=3)
                ]),
                
                dbc.Row([
                    dbc.Col([
                        html.Label("Payload Mass Range (kg)", 
                                 style={'font-weight': '500', 'margin-bottom': '16px', 'display': 'block'}),
                        dcc.RangeSlider(
                            id='payload-slider',
                            min=0, max=25000, step=1000,
                            marks={i: f'{i/1000:.0f}t' for i in range(0, 26000, 5000)},
                            value=[df['PayloadMass'].min(), df['PayloadMass'].max()],
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], width=12)
                ])
            ], className="filter-container")
        ], width=12)
    ]),
    
    # Charts Row 1
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4("Mission Success Rate", className="section-title"),
                dcc.Graph(id='success-pie-chart', style={'height': '350px'})
            ], className="chart-container")
        ], width=4),
        
        dbc.Col([
            html.Div([
                html.H4("Launch Timeline", className="section-title"),
                dcc.Graph(id='timeline-chart', style={'height': '350px'})
            ], className="chart-container")
        ], width=8)
    ]),
    
    # Charts Row 2
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4("Payload Distribution by Orbit", className="section-title"),
                dcc.Graph(id='payload-scatter-plot', style={'height': '400px'})
            ], className="chart-container")
        ], width=8),
        
        dbc.Col([
            html.Div([
                html.H4("Launch Site Performance", className="section-title"),
                dcc.Graph(id='site-performance-chart', style={'height': '400px'})
            ], className="chart-container")
        ], width=4)
    ]),
    
    # Mission Table
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4("Recent Missions", className="section-title"),
                dash_table.DataTable(
                    id='mission-table',
                    columns=[
                        {"name": "Mission", "id": "Mission"},
                        {"name": "Date", "id": "Date"},
                        {"name": "Launch Site", "id": "LaunchSite_Name"},
                        {"name": "Booster", "id": "BoosterVersion"},
                        {"name": "Payload (kg)", "id": "PayloadMass", "type": "numeric"},
                        {"name": "Orbit", "id": "Orbit"},
                        {"name": "Status", "id": "Launch Outcome"}
                    ],
                    style_cell={
                        'textAlign': 'left',
                        'padding': '12px',
                        'font-family': 'Inter',
                        'font-size': '14px',
                        'border': 'none'
                    },
                    style_header={
                        'backgroundColor': '#f7fafc',
                        'fontWeight': '600',
                        'color': '#2d3748',
                        'border-bottom': '2px solid #e2e8f0'
                    },
                    style_data={
                        'backgroundColor': 'white',
                        'border-bottom': '1px solid #f1f5f9'
                    },
                    style_data_conditional=[
                        {
                            'if': {'filter_query': '{Launch Outcome} = Success'},
                            'backgroundColor': '#f0fdf4',
                            'color': '#166534'
                        },
                        {
                            'if': {'filter_query': '{Launch Outcome} = Failure'},
                            'backgroundColor': '#fef2f2',
                            'color': '#dc2626'
                        }
                    ],
                    page_size=15,
                    sort_action="native"
                )
            ], className="chart-container")
        ], width=12)
    ]),
    
    html.Hr(style={'margin': '40px 0', 'border': 'none', 'border-top': '1px solid #e2e8f0'}),
    html.P("SpaceX Launch Analytics Dashboard", 
           style={'text-align': 'center', 'color': '#9ca3af', 'margin': '20px 0'})
    
], fluid=True, style={'max-width': '1400px'})

# --- 4.  Chart Callbacks ---
@app.callback(
    [Output('success-pie-chart', 'figure'),
     Output('payload-scatter-plot', 'figure'),
     Output('timeline-chart', 'figure'),
     Output('site-performance-chart', 'figure'),
     Output('mission-table', 'data')],
    [Input('site-dropdown', 'value'),
     Input('booster-dropdown', 'value'),
     Input('orbit-dropdown', 'value'),
     Input('payload-slider', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_dashboard(selected_site, selected_booster, selected_orbit, 
                    payload_range, start_date, end_date):
    
    # Filter data
    filtered_df = df.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['Date'] >= start_date) & 
            (filtered_df['Date'] <= end_date)
        ]
    
    low, high = payload_range
    filtered_df = filtered_df[
        (filtered_df['PayloadMass'] >= low) & 
        (filtered_df['PayloadMass'] <= high)
    ]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['LaunchSite'] == selected_site]
    
    if selected_booster != 'ALL':
        filtered_df = filtered_df[filtered_df['BoosterVersion'] == selected_booster]
    
    if selected_orbit != 'ALL':
        filtered_df = filtered_df[filtered_df['Orbit'] == selected_orbit]
    
    # 1.  Pie Chart
    if not filtered_df.empty:
        success_counts = filtered_df['Launch Outcome'].value_counts()
        pie_fig = go.Figure(data=[go.Pie(
            labels=success_counts.index,
            values=success_counts.values,
            hole=.5,
            marker=dict(colors=['#10b981', '#ef4444'], line=dict(color='white', width=2)),
            textinfo='percent',
            textfont=dict(size=16, color='white'),
            showlegend=True
        )])
        
        pie_fig.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(t=20, b=20, l=20, r=20),
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05,
                font=dict(size=12)
            )
        )
    else:
        pie_fig = go.Figure()
        pie_fig.add_annotation(text="No data available", xref="paper", yref="paper",
                              x=0.5, y=0.5, showarrow=False, font=dict(size=16, color='#718096'))
        pie_fig.update_layout(paper_bgcolor='white', plot_bgcolor='white')
    
    # 2.  Scatter Plot
    scatter_fig = px.scatter(
        filtered_df, x='PayloadMass', y='Orbit', 
        color='Launch Outcome',
        size='PayloadMass',
        hover_data=['Mission', 'BoosterVersion'],
        color_discrete_map={'Success': '#10b981', 'Failure': '#ef4444'}
    )
    
    scatter_fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(t=20, b=60, l=60, r=20),
        xaxis=dict(title="Payload Mass (kg)", gridcolor='#f1f5f9'),
        yaxis=dict(title="Target Orbit", gridcolor='#f1f5f9'),
        legend=dict(title="Mission Outcome")
    )
    
    # 3. Timeline
    monthly_data = filtered_df.groupby([
        filtered_df['Date'].dt.to_period('M'), 'Launch Outcome'
    ]).size().unstack(fill_value=0)
    
    timeline_fig = go.Figure()
    
    if 'Success' in monthly_data.columns:
        timeline_fig.add_trace(go.Scatter(
            x=[str(p) for p in monthly_data.index],
            y=monthly_data['Success'],
            name='Successful',
            line=dict(color='#10b981', width=3),
            fill='tonexty'
        ))
    
    if 'Failure' in monthly_data.columns:
        timeline_fig.add_trace(go.Scatter(
            x=[str(p) for p in monthly_data.index],
            y=monthly_data['Failure'],
            name='Failed',
            line=dict(color='#ef4444', width=3)
        ))
    
    timeline_fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(t=20, b=60, l=60, r=20),
        xaxis=dict(title="Date", gridcolor='#f1f5f9'),
        yaxis=dict(title="Number of Launches", gridcolor='#f1f5f9'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # 4. Site Performance Chart
    site_performance = filtered_df.groupby('LaunchSite').agg({
        'class': ['count', 'mean']
    }).round(3)
    site_performance.columns = ['Total', 'Success_Rate']
    site_performance = site_performance.reset_index()
    site_performance['Site_Name'] = site_performance['LaunchSite'].map(launchpad_map)
    
    site_fig = px.bar(
        site_performance, x='Site_Name', y='Success_Rate',
        color='Total',
        color_continuous_scale=['#dbeafe', '#1d4ed8'],
        text='Success_Rate'
    )
    
    site_fig.update_traces(texttemplate='%{text:.1%}', textposition='outside')
    site_fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(t=20, b=80, l=60, r=20),
        xaxis=dict(title="Launch Site", gridcolor='#f1f5f9'),
        yaxis=dict(title="Success Rate", gridcolor='#f1f5f9', tickformat='.0%'),
        coloraxis_colorbar=dict(title="Total Launches")
    )
    
    # 5. Mission Table
    table_data = filtered_df.nlargest(15, 'Date').copy()
    table_data['LaunchSite_Name'] = table_data['LaunchSite'].map(launchpad_map)
    table_data['Date'] = table_data['Date'].dt.strftime('%b %d, %Y')
    
    return (pie_fig, scatter_fig, timeline_fig, site_fig, 
            table_data[['Mission', 'Date', 'LaunchSite_Name', 'BoosterVersion', 
                       'PayloadMass', 'Orbit', 'Launch Outcome']].to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)