#import numpy
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
# would be safer if json file is specified from user, but this is just for fun :)
def parse_and_dict():
    # just change the filename to read the whole json
    # working on a smaller subset to save speed
    json1_file = open('playerlist.json')
    json1_str = json1_file.read()

    # json.loads turns the json into a list of dictionaries
    json1_data = json.loads(json1_str)  # gets the whole dictionary
    playercounter = 0

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

        # sets a player's value in the dictionary
        pdict[pname] = player
        playercounter += 1

        # debugging statements
        # pseason = str(player['season'])     # season is treated as an int
        # pmhs = player['max_hit_speed']
        # print "in " + pseason + ", " + pname + " had max hit speed of " + str(pmhs)

        # end loop
    # more code
    statdict['pc'] = playercounter
# end parse_and_dict


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
        print "there are " + str(statdict[pcname]) + " players recorded"
    else:
        print pcname + " isn't in the stat dictionary"

    merge_fas()
    # debugging statement
    # for key in pdict:
    #    player = pdict[key]
    #    if player['freeagent']:
    #        print player['name'] + " is a free agent"

# end main

# run program
main()
