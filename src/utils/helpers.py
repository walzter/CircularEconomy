import pandas as pd 

def load_dataframe(path:str) -> pd.DataFrame:
    """Function to load the Adjacency Matrix from a csv file."""
    df = pd.read_csv(path)
    #take the first row and put as columns header in df
    header, df = df.iloc[0], df[1: ]
    ## the remaining of the data 
    
    ## make the header as as columns 
    df.columns = header
    # set the to processes 
    df = df.set_index('Processes')
    return df 


def get_edge_list(df:pd.DataFrame) -> list:
    """Function to create a list of edges from a dataframe."""
    return [(process, material) for process in df.index for material in df.columns]

def get_edge_list_weighted(df:pd.DataFrame) -> list:
    """Function to create a list of edges from a dataframe."""
    return [(process, material, df.loc[process, material]) for process in df.index for material in df.columns]

def clean_dataframe(df:pd.DataFrame) -> pd.DataFrame:
    """Function to clean the dataframe."""
    pass 
