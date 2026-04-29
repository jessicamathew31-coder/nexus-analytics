import dash
from dash import html, Input, Output, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('Financial Statements.csv')
df.columns = df.columns.str.strip()
df = df.dropna(subset=['Revenue', 'Net Income', 'Market Cap(in B USD)'])

app = dash.Dash(__name__)
server = app.server

years = ['all'] + [str(y) for y in sorted(df['Year'].unique())]
sectors = ['all'] + sorted(df['Category'].dropna().unique().tolist())

app.index_string = '''<!DOCTYPE html>
<html>
<head>
{%metas%}
<title>Nexus Analytics</title>
{%favicon%}
{%css%}
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0d0015;font-family:"Segoe UI",Arial,sans-serif;overflow-x:hidden;cursor:none;}
#cd{width:8px;height:8px;background:#ff6b35;border-radius:50%;position:fixed;pointer-events:none;z-index:99999;transform:translate(-50%,-50%);box-shadow:0 0 10px #ff6b35,0 0 20px #ff6b35;}
#cr{width:36px;height:36px;border:2px solid rgba(255,107,53,0.6);border-radius:50%;position:fixed;pointer-events:none;z-index:99998;transform:translate(-50%,-50%);transition:all 0.12s ease;}
.gp{position:fixed;border-radius:50%;pointer-events:none;z-index:99997;animation:pf 1s ease-out forwards;}
@keyframes pf{0%{opacity:0.8;transform:translate(-50%,-50%) scale(1);}100%{opacity:0;transform:translate(-50%,-50%) scale(3);}}
.aurora{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;overflow:hidden;pointer-events:none;}
.ab{position:absolute;border-radius:50%;filter:blur(90px);opacity:0.2;animation:fl 10s ease-in-out infinite;}
.b1{width:700px;height:700px;background:radial-gradient(circle,#6600ff,transparent);top:-300px;left:-200px;}
.b2{width:500px;height:500px;background:radial-gradient(circle,#ff6b35,transparent);top:50%;right:-200px;animation-delay:3s;}
.b3{width:450px;height:450px;background:radial-gradient(circle,#00f0ff,transparent);bottom:-150px;left:25%;animation-delay:5s;}
.b4{width:300px;height:300px;background:radial-gradient(circle,#ff006e,transparent);top:30%;left:50%;animation-delay:2s;}
@keyframes fl{0%,100%{transform:translateY(0px) scale(1);}50%{transform:translateY(-50px) scale(1.08);}}
.mc{position:relative;z-index:1;padding:30px;min-height:100vh;}
.gc{background:rgba(255,255,255,0.03);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.07);border-radius:20px;transition:all 0.4s ease;}
.gc:hover{transform:translateY(-6px);background:rgba(255,255,255,0.06);border-color:rgba(255,107,53,0.4);box-shadow:0 25px 80px rgba(255,107,53,0.15);}
.kc{background:rgba(255,255,255,0.03);backdrop-filter:blur(20px);border-radius:20px;padding:25px;text-align:center;transition:all 0.4s ease;}
.kc:hover{transform:translateY(-10px) scale(1.03);}
.hg{background:rgba(13,0,21,0.8);backdrop-filter:blur(40px);border-bottom:1px solid rgba(255,107,53,0.15);padding:20px 30px;margin:-30px -30px 30px -30px;position:sticky;top:0;z-index:100;}
.fi{animation:fiu 0.9s ease forwards;opacity:0;}
.f1{animation-delay:0.1s;}.f2{animation-delay:0.25s;}.f3{animation-delay:0.4s;}.f4{animation-delay:0.55s;}.f5{animation-delay:0.7s;}
@keyframes fiu{from{opacity:0;transform:translateY(40px);}to{opacity:1;transform:translateY(0);}}
.pill-group{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;padding:4px 0;}
.pill{padding:6px 16px;border-radius:20px;border:1px solid rgba(255,107,53,0.3);background:rgba(255,107,53,0.05);color:#666;font-size:0.78em;letter-spacing:1px;cursor:none;transition:all 0.2s ease;display:inline-block;margin:3px;}
.pill:hover{border-color:rgba(255,107,53,0.8);color:#ff6b35;background:rgba(255,107,53,0.1);transform:translateY(-2px);}
.pill-active{border-color:#ff6b35 !important;color:#ff6b35 !important;background:rgba(255,107,53,0.15) !important;box-shadow:0 0 15px rgba(255,107,53,0.2) !important;}
.pill-sector{border-color:rgba(191,0,255,0.3) !important;background:rgba(191,0,255,0.05) !important;}
.pill-sector:hover{border-color:rgba(191,0,255,0.8) !important;color:#bf00ff !important;background:rgba(191,0,255,0.1) !important;}
.pill-sector-active{border-color:#bf00ff !important;color:#bf00ff !important;background:rgba(191,0,255,0.15) !important;box-shadow:0 0 15px rgba(191,0,255,0.2) !important;}
@keyframes np{0%,100%{text-shadow:0 0 20px #ff6b35,0 0 40px #ff6b35aa;}50%{text-shadow:0 0 40px #ff6b35,0 0 80px #ff6b35aa;}}
</style>
</head>
<body>
<div id="cd"></div>
<div id="cr"></div>
<div class="aurora">
<div class="ab b1"></div><div class="ab b2"></div><div class="ab b3"></div><div class="ab b4"></div>
</div>
{%app_entry%}
<footer>{%config%}{%scripts%}{%renderer%}</footer>
<script>
const dot=document.getElementById("cd"),ring=document.getElementById("cr");
let lpt=0;
document.addEventListener("mousemove",e=>{
dot.style.left=e.clientX+"px";dot.style.top=e.clientY+"px";
setTimeout(()=>{ring.style.left=e.clientX+"px";ring.style.top=e.clientY+"px";},60);
const now=Date.now();
if(now-lpt>40){lpt=now;const p=document.createElement("div");p.className="gp";
const s=Math.random()*8+4;const cols=["#ff6b35","#bf00ff","#00f0ff","#ff006e"];const col=cols[Math.floor(Math.random()*cols.length)];
p.style.cssText="width:"+s+"px;height:"+s+"px;background:"+col+";left:"+e.clientX+"px;top:"+e.clientY+"px;box-shadow:0 0 "+(s*2)+"px "+col+";";
document.body.appendChild(p);setTimeout(()=>p.remove(),1000);}
});
document.addEventListener("mousedown",()=>{dot.style.transform="translate(-50%,-50%) scale(3)";ring.style.transform="translate(-50%,-50%) scale(0.5)";});
document.addEventListener("mouseup",()=>{dot.style.transform="translate(-50%,-50%) scale(1)";ring.style.transform="translate(-50%,-50%) scale(1)";});
</script>
</body>
</html>'''

app.layout = html.Div(className='mc', children=[
    html.Div(className='hg fi f1', children=[
        html.Div(style={'display':'flex','justifyContent':'space-between','alignItems':'center'}, children=[
            html.Div(children=[
                html.H1('NEXUS ANALYTICS', style={'color':'#ff6b35','fontSize':'2.4em','letterSpacing':'6px','animation':'np 3s ease-in-out infinite'}),
                html.P('Global Corporate Intelligence | 2009-2023 | Fortune 500 10-K Data', style={'color':'#666','fontSize':'0.85em','marginTop':'6px','letterSpacing':'1px'}),
            ]),
            html.Div(style={'display':'flex','gap':'12px','alignItems':'center'}, children=[
                html.Div(style={'width':'8px','height':'8px','background':'#39ff14','borderRadius':'50%','boxShadow':'0 0 12px #39ff14'}),
                html.Span('LIVE', style={'color':'#39ff14','fontSize':'0.7em','letterSpacing':'3px'}),
            ])
        ])
    ]),

    html.Div(style={'marginBottom':'25px'}, className='fi f2', children=[
        html.Label('YEAR', style={'color':'#ff6b35','fontSize':'0.75em','marginBottom':'8px','display':'block','letterSpacing':'3px'}),
        html.Div(id='year-pills', className='pill-group', children=[
            html.Span('ALL', id={'type':'year-pill','index':'all'}, className='pill pill-active', n_clicks=0),
        ] + [
            html.Span(str(y), id={'type':'year-pill','index':str(y)}, className='pill', n_clicks=0)
            for y in sorted(df['Year'].unique())
        ]),
        dcc.Store(id='year-filter', data='all'),
    ]),

    html.Div(style={'marginBottom':'25px'}, className='fi f2', children=[
        html.Label('SECTOR', style={'color':'#bf00ff','fontSize':'0.75em','marginBottom':'8px','display':'block','letterSpacing':'3px'}),
        html.Div(id='sector-pills', className='pill-group', children=[
            html.Span('ALL', id={'type':'sector-pill','index':'all'}, className='pill pill-sector pill-sector-active', n_clicks=0),
        ] + [
            html.Span(s, id={'type':'sector-pill','index':s}, className='pill pill-sector', n_clicks=0)
            for s in sorted(df['Category'].dropna().unique())
        ]),
        dcc.Store(id='sector-filter', data='all'),
    ]),

    html.Div(id='kpi-cards', style={'display':'flex','gap':'15px','marginBottom':'25px','flexWrap':'wrap'}, className='fi f3'),

    html.Div(style={'display':'flex','gap':'20px','marginBottom':'20px','flexWrap':'wrap'}, className='fi f4', children=[
        html.Div(dcc.Graph(id='revenue-trend', config={'displayModeBar':False}), className='gc', style={'flex':'2','minWidth':'300px','padding':'10px'}),
        html.Div(dcc.Graph(id='sector-bar', config={'displayModeBar':False}), className='gc', style={'flex':'1','minWidth':'300px','padding':'10px'}),
    ]),

    html.Div(style={'display':'flex','gap':'20px','marginBottom':'30px','flexWrap':'wrap'}, className='fi f5', children=[
        html.Div(dcc.Graph(id='top-companies', config={'displayModeBar':False}), className='gc', style={'flex':'1','minWidth':'300px','padding':'10px'}),
        html.Div(dcc.Graph(id='roe-scatter', config={'displayModeBar':False}), className='gc', style={'flex':'1','minWidth':'300px','padding':'10px'}),
    ]),

    html.Div(style={'textAlign':'center','color':'#2a2a2a','fontSize':'0.72em','letterSpacing':'2px','paddingTop':'15px','borderTop':'1px solid rgba(255,255,255,0.03)'}, children=[
        html.P('NEXUS ANALYTICS - BUILT BY JESSICA MATHEW | MBA FINANCE & TECHNOLOGY | DATA: KAGGLE 2009-2023')
    ])
])

from dash import ctx, ALL
import json

@app.callback(
    Output('year-filter', 'data'),
    Output('year-pills', 'children'),
    Input({'type':'year-pill','index':ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def update_year(n_clicks):
    triggered = ctx.triggered_id
    if not triggered:
        raise dash.exceptions.PreventUpdate
    selected = triggered['index']
    children = [
        html.Span('ALL', id={'type':'year-pill','index':'all'}, className='pill pill-active' if selected=='all' else 'pill', n_clicks=0),
    ] + [
        html.Span(str(y), id={'type':'year-pill','index':str(y)}, className='pill pill-active' if str(y)==selected else 'pill', n_clicks=0)
        for y in sorted(df['Year'].unique())
    ]
    return selected, children

@app.callback(
    Output('sector-filter', 'data'),
    Output('sector-pills', 'children'),
    Input({'type':'sector-pill','index':ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def update_sector(n_clicks):
    triggered = ctx.triggered_id
    if not triggered:
        raise dash.exceptions.PreventUpdate
    selected = triggered['index']
    children = [
        html.Span('ALL', id={'type':'sector-pill','index':'all'}, className='pill pill-sector pill-sector-active' if selected=='all' else 'pill pill-sector', n_clicks=0),
    ] + [
        html.Span(s, id={'type':'sector-pill','index':s}, className='pill pill-sector pill-sector-active' if s==selected else 'pill pill-sector', n_clicks=0)
        for s in sorted(df['Category'].dropna().unique())
    ]
    return selected, children

@app.callback(
    Output('kpi-cards','children'),
    Output('revenue-trend','figure'),
    Output('sector-bar','figure'),
    Output('top-companies','figure'),
    Output('roe-scatter','figure'),
    Input('year-filter','data'),
    Input('sector-filter','data')
)
def update_dashboard(year, sector):
    filtered = df.copy()
    if year and year != 'all':
        filtered = filtered[filtered['Year'] == int(year)]
    if sector and sector != 'all':
        filtered = filtered[filtered['Category'] == sector]

    total_revenue = filtered['Revenue'].sum()
    avg_net_income = filtered['Net Income'].mean()
    avg_roe = filtered['ROE'].mean()
    avg_market_cap = filtered['Market Cap(in B USD)'].mean()

    def kpi_card(title, value, color, icon):
        return html.Div(className='kc', style={'border':f'1px solid {color}33','boxShadow':f'0 0 40px {color}11','flex':'1','minWidth':'180px'}, children=[
            html.Div(icon, style={'fontSize':'1.6em','marginBottom':'10px'}),
            html.P(title, style={'color':'#555','fontSize':'0.72em','letterSpacing':'2px','marginBottom':'10px'}),
            html.H2(value, style={'color':color,'fontSize':'1.7em','textShadow':f'0 0 25px {color}88','fontWeight':'700'})
        ])

    cards = [
        kpi_card('TOTAL REVENUE', f'${total_revenue:,.0f}M', '#00f0ff', '💰'),
        kpi_card('AVG NET INCOME', f'${avg_net_income:,.0f}M', '#bf00ff', '📈'),
        kpi_card('AVG ROE', f'{avg_roe:.1f}%', '#ff6b35', '🎯'),
        kpi_card('AVG MARKET CAP', f'${avg_market_cap:.1f}B', '#39ff14', '🏦'),
    ]

    BG = 'rgba(0,0,0,0)'
    PBG = 'rgba(255,255,255,0.015)'

    trend = filtered.groupby('Year')[['Revenue','Net Income']].mean().reset_index()
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=trend['Year'],y=trend['Revenue'],name='Revenue',line=dict(color='#00f0ff',width=3),fill='tozeroy',fillcolor='rgba(0,240,255,0.04)'))
    fig_trend.add_trace(go.Scatter(x=trend['Year'],y=trend['Net Income'],name='Net Income',line=dict(color='#bf00ff',width=3),fill='tozeroy',fillcolor='rgba(191,0,255,0.04)'))
    fig_trend.update_layout(title=dict(text='Revenue vs Net Income Trend',font=dict(color='#aaa',size=13)),template='plotly_dark',paper_bgcolor=BG,plot_bgcolor=PBG,font=dict(color='#666'),legend=dict(bgcolor='rgba(0,0,0,0.4)',bordercolor='#222'),margin=dict(t=50,b=30,l=30,r=30))

    sd = filtered.groupby('Category')['Revenue'].mean().reset_index().sort_values('Revenue',ascending=False)
    fig_sector = px.bar(sd,x='Category',y='Revenue',title='Avg Revenue by Sector',template='plotly_dark',color='Revenue',color_continuous_scale=[[0,'#6600ff'],[0.5,'#ff6b35'],[1,'#00f0ff']])
    fig_sector.update_layout(paper_bgcolor=BG,plot_bgcolor=PBG,font=dict(color='#666'),title_font=dict(color='#aaa',size=13),margin=dict(t=50,b=30,l=30,r=30))

    top = filtered.groupby('Company')['Market Cap(in B USD)'].mean().reset_index().sort_values('Market Cap(in B USD)',ascending=True).tail(10)
    fig_top = px.bar(top,x='Market Cap(in B USD)',y='Company',orientation='h',title='Top 10 by Market Cap',template='plotly_dark',color='Market Cap(in B USD)',color_continuous_scale=[[0,'#6600ff'],[0.5,'#bf00ff'],[1,'#ff6b35']])
    fig_top.update_layout(paper_bgcolor=BG,plot_bgcolor=PBG,font=dict(color='#666'),title_font=dict(color='#aaa',size=13),margin=dict(t=50,b=30,l=10,r=30))

    fig_scatter = px.scatter(filtered,x='ROA',y='ROE',color='Category',hover_name='Company',title='ROE vs ROA Analysis',template='plotly_dark',color_discrete_sequence=['#ff6b35','#bf00ff','#00f0ff','#39ff14','#ff006e','#ffff00'])
    fig_scatter.update_traces(marker=dict(size=9,opacity=0.85))
    fig_scatter.update_layout(paper_bgcolor=BG,plot_bgcolor=PBG,font=dict(color='#666'),title_font=dict(color='#aaa',size=13),legend=dict(bgcolor='rgba(0,0,0,0.4)'),margin=dict(t=50,b=30,l=30,r=30))

    return cards, fig_trend, fig_sector, fig_top, fig_scatter

if __name__ == '__main__':
    app.run(debug=True)
