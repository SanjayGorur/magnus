from data_processing_funs import parse_data, preprocess_data
import plotly.graph_objects as go
from plotly.offline import plot
from viz import write_fig
from numpy import round


with open('../data/carlsen.pgn', 'r') as f:
    text = f.read()

data = parse_data(text)
data = preprocess_data(data)


# prepare data
results = data.groupby(['weekday', 'magnus_result'], as_index=False)['event'].count() \
    .rename({'event': 'count'}, axis=1)

results = results.pivot_table(
    values='count', index='magnus_result', columns='weekday')

results_proportion = results.apply(lambda x: x/sum(x))


days = ['Sunday', 'Monday', 'Tuesday',
        'Wednesday', 'Thursday', 'Friday', 'Saturday']
# sort by days of week and convert to percent
results_proportion = round(results_proportion[days], 2)*100
results_proportion.index = ['draws', 'losses', 'wins']


# visualisate
fig = go.Figure()


for result in ['wins', 'draws', 'losses']:
    colors = {'wins': '#5032A9', 'draws': '#3c3d44', 'losses': '#f84050'}
    color = colors[result]

    fig.add_trace(go.Bar(x=days,
                         y=results_proportion.loc[result, :],
                         name=result,
                         text=(results_proportion.loc[result, :])
                         .apply(lambda x: str(int(x))) + '%',
                         textposition='inside',
                         textfont={'size': 24},
                         insidetextanchor='middle',
                         marker_color=color,
                         marker={'line': {'color': '#3c3d44'}},
                         opacity=1))

fig.update_layout(height=900, width=1500,
                  barmode='relative',
                  paper_bgcolor='#181a1e',
                  plot_bgcolor='#181a1e',
                  font={'color': '#ffffff', 'size': 24},
                  yaxis=dict(
                      showgrid=False,
                      showline=False,
                      showticklabels=True,
                      zeroline=True,
                      zerolinecolor='#3c3d44'),
                  legend=dict(xanchor='center', x=0.5, y=1.1,
                              font_size=25, orientation='h'))

plot(fig)

write_fig(fig)
