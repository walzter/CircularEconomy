import pandas

def reading(path):
    
    df = pandas.read_csv(path)
    #take the first row and put as columns header in df
    header = df.iloc[0]
    df = df[1: ]
    df.columns =header
    #
    df = df.set_index('Processes')

    df.head()

    return df 