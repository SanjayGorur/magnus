import pandas as pd
import re

def parse_data(text):
    all_data = text.split('\n\n')
    all_data = all_data[0:len(all_data)-1]
    
    metadata = all_data[::2]
    moves_data = all_data[1::2]
    
    metadata = list(map(lambda x: x.replace('[', '').replace(' "', ':') \
                         .replace(']','').replace('"', '').split('\n'), metadata))
        
    metadata = list(map(lambda x: list(map(lambda y: y.split(':')[1],x)), metadata))
    
    
    data = pd.DataFrame({'event':list(map(lambda x: x[0], metadata)),
                         'site':list(map(lambda x: x[1], metadata)),
                         'date':list(map(lambda x: x[2], metadata)),
                         'round':list(map(lambda x: x[3], metadata)),
                         'white':list(map(lambda x: x[4], metadata)),
                         'black':list(map(lambda x: x[5], metadata)),
                         'result':list(map(lambda x: x[6], metadata)),
                         'white_elo':list(map(lambda x: x[7], metadata)),
                         'black_elo':list(map(lambda x: x[8], metadata))})
    
    moves_data = list(map(lambda x: re.sub('\d+\.', '', x).replace('\n', ' ') , moves_data))
    moves_data = list(map(lambda x: x.split()[0:5], moves_data)) # choose first five moves
    
    data = pd.concat([data, pd.DataFrame({'1_move':list(map(lambda x: x[0], moves_data)),
                                          '2_move':list(map(lambda x: x[1], moves_data)),
                                          '3_move':list(map(lambda x: x[2], moves_data)),
                                          '4_move':list(map(lambda x: x[3], moves_data)),
                                          '5_move':list(map(lambda x: x[4], moves_data))})], axis=1)
    
    return data
    


def magnus_color(players):
    if players['white'] == 'Carlsen,M':
        return 'white'
    
    return 'black'



def magnus_opponent(players):
    if players['white'] == 'Carlsen,M':
        return players['black']
    
    return players['white']



def magnus_result(game):
    if game['result'] == '1/2-1/2':
        return 'draw'
    elif game['white'] == 'Carlsen,M' and game['result'] == '1-0':
        return 'win'
    elif game['white'] != 'Carlsen,M' and game['result'] == '0-1':
        return 'win'

    return 'lose' 


def preprocess_data(data):
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    
    data = data.loc[data['date'] > pd.to_datetime('2013-11-22')].reset_index(drop=True) # choose games since M became champion
    
    data.insert(3, 'weekday', data['date'].apply(lambda x: x.day_name()))
    
    data.insert(7, 'magnus_color', data[['white', 'black']].apply(magnus_color, axis=1))
    data.insert(8, 'opponent' , data[['white', 'black']].apply(magnus_opponent, axis=1))
    data.insert(10, 'magnus_result' , data[['white', 'result']].apply(magnus_result, axis=1))
    
    return data
    

def prepare_data_to_viz(data):
    # first move
    moves = pd.DataFrame({'ids':data['1_move'], 
                          'labels':data['1_move'], 
                          'parents':'',
                          'result':data['magnus_result']})
    
    # add second move
    moves = pd.concat([moves, pd.DataFrame({'ids':data['1_move'] +'-'+ data['2_move'],
                                   'labels':data['2_move'],
                                   'parents':data['1_move'],
                                   'result':data['magnus_result']})])
    
    # add third move
    moves = pd.concat([moves, pd.DataFrame({'ids':data['1_move'] +'-'+ data['2_move'] +'-'+ data['3_move'],
                                            'labels':data['3_move'],
                                            'parents':data['1_move'] +'-'+ data['2_move'],
                                            'result':data['magnus_result']})])
    
    # add fourth move
    moves = pd.concat([moves, pd.DataFrame({'ids':data['1_move'] +'-'+ data['2_move'] +'-'+ data['3_move'] +'-'+ data['4_move'],
                                            'labels':data['4_move'],
                                            'parents':data['1_move'] +'-'+ data['2_move'] +'-'+ data['3_move'],
                                            'result':data['magnus_result']})])
    
    # add fifth move
    moves = pd.concat([moves, pd.DataFrame({'ids':data['1_move'] +'-'+ data['2_move'] +'-'+ data['3_move'] +'-'+ data['4_move'] +'-'+ data['5_move'],
                                            'labels':data['5_move'],
                                            'parents':data['1_move'] +'-'+ data['2_move'] +'-'+ data['3_move'] +'-'+ data['4_move'],
                                            'result':data['magnus_result']})])
    
    moves['counts'] = 1
    results = moves.groupby(['ids', 'result'], as_index=False)['counts'].count()
    results = results.pivot_table(values='counts', columns='result', index='ids', fill_value=0)
    results['id'] = results.index
    
    moves['values'] = 1
    moves_count = moves.groupby('ids', as_index=False).agg({'values':'count'})
    moves = moves.drop('values', axis=1).drop_duplicates('ids').reset_index(drop=True)
    
    moves = moves.merge(results, left_on='ids', right_on='id')
    moves = moves.merge(moves_count)    
    
    return moves



def add_color(moves, color):
    moves['color'] = moves['ids'].apply(lambda x: x.split('-')[0])
    
    if color == 'white':
        moves['color'] = moves['color'].map({
            'e4':'#47186a',
            'd4':'#424085',
            'c4':'#2c728e',
            'Nf3':'#20908c',
            'b3':'#1e9f88',
            'f4':'#1e9f88',
            'g3':'#28ae7f',
            'e3':'#28ae7f',
            'Nc3':'#3ebc73',
            'h3':'#3ebc73',
            'Nh3':'#3ebc73',
            'b4':'#5ec961',
            'Na3':'#5ec961',
            'f3':'#83d34b',
            'a3':'#3ebc73'})
        
    if color == 'black':
        moves['color'] = moves['color'].map({
            'e4':'#47186a',
            'd4':'#424085',
            'c4':'#20908c',
            'Nf3':'#2c728e',
            'b3':'#1e9f88',
            'g3':'#5ec961',
            'Nc3':'#83d34b'})
        
    return moves
