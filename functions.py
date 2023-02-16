import pandas as pd
import lxml
import numpy as np
from scipy.stats import norm

def get_offense():
    dict = {}
    for year in [2020,2021,2022]:
        url = 'https://www55.myfantasyleague.com/2022/top?L=45889&SEARCHTYPE=BASIC&COUNT=300' \
          '&YEAR=' + str(year) + '&START_WEEK=1&END_WEEK=16&CATEGORY=overall&' \
            'POSITION=QB%7CRB%7CWR%7CTE&DISPLAY=points&TEAM=*&SORT=TOT'
        lis = pd.read_html(url)
        df = lis[1]
        cols = ['Rank','Player','Total','Avg']
        for i in range(1,17):
            cols.append(str(i))
        cols.append('Matchup')
        cols.append('Owner')
        cols.append('Bye')
        df.columns = cols
        df = df.drop(['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'
                        ,'Matchup','Owner','Bye'], axis = 1)
        df = clean_df(df)
        dict[year] = df
    return dict

def get_defense():
    dict = {}
    for year in [2020,2021,2022]:
        url = 'https://www55.myfantasyleague.com/2022/top?L=45889&SEARCHTYPE=BASIC&COUNT=500' \
          '&YEAR=' + str(year) + '&START_WEEK=1&END_WEEK=16&CATEGORY=overall&' \
            'POSITION=DT%7CDE%7CLB%7CCB%7CS&DISPLAY=points&TEAM=*&SORT=TOT'
        lis = pd.read_html(url)
        df = lis[1]
        cols = ['Rank','Player','Total','Avg']
        for i in range(1,17):
            cols.append(str(i))
        cols.append('Matchup')
        cols.append('Owner')
        cols.append('Bye')
        df.columns = cols
        df = df.drop(['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'
                        ,'Matchup','Owner','Bye'], axis = 1)
        df = clean_df(df)
        dict[year] = df
    return dict

def clean_df(df):
    positions, teams = [], []

    for index in df.index:
        player = df['Player'].loc[index]

        sl = slice(len(player) - 3, len(player), 1)
        if player[sl] == '(R)':
            player = player[:len(player) - 4]

        if player[len(player) - 1] == 'S':
            sl = slice(len(player) - 1, len(player), 1)
            pos = player[sl]
            positions.append(pos)
            player = player[:len(player) - 2]

            sl = slice(len(player) - 4, len(player), 1)
            team = player[sl]
            teams.append(team)
            player = player[:len(player) - 3]
            df['Player'].loc[index] = player
        else:
            sl = slice(len(player) - 2, len(player), 1)
            pos = player[sl]
            positions.append(pos)
            player = player[:len(player) - 3]

            sl = slice(len(player) - 4, len(player), 1)
            team = player[sl]
            teams.append(team)
            player = player[:len(player) - 3]
            df['Player'].loc[index] = player

    df['Team'] = teams
    df['Pos'] = positions
    return df

def divide_offense(df):
    RB = pd.DataFrame(columns=df.columns)
    WR = pd.DataFrame(columns=df.columns)
    TE = pd.DataFrame(columns=df.columns)
    QB = pd.DataFrame(columns=df.columns)
    for index in df.index:
        pos = df['Pos'][index]
        if pos == 'QB':
            QB.loc[len(QB.index)] = df.loc[index]
        if pos == 'RB':
            RB.loc[len(RB.index)] = df.loc[index]
        if pos == 'WR':
            WR.loc[len(WR.index)] = df.loc[index]
        if pos == 'TE':
            TE.loc[len(TE.index)] = df.loc[index]

    return QB, RB, WR, TE

def divide_defense(defense):
    DT = pd.DataFrame(columns =defense.columns)
    DE = pd.DataFrame(columns=defense.columns)
    LB = pd.DataFrame(columns=defense.columns)
    CB = pd.DataFrame(columns=defense.columns)
    S = pd.DataFrame(columns=defense.columns)
    for index in defense.index:
        pos = defense['Pos'][index]
        if pos == 'DT':
            DT.loc[len(DT.index)] = defense.loc[index]
        if pos == 'DE':
            DE.loc[len(DE.index)] = defense.loc[index]
        if pos == 'LB':
            LB.loc[len(LB.index)] = defense.loc[index]
        if pos == 'CB':
            CB.loc[len(CB.index)] = defense.loc[index]
        if pos == 'S':
            S.loc[len(S.index)] = defense.loc[index]
    return DT, DE, LB, CB, S

def divide_pos(offense,defense):
    dict_2020 = {}
    dict_2021 = {}
    dict_2022 = {}

    QB, RB, WR, TE = divide_offense(offense[2020])
    DT, DE, LB, CB, S = divide_defense(defense[2020])
    dict_2020 = {'QB': QB, 'RB': RB, 'WR': WR, 'TE': TE, 'DT': DT, 'DE': DE, 'LB': LB, 'CB': CB, 'S': S}

    QB, RB, WR, TE = divide_offense(offense[2021])
    DT, DE, LB, CB, S = divide_defense(defense[2021])
    dict_2021 = {'QB': QB, 'RB': RB, 'WR': WR, 'TE': TE, 'DT': DT, 'DE': DE, 'LB': LB, 'CB': CB, 'S': S}

    QB, RB, WR, TE = divide_offense(offense[2022])
    DT, DE, LB, CB, S = divide_defense(defense[2022])
    dict_2022 = {'QB': QB, 'RB': RB, 'WR': WR, 'TE': TE, 'DT': DT, 'DE': DE, 'LB': LB, 'CB': CB, 'S': S}

    final_dict = {2020:dict_2020, 2021:dict_2021, 2022:dict_2022}
    return final_dict

def avg_dicts(big_dict):
    avg_dict = {}
    for pos in ['QB','RB','WR','TE','DT','DE','LB','CB','S']:
        dict_2020 = big_dict[2020][pos]
        dict_2021 = big_dict[2021][pos]
        dict_2022 = big_dict[2022][pos]
        lens = [len(dict_2020),len(dict_2021),len(dict_2022)]
        avgs = []
        for idx in range(0,min(lens)):
            avgs_at_idx = []
            for year in big_dict.keys():
                dict = big_dict[year][pos]
                avgs_at_idx.append(dict['Avg'].iloc[idx])
            avg = (avgs_at_idx[0] + avgs_at_idx[1] + avgs_at_idx[2]) / 3
            avgs.append(avg)
        avgs_df = pd.DataFrame(data=avgs,columns=['Avg'])
        pos_list = []
        for i in range(0,len(avgs_df.index)):
            pos_list.append(pos)
        avgs_df['Pos'] = pos_list
        avg_dict[pos] = avgs_df
    return avg_dict

def get_med_avgs(avg_dict):
    med_avg_df = pd.DataFrame(columns=['Med_Avg'],index=['QB1','QB2','RB1','RB2','WR1','WR2','WR3','TE1',
                                                         'FLEX1','FLEX2','DT1','DE1','DE2','LB1','LB2',
                                                         'LB3','CB1','CB2','S1','S2','DFLEX1','DFLEX2'])
    qb1, qb2 = med_avg_2(avg_dict['QB'])
    rb1, rb2 = med_avg_2(avg_dict['RB'])
    wr1, wr2, wr3 = med_avg_3(avg_dict['WR'])
    te1 = med_avg_1(avg_dict['TE'])
    dt1 = med_avg_1(avg_dict['DT'])
    de1, de2 = med_avg_2(avg_dict['DE'])
    lb1, lb2, lb3 = med_avg_3(avg_dict['LB'])
    cb1, cb2 = med_avg_2(avg_dict['CB'])
    s1, s2 = med_avg_2(avg_dict['S'])

    med_avg_df['Med_Avg'] = [qb1,qb2,rb1,rb2,wr1,wr2,wr3,te1,0.0,0.0,dt1,de1,de2,lb1,lb2,lb3,
                             cb1,cb2,s1,s2,0.0,0.0]
    return med_avg_df

def med_avg_1(df):
    a1 = (df['Avg'].loc[4] + df['Avg'].loc[5] + df['Avg'].loc[6] + df['Avg'].loc[7]) / 4
    return a1

def med_avg_2(df):
    a1 = (df['Avg'].loc[4] + df['Avg'].loc[5] + df['Avg'].loc[6] + df['Avg'].loc[7]) / 4
    a2 = (df['Avg'].loc[16] + df['Avg'].loc[17] + df['Avg'].loc[18] + df['Avg'].loc[19]) / 4
    return a1, a2

def med_avg_3(df):
    a1 = (df['Avg'].loc[4] + df['Avg'].loc[5] + df['Avg'].loc[6] + df['Avg'].loc[7]) / 4
    a2 = (df['Avg'].loc[16] + df['Avg'].loc[17] + df['Avg'].loc[18] + df['Avg'].loc[19]) / 4
    a3 = (df['Avg'].loc[28] + df['Avg'].loc[29] + df['Avg'].loc[30] + df['Avg'].loc[31]) / 4
    return a1, a2, a3

def get_flex_avgs(avg_dict):
    flex = pd.concat([avg_dict['RB'], avg_dict['WR'], avg_dict['TE']], axis=0)
    flex = flex.sort_values(by=['Avg'],ascending=False)
    flex = flex.reset_index(drop=True)

    droppable = []
    for index in flex.index:
        pos = flex['Pos'].loc[index]
        if pos == 'RB' and len(droppable) < 24:
            droppable.append(index)
    for index in flex.index:
        pos = flex['Pos'].loc[index]
        if pos == 'WR' and len(droppable) < 60:
            droppable.append(index)
    for index in flex.index:
        pos = flex['Pos'].loc[index]
        if pos == 'TE' and len(droppable) < 72:
            droppable.append(index)
    flex = flex.drop(droppable)
    flex = flex.reset_index(drop=True)
    f1, f2 = med_avg_2(flex)
    return f1, f2

def get_dflex_avgs(avg_dict):
    flex = pd.concat([avg_dict['DT'], avg_dict['DE'], avg_dict['LB'], avg_dict['CB'], avg_dict['S']], axis=0)
    flex = flex.sort_values(by=['Avg'],ascending=False)
    flex = flex.reset_index(drop=True)

    droppable = []
    for index in flex.index:
        pos = flex['Pos'].loc[index]
        if pos == 'DT' and len(droppable) < 12:
            droppable.append(index)
    for index in flex.index:
        pos = flex['Pos'].loc[index]
        if pos == 'DE' and len(droppable) < 36:
            droppable.append(index)
    for index in flex.index:
        pos = flex['Pos'].loc[index]
        if pos == 'LB' and len(droppable) < 72:
            droppable.append(index)
    for index in flex.index:
        pos = flex['Pos'].loc[index]
        if pos == 'CB' and len(droppable) < 96:
            droppable.append(index)
    for index in flex.index:
        pos = flex['Pos'].loc[index]
        if pos == 'S' and len(droppable) < 120:
            droppable.append(index)
    flex = flex.drop(droppable)
    flex = flex.reset_index(drop=True)
    f1, f2 = med_avg_2(flex)
    return f1, f2

def get_flex_rates():
    rb_count, wr_count, te_count, weekly_count = 0, 0, 0, 0
    for year in [2020,2021,2022]:
        for week in list(range(1,17)):
            df = get_weekly_df(year,week,True)
            droppable = []
            for index in df.index:
                pos = df['Pos'].loc[index]
                if pos == 'RB' and len(droppable) < 24:
                    droppable.append(index)
            for index in df.index:
                pos = df['Pos'].loc[index]
                if pos == 'WR' and len(droppable) < 60:
                    droppable.append(index)
            for index in df.index:
                pos = df['Pos'].loc[index]
                if pos == 'TE' and len(droppable) < 72:
                    droppable.append(index)
            df = df.drop(droppable)
            df = df.reset_index(drop=True)

            weekly_count = 0
            for index in df.index:
                weekly_count += 1
                if df['Pos'].loc[index] == 'RB':
                    rb_count = rb_count + 1
                elif df['Pos'].loc[index] == 'WR':
                    wr_count = wr_count + 1
                elif df['Pos'].loc[index] == 'TE':
                    te_count = te_count + 1
                if weekly_count == 24:
                    break

    rb_rate = rb_count / (3 * 16 * 24)
    wr_rate = wr_count / (3 * 16 * 24)
    te_rate = te_count / (3 * 16 * 24)
    return [rb_rate,wr_rate,te_rate]

def get_dflex_rates(defense):
    dt_rates, de_rates, lb_rates, cb_rates, s_rates = [],[],[],[],[]
    for year in defense.keys():
        df = defense[year]
        droppable = []
        for index in df.index:
            pos = df['Pos'].loc[index]
            if pos == 'DT' and len(droppable) < 12:
                droppable.append(index)
        for index in df.index:
            pos = df['Pos'].loc[index]
            if pos == 'DE' and len(droppable) < 36:
                droppable.append(index)
        for index in df.index:
            pos = df['Pos'].loc[index]
            if pos == 'LB' and len(droppable) < 72:
                droppable.append(index)
        for index in df.index:
            pos = df['Pos'].loc[index]
            if pos == 'CB' and len(droppable) < 96:
                droppable.append(index)
        for index in df.index:
            pos = df['Pos'].loc[index]
            if pos == 'S' and len(droppable) < 120:
                droppable.append(index)
        df = df.drop(droppable)
        df = df.reset_index(drop=True)

        counts = [0, 0, 0, 0, 0]
        for index in df.index:
            if df['Pos'].loc[index] == 'DT':
                counts[0] = counts[0] + 1
            elif df['Pos'].loc[index] == 'DE':
                counts[1] = counts[1] + 1
            elif df['Pos'].loc[index] == 'LB':
                counts[2] = counts[2] + 1
            elif df['Pos'].loc[index] == 'CB':
                counts[3] = counts[3] + 1
            elif df['Pos'].loc[index] == 'S':
                counts[4] = counts[4] + 1
            if counts[0] + counts[1] + counts[2] + counts[3] + counts[4] == 24:
                dt_rates.append(counts[0] / 24)
                de_rates.append(counts[1] / 24)
                lb_rates.append(counts[2] / 24)
                cb_rates.append(counts[3] / 24)
                s_rates.append(counts[4] / 24)
    dt_rate = (dt_rates[0] + dt_rates[1] + dt_rates[2]) / 3
    de_rate = (de_rates[0] + de_rates[1] + de_rates[2]) / 3
    lb_rate = (lb_rates[0] + lb_rates[1] + lb_rates[2]) / 3
    cb_rate = (cb_rates[0] + cb_rates[1] + cb_rates[2]) / 3
    s_rate = (s_rates[0] + s_rates[1] + s_rates[2]) / 3
    return [dt_rate,de_rate,lb_rate,cb_rate,s_rate]

def get_rosters():
    url = 'https://www55.myfantasyleague.com/2022/options?L=29667&O=07'
    lis = pd.read_html(url)
    rosters = []
    for idx in range(2,18):
        droppable = []
        roster = lis[idx]
        for i in roster.index:
            bye = roster['Bye'].loc[i]
            if len(bye) > 2:
                droppable.append(i)
        roster = roster.drop(droppable)
        roster = roster.reset_index(drop=True)
        roster = clean_roster(roster)
        rosters.append(roster)
    return rosters

def evaluate_rosters(rosters):
    cons = {'QB':0,'RB':0,'WR':0,'TE':0,'DT':0,'DE':0,'LB':0,'CB':0,'S':0}
    for roster in rosters:
        for idx in roster.index:
            pos = roster['Pos'].loc[idx]
            cons[pos] = cons[pos] + 1
    total_players = 0
    for pos in cons.keys():
        total_players = total_players + cons[pos]
    ratios = {}
    for pos in cons.keys():
        r = cons[pos] / total_players
        ratios[pos] = r
    return ratios

def clean_roster(df):
    positions, teams = [], []

    for index in df.index:
        player = df['Player'].iloc[index]

        sl = slice(len(player) - 3, len(player), 1)
        if player[sl] == '(Q)' or player[sl] == '(I)' or player[sl] == '(O)' or player[sl] == '(D)':
            player = player[:len(player) - 4]

        sl = slice(len(player) - 3, len(player), 1)
        if player[sl] == '(R)':
            player = player[:len(player) - 4]

        if player[len(player) - 1] == 'S':
            sl = slice(len(player) - 1, len(player), 1)
            pos = player[sl]
            positions.append(pos)
            player = player[:len(player) - 2]

            sl = slice(len(player) - 4, len(player), 1)
            team = player[sl]
            teams.append(team)
            player = player[:len(player) - 3]
            df['Player'].loc[index] = player
        else:
            sl = slice(len(player) - 2, len(player), 1)
            pos = player[sl]
            positions.append(pos)
            player = player[:len(player) - 3]

            sl = slice(len(player) - 4, len(player), 1)
            team = player[sl]
            teams.append(team)
            player = player[:len(player) - 3]
            df['Player'].loc[index] = player
        for i in ['(',')']:
            pos = pos.replace(i, '')
            positions[index] = pos

    df['Team'] = teams
    df['Pos'] = positions
    return df

def num_rostered(ratios):
    rostered = {}
    for pos in ratios.keys():
        rostered[pos] = ratios[pos] * 480
    return rostered

def get_waivers(total_rostered,sorted_players):
    for pos in total_rostered.keys():
        num_rostered = total_rostered[pos]
        df = sorted_players[pos]
        droppable = list(range(0,int(num_rostered)))
        df = df.drop(droppable)
        df = df.reset_index(drop=True)
        sorted_players[pos] = df
    return sorted_players

def sort_rosters_by_position(rosters):
    df = rosters[0]
    RB = pd.DataFrame(columns=df.columns)
    WR = pd.DataFrame(columns=df.columns)
    TE = pd.DataFrame(columns=df.columns)
    QB = pd.DataFrame(columns=df.columns)
    DT = pd.DataFrame(columns=df.columns)
    DE = pd.DataFrame(columns=df.columns)
    LB = pd.DataFrame(columns=df.columns)
    CB = pd.DataFrame(columns=df.columns)
    S = pd.DataFrame(columns=df.columns)
    for df in rosters:
        for index in df.index:
            pos = df['Pos'][index]
            if pos == 'QB':
                QB.loc[len(QB.index)] = df.loc[index]
            if pos == 'RB':
                RB.loc[len(RB.index)] = df.loc[index]
            if pos == 'WR':
                WR.loc[len(WR.index)] = df.loc[index]
            if pos == 'TE':
                TE.loc[len(TE.index)] = df.loc[index]
            if pos == 'DT':
                DT.loc[len(DT.index)] = df.loc[index]
            if pos == 'DE':
                DE.loc[len(DE.index)] = df.loc[index]
            if pos == 'LB':
                LB.loc[len(LB.index)] = df.loc[index]
            if pos == 'CB':
                CB.loc[len(CB.index)] = df.loc[index]
            if pos == 'S':
                S.loc[len(S.index)] = df.loc[index]
    rosters_by_pos = {'QB': QB, 'RB': RB, 'WR': WR, 'TE': TE, 'DT': DT, 'DE': DE, 'LB': LB, 'CB': CB, 'S': S}
    return rosters_by_pos

def get_replacement_values(year):
    weekly_replacements = {'QB':[],'RB':[],'WR':[],'TE':[],'DT':[],'DE':[],'LB':[],'CB':[],'S':[]}
    for week in list(range(1,17)):
        print("Week: " + str(week))
        for pos in ['QB','RB','WR','TE','DT','DE','LB','CB','S']:
            url = 'https://www55.myfantasyleague.com/2022/top?L=29667&SEARCHTYPE=ADVANCED&COUNT=64' \
                  '&YEAR=' + str(year) + '&START_WEEK=' + str(week) + '&END_WEEK=' + str(week) + \
                  '&CATEGORY=overall&POSITION=' + pos + '&DISPLAY=points&TEAM=*'
            lis = pd.read_html(url)
            df = lis[1]
            df.columns = ['Rank','Player','Pts','Avg','Weekly','Matchup','Owner','Bye']
            df = df.drop(['Rank','Avg','Weekly','Matchup','Owner','Bye'], axis = 1)
            df = clean_df(df)
            rep_list = weekly_replacements[pos]
            if pos in ['QB','RB','DE','CB','S']:
                if len(df.index) < 32:
                    replacement_value = (df['Pts'].loc[len(df.index) - 2] + df['Pts'].loc[len(df.index) - 1]) / 2
                    weekly_replacements[pos].append(replacement_value)
                    continue
                replacement_value = (df['Pts'].loc[28] + df['Pts'].loc[29] + df['Pts'].loc[30] + df['Pts'].loc[31]) / 4
                weekly_replacements[pos].append(replacement_value)
                #weekly_replacements[pos] = rep_list.append(replacement_value)
            elif pos in ['WR','LB']:
                if len(df.index) < 44:
                    replacement_value = (df['Pts'].loc[len(df.index) - 2] + df['Pts'].loc[len(df.index) - 1]) / 2
                    weekly_replacements[pos].append(replacement_value)
                    continue
                replacement_value = (df['Pts'].loc[40] + df['Pts'].loc[41] + df['Pts'].loc[42] + df['Pts'].loc[43]) / 4
                print(pos)
                print(week)
                weekly_replacements[pos].append(replacement_value)
                #weekly_replacements[pos] = rep_list.append(replacement_value)
            elif pos in ['TE','DT']:
                if len(df.index) < 20:
                    replacement_value = (df['Pts'].loc[len(df.index) - 2] + df['Pts'].loc[len(df.index) - 1]) / 2
                    weekly_replacements[pos].append(replacement_value)
                    continue
                replacement_value = (df['Pts'].loc[16] + df['Pts'].loc[17] + df['Pts'].loc[18] + df['Pts'].loc[19]) / 4
                print(pos)
                print(week)
                weekly_replacements[pos].append(replacement_value)
                #weekly_replacements[pos] = rep_list.append(replacement_value)
    final_values = {}
    for pos in weekly_replacements.keys():
        s = 0
        for v in weekly_replacements[pos]:
            s += v
        final_values[pos] = s / 16

    return final_values

def top_scorers_by_pos(year):
    top_scorers = {}
    for pos in ['QB', 'RB', 'WR', 'TE', 'DT', 'DE', 'LB', 'CB', 'S']:
        url = 'https://www55.myfantasyleague.com/2022/top?L=29667&SEARCHTYPE=ADVANCED&COUNT=64&YEAR=' \
              + str(year) + '&START_WEEK=1&END_WEEK=16&CATEGORY=overall&POSITION=' + pos + \
              '&DISPLAY=points&TEAM=*'
        lis = pd.read_html(url)
        df = lis[1]
        cols = ['Rank','Player','Total','Avg']
        for i in range(1,17):
            cols.append(str(i))
        cols.append('Matchup')
        cols.append('Owner')
        cols.append('Bye')
        df.columns = cols
        df = df.fillna(0.00)
        for col in df.columns:
            for idx in df.index:
                if df[col].loc[idx] == 'B':
                    df[col].loc[idx] = 0.00
        for col in list(range(1,17)):
            for idx in df.index:
                df[str(col)].loc[idx] = float(df[str(col)].loc[idx])
        df = clean_df(df)
        top_scorers[pos] = df
    return top_scorers

def wpa_by_pos(players,replacement_values,mean,std):
    wpa_dict = {}
    for pos in players.keys():
        df = players[pos]
        rep_value = replacement_values[pos]
        wpa_list = []
        for idx in df.index:
            wpa_year = 0
            for week in list(range(1,17)):
                score = df[str(week)].loc[idx]
                if score == 0.0:
                    score = rep_value
                diff = score - rep_value
                team_score = mean + diff
                win_prob = norm(mean, std).cdf(team_score)
                wpa = win_prob - 0.5
                wpa_year += wpa
            wpa_list.append(wpa_year)
        df['WPA'] = wpa_list
        wpa_dict[pos] = df
    return wpa_dict

def avg_team():
    url = 'https://www55.myfantasyleague.com/2022/options?L=29667&O=15'
    lis = pd.read_html(url)
    df = lis[1]
    droppable = []
    for idx in df.index:
        if df['Score'].iloc[idx] == 'Score':
            droppable.append(idx)
    df = df.drop(droppable)
    df = df.drop(list(range(237,244)))
    df = df.reset_index(drop=True)
    for idx in df.index:
        df['Score'].iloc[idx] = float(df['Score'].iloc[idx]) * 1.20
    all_scores = df['Score'].tolist()
    mean = np.mean(all_scores)
    stdev = np.std(all_scores)
    return mean, stdev

def wpa_all_pos(wpa_dict):
    d = wpa_dict['QB']
    all = pd.DataFrame(columns=d.columns)
    for pos in wpa_dict.keys():
        df = wpa_dict[pos]
        for idx in df.index:
            all.loc[len(all.index)] = df.loc[idx]
    all = all.sort_values(by=['WPA'],ascending=False)
    all = all.reset_index(drop=True)
    all = all.drop(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'
                     , 'Matchup', 'Owner', 'Bye'], axis=1)
    return all

def prepare_to_plot(wpa_dict):
    x, y, sizes = [], [], []
    temp_x = 1
    for pos in wpa_dict.keys():
        df = wpa_dict[pos]
        y.extend(df['WPA'].tolist())

    for j in range(1,10):
        for i in range(0,64):
            x.append(temp_x)
            sizes.append(3)
        temp_x += 1

    return x, y, sizes

def dict_to_df(dict):
    df = pd.DataFrame(columns=['QB', 'RB', 'WR', 'TE', 'DT', 'DE', 'LB', 'CB', 'S'])
    for pos in dict.keys():
        pos_df = dict[pos]
        df[pos] = pos_df['WPA'].tolist()
    return df

def avg_dfs(dict):
    df = pd.DataFrame(data=dict[2022], columns=dict[2022].columns)
    for pos in df.columns:
        for idx in dict[2022].index:
            total = 0
            for year in dict.keys():
                df2 = dict[year]
                total += df2[pos].loc[idx]
                df[pos].loc[idx] = total / 3
    return df

def waiver_replacement_values(waivers):
    rep_values = {}
    for pos in waivers.keys():
        df = waivers[pos]
        if pos == 'QB':
            rep = np.mean(df['Avg'].tolist())
        else:
            rep = (df['Avg'].loc[4] + df['Avg'].loc[5] + df['Avg'].loc[6] + df['Avg'].loc[7]) / 4
        rep_values[pos] = rep
    return rep_values

def get_weekly_df(year,week,is_offense):
    if is_offense:
        url = 'https://www55.myfantasyleague.com/2022/top?L=45889&SEARCHTYPE=BASIC&COUNT=300' \
              '&YEAR=' + str(year) + '&START_WEEK=' + str(week) + '&END_WEEK=' + str(week) + \
              '&CATEGORY=overall&POSITION=RB%7CWR%7CTE&DISPLAY=points&TEAM=*&SORT=TOT'
        lis = pd.read_html(url)
        df = lis[1]
        df.columns = ['Rank','Player','Pts','Avg','Total','Status','Bye','None']
        df = df.drop(['Rank','Avg','Total','Status','Bye','None'], axis=1)
        df = clean_df(df)
    else:
        url = 'https://www55.myfantasyleague.com/2022/top?L=45889&SEARCHTYPE=BASIC&COUNT=300' \
              '&YEAR=' + str(year) + '&START_WEEK=' + str(week) + '&END_WEEK=' + str(week) + \
              '&CATEGORY=overall&POSITION=DT%7CDE%7CLB%7CCB%7CS&DISPLAY=points&TEAM=*&SORT=TOT'
        lis = pd.read_html(url)
        df = lis[1]
        df.columns = ['Rank','Player','Pts','Avg','Total','Status','Bye','None']
        df = df.drop(['Rank','Avg','Total','Status','Bye','None'], axis=1)
        df = clean_df(df)
    return df

