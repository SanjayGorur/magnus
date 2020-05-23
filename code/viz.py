from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.io as io


def make_plot(white_moves, black_moves):
    fig = make_subplots(rows=1, cols=2, 
                        specs=[[{'type': 'domain'}, {'type': 'domain'}]],
                        subplot_titles=('White', 'Black'))
    
    fig.add_trace(go.Sunburst(
        name='White',
        ids=white_moves['ids'],
        labels=white_moves['labels'],
        parents=white_moves['parents'],
        values=white_moves['values'],
        branchvalues="total",
        opacity=1,
        marker={'colors':white_moves['color'], 'line':{'color':'#000200'}},
        hoverinfo='label+text+value+name+current path'
        ), 
        row=1, col=1)
    
    fig.add_trace(go.Sunburst(
        name='Black',
        ids=black_moves['ids'],
        labels=black_moves['labels'],
        parents=black_moves['parents'],
        values=black_moves['values'],
        branchvalues="total",
        opacity=1,
        marker={'colors':black_moves['color'], 'line':{'color':'#000200'}},
        hoverinfo='label+text+value+name+current path'
        ),
        row=1, col=2)
    
    fig.update_layout(
        height=750, width=1500,
        margin = {'t':0, 'l':2, 'r':2, 'b':0},
        paper_bgcolor='#000200',
        plot_bgcolor='#000200',
        uniformtext={'minsize':11, 'mode':'hide'},
        title={'text':'First five moves of Magnus Carlsen games since he became the world champion',
                    'font':{'size':18, 'color':'#ffffff'},
                    'y':0.98,
                    'x':0.5}
        )
    
    return fig


def write_fig(fig):
    io.orca.config.executable = '/home/musatov/Applications/orca.AppImage'
    fig.write_image('fig.svg')
    