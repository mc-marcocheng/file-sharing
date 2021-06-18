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
    dcc.Slider(id='slider', value=1.5, min=1, max=2, step=0.01),
    html.H3(id='iter'),
    dcc.Slider(id='slider2', value=1, min=1, max=10, step=1),
    dcc.Graph(id = 'live-graph', animate = True),
    html.H3(id='root')
])

@app.callback(
    [Output('live-graph', 'figure'), Output('root', 'children'), Output('cur', 'children'), Output('iter', 'children')],
    [Input('slider', 'value'), Input('slider2', 'value')]
)
def make_fig(cur_x, iter):
    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    saved = cur_x
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=(xx := np.linspace(1,2,500)), y=xx**3-xx-1, mode='lines', line=dict(color='Green'), name="f(x)=x^3-x-1"))
    for i in range(iter):
        fig.add_trace(go.Scatter(x=[saved]*2, y=[0, saved**3-saved-1], mode='lines', line=dict(color=colors[i], dash='dash'), showlegend=False))
        fig.add_trace(go.Scatter(x=[saved], y=[saved**3-saved-1], mode='markers', line=dict(color=colors[i]), showlegend=False,
                                marker=dict(
                                    color=colors[i],
                                    size=5,
                                    line=dict(color=colors[i], width=2)
                                )))
        fig.add_trace(go.Scatter(x=xx, y=(3*saved**2-1)*(xx-saved)+saved**3-saved-1, mode='lines', line=dict(color=colors[i]), name="Iteration "+str(i+1)))
        saved = (saved**3-saved-1)/(1-3*saved**2)+saved
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
    fig.update_yaxes(range=[-1, 5])
    fig.update_xaxes(range=[1, 2])

    return fig, f'x{iter+1}={saved:.9g}', f'x1={cur_x}', f'Number of iterations = {iter}'

if __name__ == '__main__':
#     app.server.run(debug=True, threaded=True)
    app.run_server()



server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)
# app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3(id='cur'),
    dcc.Slider(id='slider', value=1, min=0, max=2, step=0.01),
    html.H3(id='iter'),
    dcc.Slider(id='slider2', value=1, min=1, max=10, step=1),
    dcc.Graph(id = 'live-graph', animate = True),
    html.H3(id='root')
])

@app.callback(
    [Output('live-graph', 'figure'), Output('root', 'children'), Output('cur', 'children'), Output('iter', 'children')],
    [Input('slider', 'value'), Input('slider2', 'value')]
)
def make_fig(cur_x, iter):
    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    saved = cur_x
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=(xx := np.linspace(0,2,500)), y=(xx-1)**2, mode='lines', line=dict(color='Green'), name="f(x)=(x-1)^2"))
    for i in range(iter):
        if saved < .9 or saved > 1.1:
            fig.add_trace(go.Scatter(x=[saved]*2, y=[0, (saved-1)**2], mode='lines', line=dict(color=colors[i], dash='dash'), showlegend=False))
        fig.add_trace(go.Scatter(x=[saved], y=[(saved-1)**2], mode='markers', line=dict(color=colors[i]), showlegend=False,
                                marker=dict(
                                    color=colors[i],
                                    size=5,
                                    line=dict(color=colors[i], width=2)
                                )))
        fig.add_trace(go.Scatter(x=xx, y=(2*saved-2)*(xx-saved)+(saved-1)**2, mode='lines', line=dict(color=colors[i]), name="Iteration "+str(i+1)))
        saved = 1 if saved==1 else (saved-1)**2/(2-2*saved)+saved
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
    fig.update_yaxes(range=[-0.5, 1])
    fig.update_xaxes(range=[0, 2])

    return fig, f'Estimated root: {saved:.2f}', f'x1={cur_x}', f'Number of iterations = {iter}'

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
    # app.run_server()
