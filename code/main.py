from data_processing_funs import parse_data, preprocess_data
from data_processing_funs import prepare_data_to_viz, add_color
from viz import make_plot, write_fig
from plotly.offline import plot


with open('../data/carlsen.pgn', 'r') as f:
    text = f.read()
    
data = parse_data(text)
data = preprocess_data(data)


white_moves = prepare_data_to_viz(data.loc[data['magnus_color'] == 'white'])
black_moves = prepare_data_to_viz(data = data.loc[data['magnus_color'] != 'white'])


white_moves = add_color(white_moves, 'white')
black_moves = add_color(black_moves, 'black')

fig = make_plot(white_moves, black_moves)

plot(fig)

write_fig(fig)
