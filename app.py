import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import numpy as np
import flask
import os
from random import randint


server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)
# app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3(id='a-val'),
    dcc.Slider(id='slider-a', value=1, min=0.1, max=10, step=0.1),
    html.H3(id='cur'),
    dcc.Slider(id='slider', value=2, min=0.1, max=4, step=0.1),
    html.H3(id='iter'),
    dcc.Slider(id='slider2', value=1, min=1, max=10, step=1),
    dcc.Graph(id = 'live-graph', animate = True),
    html.H3(id='root')
])

@app.callback(
    [Output('live-graph', 'figure'), Output('root', 'children'), Output('cur', 'children'), Output('iter', 'children'), Output('a-val', 'children')],
    [Input('slider', 'value'), Input('slider2', 'value'), Input('slider-a', 'value')]
)
def make_fig(cur_x, iter, a):
    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    saved = cur_x
    f = lambda x: x**2-a
    df = lambda x: 2*x
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=(xx := np.linspace(0,4,500)), y=f(xx), mode='lines', line=dict(color='Green'), name="f(x)=x^2-"+str(a)))
    for i in range(iter):
        if saved < np.sqrt(a) - .1 or saved > np.sqrt(a) + .1:
            fig.add_trace(go.Scatter(x=[saved]*2, y=[0, f(saved)], mode='lines', line=dict(color=colors[i], dash='dash'), showlegend=False))
        fig.add_trace(go.Scatter(x=[saved], y=[f(saved)], mode='markers', line=dict(color=colors[i]), showlegend=False,
                                marker=dict(
                                    color=colors[i],
                                    size=5,
                                    line=dict(color=colors[i], width=2)
                                )))
        fig.add_trace(go.Scatter(x=xx, y=(df(saved))*(xx-saved)+f(saved), mode='lines', line=dict(color=colors[i]), name="Iteration "+str(i+1)))
        saved = 4 if saved == 4 else f(saved)/(-df(saved))+saved
        fig.add_trace(go.Scatter(x=[saved], y=[0], mode='markers', line=dict(color=colors[i]), showlegend=False,
                                marker=dict(
                                    color=colors[i],
                                    size=5,
                                    line=dict(color=colors[i], width=2)
                                )))

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
    fig.update_yaxes(range=[-10, 10])
    fig.update_xaxes(range=[0, 4])

    return fig, f'Estimated root: {saved:.2f}', f'x1={cur_x}', f'Number of iterations = {iter}', f'{a=}'

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
    # app.run_server()
