# dictionary for positional scoring by week:
#   key = week number, value = dictionary
#       key = position (QB,RB,WR,TE,DT,DE,LB,CB,S,FLEX,DFLEX)
#       value = dataframe

from functions import *
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm

def main():
    dict_split = {}
    dict_all = {}
    mean, std = avg_team()
    for year in [2020,2021,2022]:
        print("Year: " + str(year))
        top_scorers = top_scorers_by_pos(year)
        replacement_values = get_replacement_values(year)
        wpa_dict = wpa_by_pos(top_scorers,replacement_values,mean,std)

        # x, y, sizes = prepare_to_plot(wpa_dict)

        # plt.scatter(x,y,s=sizes)
        # plt.show()

        df_all = wpa_all_pos(wpa_dict)
        df_split = dict_to_df(wpa_dict)

        dict_split[year] = df_split
        dict_all[year] = df_all

    avg_split_df = avg_dfs(dict_split)

    with pd.ExcelWriter("HolyGrailWorp2.xlsx") as writer:
        dict_all[2020].to_excel(writer, sheet_name="2020", index=False)
        dict_all[2021].to_excel(writer, sheet_name="2021", index=False)
        dict_all[2022].to_excel(writer, sheet_name="2022", index=False)
        avg_split_df.to_excel(writer, sheet_name="Avg By Pos", index=False)

main()
