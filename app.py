import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import numpy as np
import flask
import os
from random import randint


# server = flask.Flask(__name__)
# server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
# app = dash.Dash(__name__, server=server)
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3(id='cur'),
    dcc.Slider(id='slider', value=1, min=0, max=1, step=0.01),
    html.H3(id='iter'),
    dcc.Slider(id='slider2', value=1, min=1, max=10, step=1),
    dcc.Graph(id = 'live-graph', animate = True),
    dcc.Graph(id = 'live-graph2', animate = True),
    html.H3(id='root')
])

@app.callback(
    [Output('live-graph', 'figure'), Output('live-graph2', 'figure'), Output('root', 'children'), Output('cur', 'children'), Output('iter', 'children')],
    [Input('slider', 'value'), Input('slider2', 'value')]
)
def make_fig(cur_x, iter):
    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    saved = cur_x
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=(xx := np.linspace(0,1,500)), y=xx-np.cos(xx), mode='lines', line=dict(color='Green'), name="f(x)=x-cos(x)"))
    for i in range(iter):
        fig.add_trace(go.Scatter(x=[saved]*2, y=[0, saved-np.cos(saved)], mode='lines', line=dict(color=colors[i], dash='dash'), showlegend=False))
        fig.add_trace(go.Scatter(x=[saved], y=[saved-np.cos(saved)], mode='markers', line=dict(color=colors[i]), showlegend=False,
                                marker=dict(
                                    color=colors[i],
                                    size=5,
                                    line=dict(color=colors[i], width=2)
                                )))
        fig.add_trace(go.Scatter(x=xx, y=(1+np.sin(saved))*(xx-saved)+saved-np.cos(saved), mode='lines', line=dict(color=colors[i]), name="Iteration "+str(i+1)))
        saved = (saved-np.cos(saved))/(-1-np.sin(saved))+saved
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
    fig.update_yaxes(range=[-1, .5])
    fig.update_xaxes(range=[0, 1])

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=(xx := np.linspace(0,1,500)), y=xx, mode='lines', line=dict(color=colors[7]), name="g(x)=x"))
    fig2.add_trace(go.Scatter(x=(xx := np.linspace(0,1,500)), y=np.cos(xx), mode='lines', line=dict(color=colors[8]), name="h(x)=cos(x)"))
    fig2.add_trace(go.Scatter(x=[saved]*2, y=[-100, 100], mode='lines', line=dict(color=colors[9], dash='dash'), showlegend=False))
    fig2.add_trace(go.Scatter(x=[saved], y=[saved], mode='markers', line=dict(color=colors[9]), showlegend=False,
                                marker=dict(
                                    color=colors[9],
                                    size=5,
                                    line=dict(color=colors[9], width=2)
                                )))
    fig2.add_trace(go.Scatter(x=[saved], y=[np.cos(saved)], mode='markers', line=dict(color=colors[9]), showlegend=False,
                                marker=dict(
                                    color=colors[9],
                                    size=5,
                                    line=dict(color=colors[9], width=2)
                                )))
    fig2.update_layout(
        autosize=False,
        height=650,
        width=650,
        paper_bgcolor="White",
        )

    fig2.update_layout(
        xaxis=dict(
            tickangle=45,
            title_font={"size": 20},
            title_standoff=10),
            )
    fig2.update(layout_showlegend=True)
    fig2.update_yaxes(range=[0, 1])
    fig2.update_xaxes(range=[0, 1])

    return fig, fig2, f'x{iter+1}={saved:.9g}', f'x1={cur_x}', f'Number of iterations = {iter}'

if __name__ == '__main__':
#     app.server.run(debug=True, threaded=True)
    app.run_server()
