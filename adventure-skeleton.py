def print_intro():
    # Level - 1

    # TODO print an introduction to the game, with some helpful hints

    print "intro"

def print_help():
    # Level - 2

    # TODO print help text

    print "help"

def print_goodbye():
    # Level - 2

    global g_score

    # TODO print goodbye text, along with the player's current score

    print "goodbye: ", g_score

def print_room_description(room_name):
    # Level - 4

    global g_rooms

    # TODO print the room's description

    print "room description"

def print_items():
    # Level - 5

    global g_player_items

    # TODO print a list of the item names that the player has, which
    # means a loop that iterates over the g_game_items list, and prints
    # out the list. If the player has nothing, print "You've got nothing"

    print "You've got nothing"

def check_move_command(room_name, command):
    # Level - 4

    global g_rooms

    # TODO see if this is the name of a door in this room.
    # If so, return the name of the new room, otherwise return None

    return None

def check_general_command(room_name, command):
    # Level - 2

    # TODO see if the command is one that we want to respond to, without
    # doing anything. E.g. if they're swearing at us, tell them to keep
    # it clean. If we don't have any match, return None. This should handle
    # all of the cases for an action without an item name, e.g. the user
    # enters "take" without saying what they want to take.

    if command.startswith("hit "):
        print "There's no violence allowed at Bitney!"
        return True
    else:
        return False

def move_to_room(room_name):
    # Level - 5

    global g_current_room_name
    global g_visited_room_names
    global g_score

    # TODO set the current_room to be room.
    # If this is the first time in this room (check visited_rooms) then
    # add the room's score to the player's score, and let them know they
    # just earned some additional points. Also print out the room's
    # description if it's the first time, otherwise just the room name.


def take_item_command(room_name, command):
    # Level - 5

    global g_player_items
    global g_rooms

    # First use the handy-dandy get_item_name utility routine to extract
    # the item name from the command.
    item_name = get_item_name("take", command)

    # TODO command will be "take xxx", where xxx is the name of an
    # item in the room. If xxx isn't the name of an item in the room, then
    # print an error message. Otherwise move the item from
    # the room's list of items, and put it into the player's list of items (g_player_items),
    # and print a string that says "you now have the xxx". Though
    # you only want to do this if the item is takeable!

    print "I don't know how to take " + item_name

def examine_item_command(room_name, command):
    # Level - 3

    global g_player_items
    global g_game_items

    # First use the handy-dandy get_item_name utility routine to extract
    # the item name from the command.
    item_name = get_item_name("take", command)

    # TODO if item_name isn't in the player's
    # list of items, print an error message. Otherwise print
    # the item's description. You can use the player_has_item(item_name)
    # function to help with this.

    print "I don't know how to examine " + item_name

def drop_item_command(room_name, command):
    # Level - 5

    global g_player_items
    global g_rooms

    # First use the handy-dandy get_item_name utility routine to extract
    # the item name from the command.
    item_name = get_item_name("take", command)

    # TODO command should be "drop xxx", where xxx is the name of an
    # item in the player's list of items. If xxx isn't the name of an item
    # in the player's list of items, then print a an error message.
    # Otherwise move the item from the player's list of items to the room's
    # list of items, and print a string that says "you no longer have
    # the xxx"

    print "I don't know how to drop " + item_name

def check_item_command(room_name, command):
    # Level - 5

    # TODO see if the command is for any of the items in the player's
    # list of items. If so, print out an appropriate message, and do
    # the action, and return True so that we know the command has been
    # handled.

    if command == "eat donut":
        if not player_has_item("donut"):
            print "You don't have anything to eat"
        else:
            # TODO you need to remove the donut from the player's list of
            # items, because they've eaten it.
            print "Yum, that was tasty!"

        # We handled the command, so return True
        return True
    else:
        # We didn't handle the command, so return False
        return False

def game_complete():
    # Level - 3

    global g_visited_room_names
    global g_score

    # TODO decide when to congratulate user and return True. This would
    # be the case for when they've visited every room. So you can either
    # compare their score against the sum of scores from every room, or
    # if the g_visited_room_names list length is == the number of rooms.

    return False

# This is a handy utility routine that you give an action (like "take")
# and a command (like "take key"), and it returns just the item (e.g. "key")
def get_item_name(action, command):
    if command.startswith(action + " "):
        return command[len(action) + 1:]
    else:
        return None

# This is a handy utility routine that you give an item name (like "key")
# and it returns True if the user has that item, otherwise False.
def player_has_item(item_name):
    global g_player_items

    # Return true if the user has the item, otherwise false.
    return g_player_items.count(item_name) > 0


# This is a list of names of items that player has taken. It starts off
# as empty. When you take an item, it gets added to this list, and when
# you drop an item, it gets removed from this list.
g_player_items = []

# This is the name of the current room that the player is in.
g_current_room_name = None

# This is a list of all of names of all the rooms that the player has visited.
# It starts off with just the current room that they're in.
g_visited_room_names = []

# This is the player's current score. They get points for visiting a room
# (but only the first time!)
g_score = 0

# rooms is a dictionary, where the key is the room name, and the value is a "room"
# Each room is also a dictionary, where the key is one of several possible values
#   description -> string that describes the room. This should include all doors.
#   items -> list of item names for items found in that room
#   value -> points for visiting the room
#   doors -> dictionary that maps from a door name ("north", "up", etc) to a room name
#
# You can also have other room-specific attributed, e.g. the computer lab could have
# a "locked": True attribute, and you have to unlock it first before you can go through
# that door. Use your imagination.

g_rooms = {"computer lab":
             {"description": "The computer lab is filled with glowing screens and old chairs. There is a door to the south",
              "items": ["notebook"],
              "value": 5,
              "doors": {"south": "hallway"}},
         "hallway":
             {"description": "The hallway is filled with colorful murals. There are doors to the north and east",
              "items": ["key"],
              "value": 0,
              "doors": {"north": "computer lab", "east": "lobby"}},
         "lobby":
             {"description": "The lobby is a place where people go to chill. There is a door to the west",
              "items": [],
              "value": 2,
              "doors": {"west": "hallway"}},
}

# items is a dictionary, where the key is the item name, and the value is an "item"
# Each item is also a dictionary, where the key is one of several possible values
#   description -> string that describes the item
#   takeable -> boolean for whether the item can be taken or not.
#
# You can also have other item-specific attributed, e.g. a bottle of water could have
# an "empty": False attribute, and this changes to True after you've had a drink.
# Use your imagination.

g_game_items = {"notebook":
             {"description":
'''notebook containing all kinds of complex diagrams, equations, assignments
(many with very low grades), etc. in a completely random order. None of the
pages have any students names on them, but Mr. Schneider has obviously written
in the name "Peggy???" in red ink on several of the graded assignments.''',
              "takeable": True},
         "key":
             {"description": "small, nondescript key",
              "takeable": True}
}

# ============================================================
# Start of the main game
# ============================================================

# Print out the welcome message
print_intro()

# Start the player in the hallway. Which is why this room isn't worth
# any points, as you get there automatically.
move_to_room("hallway")

# Keep looping until the game is complete (or the user enters "bye")
while not game_complete():
    # Print an empty line
    print("")

    # Get the user's command
    command = raw_input("> ")

    # See if the command is one of our special commands.
    if command == "bye":
        # Print a goodbye message, and then break out of the loop, thus
        # ending the game.
        print_goodbye()
        break

    if command == "help":
        print_help()
        continue

    if command == "list":
        print_items()
        continue

    if command == "look":
        print_room_description(g_current_room_name)
        continue

    if command.startswith("take "):
        take_item_command(g_current_room_name, command)
        continue

    if command.startswith("drop "):
        drop_item_command(g_current_room_name, command)
        continue

    if command.startswith("examine "):
        examine_item_command(g_current_room_name, command)
        continue

    # See if the command is the name of a door
    next_room = check_move_command(g_current_room_name, command)
    if next_room != None:
        # Go to the new room
        move_to_room(next_room)
        continue

    # See if the command is an action on an item the user
    # has, in the appropriate room
    if check_item_command(g_current_room_name, command):
        continue

    # See if the command is something we want to respond to
    # with special text
    if check_general_command(g_current_room_name, command):
        continue

    # No idea what they want to do
    print("I don't understand that")

