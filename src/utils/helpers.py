import pandas as pd 
import numpy as np 
import neo4j
import matplotlib.pyplot as plt
import networkx as nx


def reading_data(path:str) -> pd.DataFrame:
    
    df = pd.read_csv(path)


    #take the first column of the data and convert as the index of the dataframe\n",
    df.index = df.iloc[:,0]

    #delete the first column
    df = df.drop(df.columns[0], axis=1)


    return (df)



def load_dataframe(path:str) -> pd.DataFrame:
    """Function to load the Adjacency Matrix from a csv file."""
    df = pd.read_csv(path)
    #take the first row and put as columns header in df
    header, df = df.iloc[0], df[1: ]
    ## the remaining of the data 
    
    ## make the header as as columns 
    df.columns = header
    # set the to processes 
    df = df.set_index("Processes")
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


def prepare_dataframe(path:str,save_dir:str) -> pd.DataFrame:
    """
    This function takes the path to the data and returns a dataframe with the data.
    """
    ## loading 
    df = pd.read_csv(path).reset_index(drop=True)
    ## current dataframe: Processes | Material 1| Material 2| Material 3| ... 
    ## convert to Processes | Materials | Values
    long_df = pd.wide_to_long(df, ["M-"], i="Processes", j="Material").reset_index().rename(columns={"M-": "Consumption"})
    ## add Input or Output column
    ## x > 0 -> Input, x < 0 -> Output, x = 0 -> None
    long_df['IO'] = long_df['Consumption'].apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0)
    ## adding the text to it in case
    long_df['IO_txt'] = long_df['IO'].apply(lambda x: "Input" if x == 1 else "Output" if x == -1 else "None")
    long_df['Processes'] = list(map(lambda x: f'P{int(x.split("-")[1])}',long_df['Processes']))
    long_df['Material'] = list(map(lambda x: f"M{x}",long_df['Material']))
    ## the dataframe is per process, 
    long_df = long_df.sort_values(by=['Processes','Material'])
    ## remove materials that are not used, keep the used one. 
    long_df_nz = long_df.query("Consumption != 0")
    long_df_nz = long_df_nz.drop(columns=['IO','IO_txt'])
    ## save it 
    long_df_nz.to_csv(save_dir, index=False)
    ## return the dataframe
    return long_df_nz
    
    
    
def parse_subgraph(subgraph:tuple) -> list:
    """Returns a list of tuples for the subgraph"""
    ## get the relationships
    relationships = [rel for subg in subgraph[0] for rel in subg if type(rel) != neo4j.graph.Node]
    ## retrieve the data, store as generator for lazy loading
    data = [(x.type, x.nodes[0]._properties['uuid'],x.nodes[1]._properties['uuid']) for x in relationships]
    return data, relationships


def parsed_subgraph_to_df(parsed_subgraph:list,verbose:bool=False) -> pd.DataFrame:
    """Returns the dataframe of a parsed subgraph"""
    ## make the dataframe
    df = pd.DataFrame(parsed_subgraph, columns=['Relationship', 'From', 'To']).sort_values(by=['Relationship'],ascending=True)
    if verbose:
        from termcolor import colored
        for e in df.itertuples():
            ## type of the relationship
            _node_a,_node_b = e[2], e[3]
            if e[1] =='INPUT_MATERIAL':
                ## then "M1" is INPUT_MATERIAL for "P2"; "M1" --> "P2"
                _type_c = colored("INPUT_MATERIAL ", "green")
                print(f"{_type_c} for Process {_node_b}; {_node_a} --> {_node_b}")
            elif e[1] =='OUTPUT_MATERIAL':
                _type_c = colored("OUTPUT_MATERIAL", "red")
                ## then "M1" is OUTPUT_MATERIAL for "P2"; "P2" --> "M1"
                print(f"{_type_c} for Process {_node_a}; {_node_a} --> {_node_b}")
    return df