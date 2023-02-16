from functions import *

def main():
    rosters = get_rosters()
    ratios = evaluate_rosters(rosters)
    total_rostered = num_rostered(ratios)

    offense = get_offense()
    defense = get_defense()
    big_dict = divide_pos(offense,defense)
    sorted_players = big_dict[2022]

    waivers = get_waivers(total_rostered,sorted_players)

main()
