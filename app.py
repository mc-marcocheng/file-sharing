import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import numpy as np
import flask
from sympy import *


# server = flask.Flask(__name__)
# server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
# app = dash.Dash(__name__, server=server)
app = dash.Dash(__name__)

app.layout = html.Div([
    html.I("f(x)="),
    dcc.Input(id='expr', type='text', placeholder='x+1', debounce=True),
    html.I("  x1="),
    dcc.Input(id='slider', type='number', placeholder='0', value=0, min=-1000, max=1000, debounce=True),
    html.H3(id='iter'),
    dcc.Slider(id='slider2', value=1, min=1, max=10, step=1),
    dcc.Input(id='xleft', type='number', placeholder='x-axis lower lim', debounce=True, min=-1000),
    dcc.Input(id='xright', type='number', placeholder='x-axis upper lim', debounce=True, max=1000),
    dcc.Input(id='yleft', type='number', placeholder='y-axis lower lim', debounce=True, min=-1000),
    dcc.Input(id='yright', type='number', placeholder='y-axis upper lim', debounce=True, max=1000),
    dcc.Graph(id = 'live-graph', animate = True),
    html.H3(id='root')
])

@app.callback(
    [Output('live-graph', 'figure'), Output('root', 'children'), Output('iter', 'children')],
    [Input('slider', 'value'), Input('slider2', 'value'), Input('expr', 'value'), Input('xleft', 'value'), Input('xright', 'value'), Input('yleft', 'value'), Input('yright', 'value')]
)
def make_fig(cur_x, iter, expr, xl, xr, yl, yr):
    if not expr:
        expr = "x+1"
    fig = go.Figure()
    fig.update_layout(
        autosize=False,
        height=650,
        width=650,
        paper_bgcolor="White",
    )
    fig.update_layout(
        xaxis=dict(
            tickangle=45,
            title_font={"size": 20},
            title_standoff=10),
            )
    fig.update(layout_showlegend=True)
    if xl is None: xl = -5
    if xr is None: xr = 5
    if yl is None: yl = -10
    if yr is None: yr = 10
    def invalid_return(msg):
        return fig, msg, f'Number of iterations = {iter}'
    if xl>=xr or yl>=yr: return invalid_return("Invalid axis range")
    fig.update_yaxes(range=[yl, yr])
    fig.update_xaxes(range=[xl, xr])
    for i in ";'\"\\,!@#$%&_=`~":
        if i in expr: return invalid_return("Invalid input")
    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    saved = cur_x
    x = Symbol('x')
    for i in range(10): expr = expr.replace(str(i)+'x', str(i)+'*x')
    try:
        expr = eval(expr.replace('^', '**'))
    except:
        return invalid_return("Invalid input")
    def f(c):
        try:
            return np.array([float(N(expr.subs(x,i))) for i in c])
        except:
            return float(N(expr.subs(x,c)))
    def df(c):
        try:
            return np.array([float(N(expr.diff(x).subs(x,i))) for i in c])
        except:
            return float(N(expr.diff(x).subs(x,c)))
    try:
        fig.add_trace(go.Scatter(x=(xx := np.linspace(xl,xr,500)), y=f(xx), mode='lines', line=dict(color='Green'), name="f(x)"))
    except:
        return invalid_return("Cannot draw function")
    try:
        for i in range(iter):
            if f(saved) > .5:
                fig.add_trace(go.Scatter(x=[saved]*2, y=[0, f(saved)], mode='lines', line=dict(color=colors[i], dash='dash'), showlegend=False))
            fig.add_trace(go.Scatter(x=[saved], y=[f(saved)], mode='markers', line=dict(color=colors[i]), showlegend=False,
                                    marker=dict(
                                        color=colors[i],
                                        size=5,
                                        line=dict(color=colors[i], width=2)
                                    )))
            fig.add_trace(go.Scatter(x=xx, y=(df(saved))*(xx-saved)+f(saved), mode='lines', line=dict(color=colors[i]), name="Iteration "+str(i+1)))
            if df(saved) == 0:
                return invalid_return("Zero divison error")
            saved = f(saved)/(-df(saved))+saved
            fig.add_trace(go.Scatter(x=[saved], y=[0], mode='markers', line=dict(color=colors[i]), showlegend=False,
                                    marker=dict(
                                        color=colors[i],
                                        size=5,
                                        line=dict(color=colors[i], width=2)
                                    )))
    except:
        return invalid_return("Iteration failed")
    return fig, f'Estimated root: {saved}', f'Number of iterations = {iter}'

if __name__ == '__main__':
#     app.server.run(debug=True, threaded=True)
    app.run_server()
