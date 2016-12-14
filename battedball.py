import numpy as np
import matplotlib.pyplot as plt
# import scipy as sp
from scipy import stats

import json

# global dictionaries
# pdict: conversion of json file to dictionary of players and their batted ball numbers
# statdict: stores certain playerbase stats, i.e. number of players in pdict
pdict = {}
statdict = {}

# merging list of free agents with dictionary
# if player is a free agent, change their free agent status to True
def merge_fas():
    falist = open('fullfalist.txt')
    for fa in falist:
        f_a = fa.strip('\r\n')
        if f_a in pdict:
            player = pdict[f_a]
            player['freeagent'] = True      # this actually changes the value of the player in pdict
# end merge_fas

# opens the json file and creates a dictionary
# working with static jason file 'playerlist.json'
# playerlist.json retrieved from page source at https://baseballsavant.mlb.com/statcast_leaderboard
# query: minimum batted balls events of 30, season 2016
# would be better if json file is specified from user, but this is just for fun :)
def parse_and_dict():
    # just change the filename to read the whole json
    # working on a smaller subset to save speed
    json1_file = open('playerlist.json')
    json1_str = json1_file.read()

    # json.loads turns the json into a list of dictionaries
    json1_data = json.loads(json1_str)  # gets the whole dictionary
    playercounter = 0
    mavahs_name = ""
    minahs_name = ""
    mavahs = 0
    minahs = 100
    league_ahs = 0

    # populate the dictionary
    for player in json1_data:
        pname = player['name']

        # to int: avg_distance, avg_hr_distance, batter, max_distance, player_id
        player['avg_distance'] = int(player['avg_distance'])
        ahd = str(player['avg_hr_distance'])                # manually changed null to "null" in list
        if ahd.lower() == 'null':               # sometimes ahd is null; players w/o hr
            player['avg_hr_distance'] = 0
        else:
            player['avg_hr_distance'] = int(player['avg_hr_distance'])
        player['batter'] = int(player['batter'])
        player['max_distance'] = int(player['max_distance'])
        player['player_id'] = int(player['player_id'])

        # to float: avg_hit_speed, brl_pa(%), brl_percent(%), fbld, gb, max_hit_speed, min_hit_speed
        player['avg_hit_speed'] = float(player['avg_hit_speed'])
        league_ahs = league_ahs + player['avg_hit_speed']
        player['brl_pa'] = float(player['brl_pa'].strip('%')) / 100
        player['brl_percent'] = float(player['brl_percent'].strip('%')) / 100
        player['fbld'] = float(player['fbld'])
        player['gb'] = float(player['gb'])
        player['max_hit_speed'] = float(player['max_hit_speed'])
        player['min_hit_speed'] = float(player['min_hit_speed'])

        # to bool: freeagent
        if player['freeagent'].lower() == 'true':
            player['freeagent'] = True
        else:
            player['freeagent'] = False

        # dictionary population
        # sets a player's value in the dictionary
        pdict[pname] = player
        playercounter += 1
        if player['avg_hit_speed'] > mavahs:
            mavahs = player['avg_hit_speed']
            mavahs_name = pname
        if player['avg_hit_speed'] < minahs:
            minahs = player['avg_hit_speed']
            minahs_name = pname

        # debugging statements
        # pseason = str(player['season'])     # season is treated as an int
        # pmhs = player['max_hit_speed']
        # print "in " + pseason + ", " + pname + " had max hit speed of " + str(pmhs)

        # end loop
    # more code
    statdict['pc'] = playercounter
    statdict['max_avg_hs'] = {}
    statdict['min_avg_hs'] = {}
    sdmax = statdict['max_avg_hs']  # useful when creating plots
    sdmax['speed'] = mavahs
    sdmax['name'] = mavahs_name
    sdmin = statdict['min_avg_hs']  # useful when creating plots
    sdmin['speed'] = minahs
    sdmin['name'] = minahs_name
    statdict['league_ahs'] = float('%.2f' % (league_ahs / playercounter))   # truncate the float
# end parse_and_dict

def fa_to_plot():
    print 'hi'
    fastr = "Free Agent"
    notfastr = "Contracted Player"
    facolor = 'red'
    defcolor = 'blue'
    numplayers = statdict['pc']

    # for line of best fit, two arrays of equal size created
    # one array corresponding to the x-value, the other with y-values
    lobf_x = np.zeros(numplayers, dtype=np.int)
    lobf_y = np.zeros(numplayers, dtype=np.int)
    fa_to_plot_counter = 0

    fa_c = 0        # free_agent counter: used to set the legend
    nfa_c = 0       # not free agent counter: used to set the legend

    for key in pdict:
        player = pdict[key]
        if player['brl_pa'] != 0:
            if player['freeagent']:
                if fa_c == 1:
                    plt.scatter(player['avg_hit_speed'], player['brl_pa'], marker='D', c=facolor)
                else:
                    plt.scatter(player['avg_hit_speed'], player['brl_pa'], marker='D', c=facolor, label=fastr)
                    fa_c = 1
                lobf_x[fa_to_plot_counter] = player['avg_hit_speed']
                lobf_y[fa_to_plot_counter] = player['brl_pa']
            else:
                if nfa_c == 1:
                    plt.scatter(player['avg_hit_speed'], player['brl_pa'], c=defcolor)
                else:
                    plt.scatter(player['avg_hit_speed'], player['brl_pa'], c=defcolor, label=notfastr)
                    nfa_c = 1
                lobf_x[fa_to_plot_counter] = player['avg_hit_speed']
                lobf_y[fa_to_plot_counter] = player['brl_pa']
        fa_to_plot_counter += 1
    lr_array = stats.linregress(lobf_x, lobf_y)
    xa_lobf = np.linspace(80, 98, 10, dtype=int)
    ya_lobf = lr_array.slope * xa_lobf + lr_array.intercept
    plt.plot(xa_lobf,ya_lobf)
    plt.xlabel('Average Hit Speed')
    plt.ylabel('Barrels/PA')
    plt.legend(loc='upper left', scatterpoints=1)
    plt.grid(True)
    plt.show()
#end plotter

# the main machine
def main():
    # dictionary is a lot faster than list
    # will be useful when updating a player's FA stats
    # dictionary AO(1) speed to update, access
    # list is O(n) update, access

    # populate pdict
    parse_and_dict()

    # to check if item is in dict, do this: ITEM in dict_name
    gsname = "Giancarlo Stanton"
    if gsname in pdict:
        gs1 = pdict[gsname]
        print str(gs1['name']) + " had an average speed of " + str(gs1['gb']) + " mph on his groundballs"
    else:
        print gsname + " isn't in the dictionary"
    if 'Bob Sutton' in pdict:
        print "how??"
    else:
        print "Bob Sutton not in the dictionary"

    pcname = "pc"
    if pcname in statdict:
        print "There are " + str(statdict[pcname]) + " players recorded"
    else:
        print pcname + " isn't in the stat dictionary"

    merge_fas()
    fa_to_plot()
    # debugging statement
    # for key in pdict:
    #    player = pdict[key]
    #    if player['freeagent']:
    #        print player['name'] + " is a free agent"

# end main

# run program
main()
