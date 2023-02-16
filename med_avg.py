import pandas as pd
from functions import *

def main():
    offense = get_offense()
    defense = get_defense()

    big_dict = divide_pos(offense,defense)

    avg_dict = avg_dicts(big_dict)

    med_avgs = get_med_avgs(avg_dict)

    f1, f2 = get_flex_avgs(avg_dict)
    med_avgs['Med_Avg'].loc['FLEX1'] = f1
    med_avgs['Med_Avg'].loc['FLEX2'] = f2

    d1, d2 = get_dflex_avgs(avg_dict)
    med_avgs['Med_Avg'].loc['DFLEX1'] = d1
    med_avgs['Med_Avg'].loc['DFLEX2'] = d2

    flex_rates = get_flex_rates(offense)
    dflex_rates = get_dflex_rates(defense)

    flex_rate_df = pd.DataFrame(data=flex_rates,index=['RB','WR','TE'])
    dflex_rate_df = pd.DataFrame(data=dflex_rates, index=['DT', 'DE', 'LB', 'CB', 'S'])

main()
