import pandas as pd

def get_latest(df : pd.DataFrame, interval : str) -> pd.DataFrame:
    """
    Returns a DataFrame considering all entries from latest session
        :param df: DataFrame containing all entries
        :param interval: string representing time interval (e.g. 90Mins)
        :ret pd.DataFrame: 
    """
    delta = pd.Timedelta("2 hours")
    df_new = df.copy()
    df_new = df_new.sort_index()      
    df_new = df_new.reset_index()
    return df[df.index >= df_new['index'].loc[df_new['index'].diff() > delta].iloc[-1]]                        
