from csair_map import Map
from os import path
import webbrowser
import graph_parser
import sys

ROOT_DIR = path.dirname(path.dirname(path.realpath(__file__)))
DEFAULT_DATAFILE = "%s/data/map_data.json" % ROOT_DIR
SAVED_STATE_FILE = "%s/data/.saved_state.json" % ROOT_DIR

HELP_MESSAGE =  "h                           : prints this message\n" + \
                "list_cities                 : lists all available cities\n" + \
                "show <CODE> [FIELD]         : displays info about city with code CODE\n" + \
                "longest_flight              : displays the longest flight available\n" + \
                "shortest_flight             : displays the shortest flight available\n" + \
                "average_flight              : displays the average flight distance\n" + \
                "biggest_city                : displays the largest city by population\n" + \
                "smallest_city               : displays the smallest city by population\n" + \
                "average_population          : displays the average city population\n" + \
                "list_continents             : lists all available continents with their available cities\n" + \
                "hubs [NUM]                  : lists NUM biggest hub cities\n" + \
                "visualize                   : opens a map visualizer in browser\n" + \
                "add_city <CODE> <JSON_DATA> : adds a city to the map\n" + \
                "remove_city <CITY>          : removes city with code CODE from the map\n" + \
                "edit_city <C> <KEY> <VAL>   : updates KEY of city with code C to be VAL\n" + \
                "add_route <SRC> <DST> <LEN> : adds a flight between SRC and DST\n" + \
                "remove_route <SRC> <DST>    : removes the flight between SRC and DST\n" + \
                "route_info <CITIES...>      : displays info regarding the route represented by the list CITIES\n" + \
                "shortest_path <SRC> <DST>   : displays the shortest route between SRC and DST\n" + \
                "load <FILE>                 : loads the json data in FILE into the map\n" + \
                "save [FILE]                 : saves the map in json form to FILE, if provided, or to saved state if not\n" + \
                "exit                        : exits the CLI"

def get_command():
    """
    :return: the next user input
    """
    return raw_input("\n>> ")

def execute(cmd, airmap):
    """
    execute the user-supplied command, or print a help message
    """
    print
    
    cmds = cmd.split(' ')
    
    if cmds[0] == "h" or cmd[0] == "help":
        print HELP_MESSAGE
    elif cmds[0] == "list_cities":
        print "Cities:\n"
        for city in airmap.city_list():
            print city
    elif cmds[0] == "show":
        print "======== %s ========\n" % cmds[1]
        if len(cmds) > 2:
            info = airmap.city_info(cmds[1], cmds[2])
        else:
            info = airmap.city_info(cmds[1])
        for field in info:
            print "%s: %s" % (field, info[field])
    elif cmds[0] == "longest_flight":
        print "Longest flight: %s to %s (%s)" % airmap.longest_flight()
    elif cmds[0] == "shortest_flight":
        print "Shortest flight: %s to %s (%s)" % airmap.shortest_flight()
    elif cmds[0] == "average_flight":
        print "Average flight distance: %s" % airmap.average_flight()
    elif cmds[0] == "biggest_city":
        print "Largest city: %s (Pop %s)" % airmap.biggest_city() 
    elif cmds[0] == "smallest_city":
        print "Smallest city: %s (Pop %s)" % airmap.smallest_city() 
    elif cmds[0] == "average_population":
        print "Average population: %s" % airmap.average_population()
    elif cmds[0] == "list_continents":
        print "Continents:\n"
        print airmap.continent_list()
    elif cmds[0] == "hubs":
        if len(cmds) > 1:
            hubs = airmap.hubs(int(cmds[1]))
        else:
            hubs = airmap.hubs()
        print "Hubs and # of direct connections:\n"
        for hub in hubs:
            print "%s (%s)" % hub
    elif cmds[0] == "visualize":
        webbrowser.open(airmap.visualizer_url())
    elif cmds[0] == "add_city" and len(cmds) >= 3:
        print airmap.add_city(cmds[1], cmds[2])
    elif cmds[0] == "remove_city" and len(cmds) >= 2:
        print airmap.remove_city(cmds[1])
    elif cmds[0] == "edit_city" and len(cmds) >= 4:
        print airmap.edit_city(cmds[1], cmds[2], cmds[3])
    elif cmds[0] == "add_route" and len(cmds) >= 4:
        print airmap.add_route(cmds[1], cmds[2], cmds[3])
    elif cmds[0] == "remove_route" and len(cmds) >= 3:
        print airmap.remove_route(cmds[1], cmds[2])
    elif cmds[0] == "load" and len(cmds) >= 2:
        print airmap.load_extra(cmds[1])
    elif cmds[0] == "save":
        if len(cmds) == 1:
            print airmap.save(SAVED_STATE_FILE)
        else:
            print airmap.save(cmds[1])
    elif cmds[0] == "route_info" and len(cmds) >= 3:
        print airmap.route_info(cmds[1:])
    elif cmds[0] == "shortest_path" and len(cmds) == 3:
        print airmap.shortest_path(cmds[1], cmds[2])
    else:
        print HELP_MESSAGE

def run_cli():
    """
    starts the main loop of the CSAir CLI
    """
    
    print "\n======== CSAir CLI ========\n"
        
    try:
        if path.isfile(SAVED_STATE_FILE):
            print "\nLoading saved state..."
            # map data is saved in non-symmetric route format
            airmap = Map(SAVED_STATE_FILE, symmetric_routes=False)
        else:
            data_filename = raw_input("Please enter name of map data file \n(default is %s): " % DEFAULT_DATAFILE)
            if data_filename == "":
                data_filename = DEFAULT_DATAFILE    
            print "\nLoading %s..." % data_filename 
            airmap = Map(data_filename, symmetric_routes=True)  
    except:
        e = sys.exc_info()[0]
        print "ERROR loading data file: %s" % e
        sys.exit(1)
    
    print "Loaded."
    print "Enter 'exit' to exit"
    print "Enter 'help' for a list of commands"
    
    cmd = get_command()
    while cmd != "exit":
        execute(cmd, airmap)
        cmd = get_command()
        
    print "Goodbye\n"

    
    
if __name__ == '__main__':
    run_cli()