import pandas as pd
from functions import *

def main():
    dlf = pd.read_csv('idp_rankings_dlf.csv')
    dlf = dlf.drop(['AVG','Jase A', 'Jason K', 'Value', 'Audio'],axis=1)
    true_pos = pd.read_csv('true_pos.csv')

    defense = get_defense()
    mfl = defense[2022]

    for idx in dlf.index:
        name = dlf['Name'].loc[idx]
        substrings = name.split(' ')
        dlf['Name'].loc[idx] = substrings[1] + ', ' + substrings[0]
        name = dlf['Name'].loc[idx]
        for idx in mfl.index:
            if name == mfl['Player'].loc[idx]:
                mfl_pos = mfl['Pos'].loc[idx]
                dlf['Pos'].loc[idx] = mfl_pos
        for idx in true_pos.index:
            if name == true_pos['MFL Name'].loc[idx]:
                dlf['Pos'].loc[idx] = true_pos['TRUE POSITION'].loc[idx]

main()