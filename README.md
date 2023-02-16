# HolyGrailAnalysis

This project is focused on analyzing my latest fantasy football league format to find the best strategy.

The basics of the format are:
12 Teams
Auction + Salary Cap
40 man roster
Start 10 on offense, 12 on defense
Superflex, TE Premium, Point Per Carry, Weighted Scoring for each defensive position

functions.py:
  Contains all helper functions used in the other files

med_avg.py:
  Calculates the median average PPG for each spot in a team's starting lineup.
  Calculates the rate at which FLEX spots are filled by RB, WR, or TE.
  Calculates the rate at which DFLEX spots are filled by DT, DE, LB, CB, or S.
  Results are presented in pandas dataframes.

waivers.py:
  Uses data from my other leagues to estimate the PPG from the top players on waivers.
  These values are used to calculate WoW (Wins Over Waivers).

worp.py:
  Calculates the WORP (Wins Over Replacement Player) for the top 64 scorers at each position over the last 3 years.
  Uses bench players as replacement value.
  Averages these dataframes and exports to excel.
  
wow.py:
  Calculates the WOW (Wins Over Waivers) for the top 64 scorers at each position over the last 3 years.
  Uses waivers as replacement value.
  Averages these dataframes and exports to excel.
  
auction.py:
  Attempts to use WORP/WOW values to estimate the player's value in relation to the salary cap.
