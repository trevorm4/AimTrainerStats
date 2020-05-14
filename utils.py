import pandas as pd
from datetime import datetime
def create_dict_from_file(path):
    stats = {}
    empty_required = 2 # simply due to the format of the csv files
    num_empty = 0
    csv_header = ""

    split_name = path.split(" - ")
    date_str = split_name[-1]
    date_split = date_str.split("-")
    stats["Date"] = date_split[0]
    stats["Time"] = date_split[1].split(" ")[0]
    stats["Scenario"] = split_name[0]

    with open(path,'r') as f:
        for line in f:
            if line in ['\n', '\r\n']:
                if num_empty < empty_required:
                    num_empty += 1
                else:
                    return stats
            elif num_empty == empty_required - 1:
                split_line = line.strip().split(",")
                if split_line[0] != "Weapon": #its the stat line
                    for i in range(len(split_line)):
                        stats[csv_header[i]] = split_line[i]
                else: #header
                    csv_header = [i for i in line.strip().split(",") if len(i) > 0]
            elif num_empty == empty_required:
                split_line = line.split(":,")
                stats[split_line[0].strip()] = split_line[1].strip()
    return stats

def get_score(stat_dict):
    return stat_dict["Score"]

def get_accuracy(stat_dict):
    return int(stat_dict["Hits"])/int(stat_dict["Shots"])

def get_datetime(stat_dict):
    datetime_str = stat_dict["Date"] + " " + stat_dict["Time"]
    return datetime.strptime(datetime_str,"%Y.%m.%d %H.%M.%S")
def get_scenario(stat_dict):
    return stat_dict["Scenario"]

def init_df():
    return pd.DataFrame(columns=["Date","Scenario","Score","Accuracy"])

def add_entry(df,stats):
    temp_list = [get_datetime(stats), get_scenario(stats), get_score(stats), get_accuracy(stats)]
    df.loc[len(df)] = temp_list

