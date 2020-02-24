from ast import literal_eval
from room import Room
from player import Player
from world import World

import random
random.seed()

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


# Utils
reverse_dir = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}


def on_move(traversal_graph, from_room, to_room, dir=None):
    if to_room.id not in traversal_graph:
        new_room = {'n': None, 's': None, 'w': None, 'e': None}
        exits = to_room.get_exits()

        for exit in exits:
            new_room[exit] = '?'

        traversal_graph[to_room.id] = new_room
    if from_room is not None:
        traversal_graph[from_room.id][dir] = to_room.id
        traversal_graph[to_room.id][reverse_dir[dir]] = from_room.id


def next_moves(traversal_graph, current_room):
    seen = set([current_room.id])
    exits = [{'direction': exit, 'path': []}
             for exit in traversal_graph[current_room.id].items() if exit[1] is not None and exit[1] not in seen]
    random.seed(random.randint(0,1000000))
    random.shuffle(exits)
    while len(exits) > 0:
        current = exits.pop(0)
        if current['direction'][1] == '?':
            current['path'].append(current['direction'][0])
            return current['path']
        else:
            seen.add(current['direction'][1])
            next_exits = [{
                'direction': exit,
                'path': current['path'] + [current['direction'][0]]
            }
                for exit in traversal_graph[current['direction'][1]].items()
                if exit[1] is not None and exit[1] not in seen
            ]
            random.seed(random.randint(0,1000000))
            random.shuffle(next_exits)
            exits = exits + next_exits

def find_path(player):
    player = Player(world.starting_room)

    traversal_path = []
    traversal_graph = {}
    on_move(traversal_graph, None, player.current_room)

    while len(traversal_graph.keys()) != len(world.rooms):
        room = player.current_room
        directions = next_moves(traversal_graph, room)
        for direction in directions:
            traversal_path.append(direction)
            current_room = player.current_room
            player.travel(direction)
            next_room = player.current_room
            on_move(traversal_graph, current_room, next_room, direction)
    return traversal_path

def calculate_move(player, path):
    visited_rooms = set()

    player.current_room = world.starting_room
    visited_rooms.add(player.current_room)

    for move in traversal_path:
        player.travel(move)
        visited_rooms.add(player.current_room)

    if len(visited_rooms) == len(room_graph):
        print(
            f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
    else:
        print("TESTS FAILED: INCOMPLETE TRAVERSAL")
        print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


for i in range(0, 1000): 
    # Fill this out with directions to walk
    # traversal_path = ['n', 'n']
    traversal_path = find_path(player)
    if len(traversal_path) < 980:
        print(len(traversal_path)) #970

        # TRAVERSAL TEST
        calculate_move(player, traversal_path)

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
