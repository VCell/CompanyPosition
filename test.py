import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=2,
                    specs=[[{"secondary_y": True}, {"secondary_y": True}],
                           [{"secondary_y": True}, {"secondary_y": True}]])

# Top left
fig.add_trace(
    go.Scatter(x=[1, 2, 3], y=[2, 52, 62], name="yaxis data"),
    row=1, col=1, secondary_y=False)

fig.add_trace(
    go.Scatter(x=[1, 2, 3], y=[40, 50, 60], name="yaxis2 data"),
    row=1, col=1, secondary_y=True,
)

# Top right
fig.add_trace(
    go.Scatter(x=[1, 2, 3], y=[2, 52, 62], name="yaxis3 data"),
    row=1, col=2, secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=[1, 2, 3], y=[40, 50, 60], name="yaxis4 data"),
    row=1, col=2, secondary_y=True,
)

# Bottom left
fig.add_trace(
    go.Scatter(x=[1, 2, 3], y=[2, 52, 62], name="yaxis5 data"),
    row=2, col=1, secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=[1, 2, 3], y=[40, 50, 60], name="yaxis6 data"),
    row=2, col=1, secondary_y=True,
)

# Bottom right
fig.add_trace(
    go.Scatter(x=[1, 2, 3], y=[2, 52, 62], name="yaxis7 data"),
    row=2, col=2, secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=[1, 2, 3], y=[40, 50, 60], name="yaxis8 data"),
    row=2, col=2, secondary_y=True,
)

fig.show()