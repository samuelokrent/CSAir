# CSAir

This project was an assignment for a UIUC course. It includes an implementation of the Graph ADT, as well as a command line interface that manages a fake air transportation network called CSAir.

## Try it out

Run `python src/csair.py` to launch the CLI.

Enter `help` to view a list of the CLI's functionality:

```
h                           : prints this message
list_cities                 : lists all available cities
show <CODE> [FIELD]         : displays info about city with code CODE
longest_flight              : displays the longest flight available
shortest_flight             : displays the shortest flight available
average_flight              : displays the average flight distance
biggest_city                : displays the largest city by population
smallest_city               : displays the smallest city by population
average_population          : displays the average city population
list_continents             : lists all available continents with their available cities
hubs [NUM]                  : lists NUM biggest hub cities
visualize                   : opens a map visualizer in browser
add_city <CODE> <JSON_DATA> : adds a city to the map
remove_city <CITY>          : removes city with code CODE from the map
edit_city <C> <KEY> <VAL>   : updates KEY of city with code C to be VAL
add_route <SRC> <DST> <LEN> : adds a flight between SRC and DST
remove_route <SRC> <DST>    : removes the flight between SRC and DST
route_info <CITIES...>      : displays info regarding the route represented by the list CITIES
shortest_path <SRC> <DST>   : displays the shortest route between SRC and DST
load <FILE>                 : loads the json data in FILE into the map
save [FILE]                 : saves the map in json form to FILE, if provided, or to saved state if not
exit                        : exits the CLI
```
