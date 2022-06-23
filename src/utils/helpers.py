import pandas as pd 
import numpy as np 
import networkx as nx 
import matplotlib.pyplot as plt

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


def get_edge_list(df:pd.DataFrame, filter:bool = False) -> list:
    """Function to create a list of edges from a dataframe."""
    if filter:
        return [(process, material) for process in df.index for material in df.columns if df.loc[process, material] != 0]
    else: 
        return [(process, material) for process in df.index for material in df.columns]

def clean_dataframe(df:pd.DataFrame) -> pd.DataFrame:
    """Function to clean the dataframe."""
    ## remove the last column "Cost/Energy…?"
    df.drop(columns=['Cost/Energy…?'], inplace=True)
    ## convert to int 
    df = df.astype(np.int64)
    return df 