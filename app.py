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
    html.H3(id='cur'),
    dcc.Slider(id='slider', value=1, min=0, max=2, step=0.01),
    dcc.Graph(id = 'live-graph', animate = True),
    html.H3(id='root')
])

@app.callback(
    [Output('live-graph', 'figure'), Output('root', 'children'), Output('cur', 'children')],
    Input('slider', 'value')
)
def make_fig(cur_x):
    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    saved = cur_x
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=(xx := np.linspace(0,2,500)), y=(xx-1)**2+1, mode='lines', line=dict(color='Green'), name="f(x)=(x-1)^2+1"))
    fig.add_trace(go.Scatter(x=[saved]*2, y=[0, (saved-1)**2+1], mode='lines', line=dict(color=colors[0], dash='dash'), showlegend=False))
    fig.add_trace(go.Scatter(x=[saved], y=[(saved-1)**2+1], mode='markers', line=dict(color=colors[0]), showlegend=False,
                            marker=dict(
                                color=colors[0],
                                size=5,
                                line=dict(color=colors[0], width=2)
                            )))
    fig.add_trace(go.Scatter(x=xx, y=(2*saved-2)*(xx-saved)+(saved-1)**2+1, mode='lines', line=dict(color=colors[0]), name="Iteration 1"))

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
    fig.update_yaxes(range=[-0.1, 2])
    fig.update_xaxes(range=[0, 2])

    if saved == 1:
        return fig, f'Intersection with x-axis: x=???', f'x1={cur_x}'
    saved = ((saved-1)**2+1)/(2-2*saved)+saved
    fig.add_trace(go.Scatter(x=[saved], y=[0], mode='markers', line=dict(color=colors[0]), showlegend=False,
                            marker=dict(
                                color=colors[0],
                                size=5,
                                line=dict(color=colors[0], width=2)
                            )))
    return fig, f'Intersection with x-axis: x={saved:.2f}', f'x1={cur_x}'

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
    # app.run_server()
