import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load data
df = pd.read_csv('Financial Statements.csv')
df.columns = df.columns.str.strip()
df = df.dropna(subset=['Revenue', 'Net Income', 'Market Cap(in B USD)'])

# Colour palette
NEON_CYAN = '#00f5ff'
NEON_PINK = '#ff00ff'
NEON_YELLOW = '#ffff00'
NEON_GREEN = '#00ff88'
NEON_ORANGE = '#ff6b35'
BG_DARK = '#0a0a1a'
BG_CARD = '#0d0d2b'

app = dash.Dash(__name__)
server = app.server

# Layout
app.layout = html.Div(style={'backgroundColor': BG_DARK, 'fontFamily': 'Arial', 'padding': '20px', 'minHeight': '100vh'}, children=[

    # Header
    html.Div(style={'textAlign': 'center', 'marginBottom': '30px', 'borderBottom': f'1px solid {NEON_CYAN}', 'paddingBottom': '20px'}, children=[
        html.H1('Financial MIS Dashboard', style={'color': NEON_CYAN, 'fontSize': '2.8em', 'letterSpacing': '4px', 'margin': '0'}),
        html.P('Global Company Performance | 2009–2023 | Real 10-K Data', style={'color': '#888', 'fontSize': '1em', 'marginTop': '8px'}),
    ]),

    # Filters Row
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '25px', 'flexWrap': 'wrap'}, children=[
        html.Div(style={'flex': '1', 'minWidth': '200px'}, children=[
            html.Label('Filter by Year', style={'color': NEON_CYAN, 'fontSize': '0.85em', 'marginBottom': '5px', 'display': 'block'}),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': 'All Years', 'value': 'all'}] + [{'label': str(y), 'value': y} for y in sorted(df['Year'].unique())],
                value='all',
                style={'backgroundColor': BG_CARD, 'color': 'white', 'border': f'1px solid {NEON_CYAN}'},
                className='dash-dropdown'
            )
        ]),
        html.Div(style={'flex': '1', 'minWidth': '200px'}, children=[
            html.Label('Filter by Sector', style={'color': NEON_PINK, 'fontSize': '0.85em', 'marginBottom': '5px', 'display': 'block'}),
            dcc.Dropdown(
                id='sector-filter',
                options=[{'label': 'All Sectors', 'value': 'all'}] + [{'label': s, 'value': s} for s in sorted(df['Category'].dropna().unique())],
                value='all',
                style={'backgroundColor': BG_CARD, 'color': 'white', 'border': f'1px solid {NEON_PINK}'},
            )
        ]),
    ]),

    # KPI Cards
    html.Div(id='kpi-cards', style={'display': 'flex', 'gap': '15px', 'marginBottom': '25px', 'flexWrap': 'wrap'}),

    # Charts Row 1
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px', 'flexWrap': 'wrap'}, children=[
        html.Div(dcc.Graph(id='revenue-trend'), style={'flex': '2', 'minWidth': '300px', 'backgroundColor': BG_CARD, 'borderRadius': '12px', 'border': f'1px solid #1a1a3e'}),
        html.Div(dcc.Graph(id='sector-bar'), style={'flex': '1', 'minWidth': '300px', 'backgroundColor': BG_CARD, 'borderRadius': '12px', 'border': f'1px solid #1a1a3e'}),
    ]),

    # Charts Row 2
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px', 'flexWrap': 'wrap'}, children=[
        html.Div(dcc.Graph(id='top-companies'), style={'flex': '1', 'minWidth': '300px', 'backgroundColor': BG_CARD, 'borderRadius': '12px', 'border': f'1px solid #1a1a3e'}),
        html.Div(dcc.Graph(id='roe-scatter'), style={'flex': '1', 'minWidth': '300px', 'backgroundColor': BG_CARD, 'borderRadius': '12px', 'border': f'1px solid #1a1a3e'}),
    ]),

    # Footer
    html.Div(style={'textAlign': 'center', 'marginTop': '30px', 'color': '#444', 'fontSize': '0.8em', 'borderTop': '1px solid #1a1a3e', 'paddingTop': '15px'}, children=[
        html.P('Built by Jessica Mathew | Data Source: Kaggle — Financial Statements of Major Companies 2009–2023')
    ])
])


def filter_data(year, sector):
    filtered = df.copy()
    if year != 'all':
        filtered = filtered[filtered['Year'] == year]
    if sector != 'all':
        filtered = filtered[filtered['Category'] == sector]
    return filtered


@app.callback(
    Output('kpi-cards', 'children'),
    Output('revenue-trend', 'figure'),
    Output('sector-bar', 'figure'),
    Output('top-companies', 'figure'),
    Output('roe-scatter', 'figure'),
    Input('year-filter', 'value'),
    Input('sector-filter', 'value')
)
def update_dashboard(year, sector):
    filtered = filter_data(year, sector)

    # KPI Cards
    total_revenue = filtered['Revenue'].sum()
    avg_net_income = filtered['Net Income'].mean()
    avg_roe = filtered['ROE'].mean()
    avg_market_cap = filtered['Market Cap(in B USD)'].mean()

    def kpi_card(title, value, color):
        return html.Div(style={
            'backgroundColor': BG_CARD, 'border': f'1px solid {color}',
            'borderRadius': '12px', 'padding': '20px', 'flex': '1',
            'minWidth': '180px', 'textAlign': 'center',
            'boxShadow': f'0 0 15px {color}33'
        }, children=[
            html.P(title, style={'color': '#888', 'fontSize': '0.85em', 'margin': '0 0 8px 0'}),
            html.H2(value, style={'color': color, 'fontSize': '1.8em', 'margin': '0'})
        ])

    cards = [
        kpi_card('Total Revenue (M)', f'${total_revenue:,.0f}M', NEON_CYAN),
        kpi_card('Avg Net Income (M)', f'${avg_net_income:,.0f}M', NEON_PINK),
        kpi_card('Avg ROE (%)', f'{avg_roe:.1f}%', NEON_YELLOW),
        kpi_card('Avg Market Cap (B)', f'${avg_market_cap:.1f}B', NEON_GREEN),
    ]

    # Revenue Trend
    trend = filtered.groupby('Year')[['Revenue', 'Net Income']].mean().reset_index()
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=trend['Year'], y=trend['Revenue'], name='Revenue', line=dict(color=NEON_CYAN, width=2.5)))
    fig_trend.add_trace(go.Scatter(x=trend['Year'], y=trend['Net Income'], name='Net Income', line=dict(color=NEON_PINK, width=2.5)))
    fig_trend.update_layout(title='Revenue vs Net Income Trend', template='plotly_dark', paper_bgcolor=BG_CARD, plot_bgcolor=BG_CARD, font=dict(color='white'), legend=dict(bgcolor=BG_DARK))

    # Sector Bar
    sector_data = filtered.groupby('Category')['Revenue'].mean().reset_index().sort_values('Revenue', ascending=False)
    fig_sector = px.bar(sector_data, x='Category', y='Revenue', title='Avg Revenue by Sector', template='plotly_dark', color='Revenue', color_continuous_scale='Viridis')
    fig_sector.update_layout(paper_bgcolor=BG_CARD, plot_bgcolor=BG_CARD, font=dict(color='white'))

    # Top Companies
    top = filtered.groupby('Company')['Market Cap(in B USD)'].mean().reset_index().sort_values('Market Cap(in B USD)', ascending=True).tail(10)
    fig_top = px.bar(top, x='Market Cap(in B USD)', y='Company', orientation='h', title='Top 10 Companies by Market Cap', template='plotly_dark', color='Market Cap(in B USD)', color_continuous_scale='Plasma')
    fig_top.update_layout(paper_bgcolor=BG_CARD, plot_bgcolor=BG_CARD, font=dict(color='white'))

    # ROE vs ROA Scatter
    fig_scatter = px.scatter(filtered, x='ROA', y='ROE', color='Category', hover_name='Company', title='ROE vs ROA by Company', template='plotly_dark', size_max=15)
    fig_scatter.update_layout(paper_bgcolor=BG_CARD, plot_bgcolor=BG_CARD, font=dict(color='white'))

    return cards, fig_trend, fig_sector, fig_top, fig_scatter


if __name__ == '__main__':
    app.run(debug=True)