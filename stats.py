import pandas as pd

def get_latest(df : pd.DataFrame, interval : str) -> pd.DataFrame:
    """
    Returns a DataFrame considering all entries from latest session
        :param df: DataFrame containing all entries
        :param interval: string representing time interval (e.g. 90Mins)
        :ret pd.DataFrame: 
    """
    delta = pd.Timedelta("4 hours")
    df_new = df.copy()
    df_new = df_new.sort_index()      
    df_new = df_new.reset_index()
    return df[df.index >= df_new['index'].loc[df_new['index'].diff() > delta].iloc[-1]]                        

def get_scenario_data(df: pd.DataFrame, scenario : str) -> pd.DataFrame:
    return df[df["Scenario"] == scenario]

def get_mean_accuracy(session_df : pd.DataFrame, scenario : str):
    scenario_data = get_scenario_data(session_df, scenario)
    return scenario_data["Accuracy"].mean()

def get_mean_score(session_df : pd.DataFrame, scenario: str):
    scenario_data = get_scenario_data(session_df, scenario)
    return scenario_data["Score"].mean()    

def get_session_starts(df: pd.DataFrame) -> pd.Series:
    delta = pd.Timedelta("2 hours") 
    df_new = df.copy()
    df_new = df_new.sort_index()      
    df_new = df_new.reset_index()
    starting = df_new['index'].loc[df_new['index'].diff() > delta]
    starting.loc[0] = df_new.iloc[0]["index"]
    starting = starting.sort_index()
    return starting

def get_session_dataframes(df: pd.DataFrame) -> pd.DataFrame:
    starts_dict = get_session_starts(df).to_dict()
    df = df.sort_index()
    cutoffs = list(starts_dict.keys())
    cutoffs.sort()
    prev = cutoffs[0]
    df_dict = {}
    cur = None
    prev = 0
    for i in range(1,len(cutoffs)):
        cur = cutoffs[i]
        df_dict[starts_dict[prev]] = df.iloc[prev:cur]
        prev = cur
    df_dict[starts_dict[cur]] = df.iloc[cur:]
    return df_dict #maps start of sessions to their respective dataframe


def create_stat_df(df : pd.DataFrame) -> pd.DataFrame:
    # creates df, where in each session, the scores and accuracies are averaged out
    starts = get_session_dataframes(df)
    new_dict = {}
    for k,v in starts.items():
        d = {"Date" : [] , "Scenario" : [], "Score" : [], "Accuracy" : []}
        for i,s in enumerate(v["Scenario"].unique()):
            sub_df = v[v["Scenario"] == s].describe()
            d["Date"].append(k)
            d["Score"].append(sub_df.loc["mean"]["Score"])
            d["Accuracy"].append(sub_df.loc["mean"]["Accuracy"])
            d["Scenario"].append(s)
        new_dict[k] = pd.DataFrame(d)
    return new_dict

def create_mean_df(df : pd.DataFrame) -> pd.DataFrame:
    return pd.concat(list(create_stat_df(df).values()),ignore_index=True)
