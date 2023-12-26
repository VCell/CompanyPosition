#import plotly.plotly
import pandas as pd

import plotly.offline as po
# init_notebook_mode(connected=True) 

import plotly.graph_objs as go
import numpy as np
N = 1000
random_x = np.random.randn(N)
random_y = np.random.randn(N)
 
# # 构造trace，绘制散点图
# trace = go.Scatter(
#  x = random_x,
#  y = random_y,
#  mode = 'markers'
# )
# data = [trace]
# layout = go.Layout(title='测试',
#  titlefont={
#  'size':20,
#   'color':'#9ed900'
#  })
# fig = go.Figure(data=data,layout=layout)
# # fig = dict(data=data,layout=layout)
# # po.iplot(fig)
# po.plot(fig, filename='filename.html')

import plotly.graph_objs as go
import pandas as pd

# 创建数据
df = pd.DataFrame({'x': [1, 2, 3, 4, 5],
                   'y1': [10, 22, 28, 25, 30],
                   'y2': [1000, 2000, 3000, 2000, 1000]})

# 创建Trace1
trace1 = go.Scatter(x=df['x'],
                    y=df['y1'],
                    name='y1')

# 创建Trace2
trace2 = go.Scatter(x=df['x'],
                    y=df['y2'],
                    name='y2',
                    yaxis='y2')

# 创建Layout
layout = go.Layout(title='Plotly: Dual Y-Axis Example',
                   yaxis=dict(title='y1'),
                   yaxis2=dict(title='y2', overlaying='y', side='right')
                   )

# 组合Trace并绘制
data = [trace1, trace2]
fig = go.Figure(data=data, layout=layout)
fig.show()