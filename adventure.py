# The following functions implement interesting solutions to the
# handlers below, but should be removed from this file before
# getting pasted into the default code for the Codecademy exercise.
# The references from those handlers to these functions also need
# to be removed, of course and any default behavior restored
# (search for "_soln").
# This file can be pasted as is into the solution to the exercise.

def print_room_description_soln(room_name):

    # Retrieve the current room by name
    room = g_rooms[room_name]

    # Print the room's description
    print room['description']

def print_room_items_soln(room_name):

    # Get the current room by name
    room = g_rooms[room_name]

    # Get the room's item list
    item_names = room['item_names']

    # Print a comma-separated list of the room's items, if any
    # otherwise print "the room is empty"
    if (item_names):
        items_text = "the room contains the following items: "
        for item_name in item_names:
            items_text += (item_name + ", ")
        items_text = items_text[:-2] # remove that last comma & space
    else:
        items_text = "the room is empty"
    print items_text

def check_move_command_soln(room_name, command):

    # Get the current room by name
    room = g_rooms[room_name]

    # See if command is the name of a door in this room.
    doors = room['doors']

    # If so, return the name of the new room, otherwise return None.
    if doors.has_key(command):
        return doors[command]
    return None

def take_item_command_soln(room_name, command):
    global g_rooms
    global g_inventory

    # command should be "take xxx", where xxx is the name of an
    # item in the room.
    item_name = command[len('take'):].strip()

    # If it's just "take" then return an appropriate
    # error message.
    if (not item_name):
        return "You didn't specify what to take"

    # Get the current room by name
    room = g_rooms[room_name]

    # Get the room's item list
    room_item_names = room['item_names']

    # If xxx isn't the name of an item in the room, then
    # return a different error message.
    if (room_item_names.count(item_name) == 0):
        return "There is no %s in this room" % item_name

    # Otherwise, move the item from the room's list of items,
    # add the item to the player's inventory,
    # and return a string that says "you now have the xxx"
    room_item_names.remove(item_name)
    g_inventory.append(item_name)
    return "You now have the %s" % item_name

    return None

def move_to_room_soln(room_name):
    global g_current_room_name
    global g_score

    # Update the global current room name.
    g_current_room_name = room_name

    # If this is the first time in this room (check visited_rooms) then
    # add the room's score to the player's score, and return a msg
    # about how many points they've earned.
    if (g_visited_room_names.count(room_name) == 0):

        # Get the new room by name
        room = g_rooms[room_name]

        # The player has earned the new room's value
        room_value = room['value']
        g_score += room_value

        # Congratulate the player on his/her progress
        if (room_value):
            return "You just earned %s points for a total of %s" % (room_value, g_score)
        else:
            return "This room has no extra value, so your score remains %s" % g_score

    return None


# End of solution code

def print_intro():
    # TODO print an introduction to the game, with some helpful hints
    print "intro"

def print_help():
    # TODO print help text
    print "help"

def game_complete():
    # TODO decide when to congratulate user and return True
    return False

def print_goodbye(score):
    # TODO print goodbye text, along with the player's current score
    print "goodbye: ", score

def print_room_description(room_name):
    # TODO print the room's description
    print_room_description_soln(room_name)
    # print "room description"

def print_room_items(room_name):
    # TODO print a list of items in the room, if there are any
    print_room_items_soln(room_name)
    # print "room items"

def print_inventory():
    # TODO print a list of the item names that the user has
    print "inventory"

def check_move_command(room_name, command):
    # TODO see if this is the name of a door in this room.
    # If so, return the name of the new room, otherwise return None
    return check_move_command_soln(room_name, command)
    # return None

def check_item_command(room_name, command):
    # TODO see if we have a function for handling item-specific commands
    # If so, call it, and return its result string (which can be None)
    return None

def check_general_command(room_name, command):
    # TODO see if the command is one that we want to respond to, without
    # doing anything. E.g. if they're swearing at us, tell them to keep
    # it clean. If we don't have any match, return None
    return None

def has_item(item):
    # TODO return true if the user has the item, otherwise false.
    return g_inventory.count(item) > 0

def key_command(room_name, command):
    # TODO see if this is a specific command for the key.
    # E.g. use key or "turn key" in the appropriate room
    # If so, return a string indicating the result of the
    # command, otherwise return None
    if command == "turn key":
        # TODO check if the user has the key. If not, return a string
        # that tells they they don't have the key. Otherwise...
        if not has_item("key"):
            return "You need to get the key first"

        if room_name == "hallway":
            # TODO set the computerlab room's "locked" attribute to
            # False.
            return "I just unlocked the door"
        else:
            return "I don't see any lock around here"
    else:
        return None

def notebook_command(room_name, command):
    # TODO see if this is a specific command for the notebook.
    # E.g. "read notebook"
    # If so, return a string indicating the result of the
    # command, otherwise return None
    return None

def move_to_room(room_name):
    global g_current_room_name
    global g_score

    # TODO set the current_room to be room.
    # If this is the first time in this room (check visited_rooms) then
    # add the room's score to the player's score, and return a msg
    # about how many points they've earned.
    return move_to_room_soln(room_name)
    #g_current_room_name = room_name
    #return None

def take_item_command(room_name, command):
    global g_inventory # not rebound, but contents changed
    global g_rooms # not rebound, but contents changed

    # TODO command should be "take xxx", where xxx is the name of an
    # item in the room. If it's just "take" then return an appropriate
    # error message. If xxx isn't the name of an item in the room, then
    # return a different error message. Otherwise move the item from
    # the room's list of items, and put it into the player's inventory,
    # and return a string that says "you now have the xxx"
    return take_item_command_soln(room_name, command)
    #return None

def drop_item_command(room_name, command):
    # TODO command should be "drop xxx", where xxx is the name of an
    # item in the player's inventory. If it's just "drop" then return
    # an appropriate error message. If xxx isn't the name of an item
    # in the player's inventory, then return a different error message.
    # Otherwise move the item from the player's inventory to the room's
    # list of items, and return a string that says "you no longer have
    # the xxx"
    return None

# This is a list of items that player has picked up. It starts off
# as empty
g_inventory = []

# This is the name of the current room that the player is in.
g_current_room_name = None

# This is a list of all of names of all the rooms that the player has visited.
# It starts off with just the current room that they're in.
g_visited_room_names = []

# This is the player's current score. They get points for visiting a room
# (but only the first time!)
g_score = 0

# This is a boolean variable. When it's set to False, the game should
# exit the main loop below.
g_keep_going = True

# rooms is a dictionary, where the key is the room name, and the value is a "room"
# Each room is also a dictionary, where the key is one of several possible values
#   description -> string that describes the room
#   items -> list of item names for items found in that room
#   value -> points for visiting the room
#   doors -> dictionary that maps from a door name ("north", "up", etc) to a room name
#
# You can also have other room-specific attributed, e.g. the computer lab could have
# a "locked": True attribute, and you have to unlock it first before you can go through
# that door. Use your imagination.

g_rooms = {"computerlab":
             {"description": "The computer lab is filled with glowing screens and old chairs",
              "item_names": ["notebook"],
              "value": 5,
              "doors": {"exit": "hallway"}},
         "hallway":
             {"description": "The hallway is filled with colorful murals",
              "item_names": [],
              "value": 0,
              "doors": {"north": "computerlab", "east": "lobby"}}
}

# items is a dictionary, where the key is the item name, and the value is an "item"
# Each item is also a dictionary, where the key is one of several possible values
#   description -> string that describes the item
#   action -> function that checks for item-specific actions
#   takeable -> boolean for whether the item can be taken or not.
#   room -> room name where item exists (so its starting location). This is set to
#           None when the item has been taken by the person.

g_items = {"notebook":
             {"description": '''notebook containing all kinds of complex diagrams, equations, assignments
(many with very low grades), etc. in a completely random order. None of the pages have any students names
on them, but Mr. Schneider has obviously written in the name "Peggy???" in red ink on several of the graded assignments.''',
              "action": notebook_command,
              "takeable": True,
              "room": "computerlab"},
         "key":
             {"description": "small, nondescript key",
              "action": key_command,
              "takeable": True,
              "room": "hallway"}
}

# ============================================================
# Start of the main game
# ============================================================

print_intro()

print move_to_room("hallway")

while g_keep_going and (not game_complete()):
    print_room_description(g_current_room_name)
    print_room_items(g_current_room_name)

    # Get the user's command
    command = raw_input("> ")

    # See if the command is one of our special commands.
    if command == "bye":
        print_goodbye(g_score)
        g_keep_going = False
        continue

    if command == "help":
        print_help()
        continue

    if command == "list":
        print_inventory()
        continue

    if command.startswith("take"):
        print take_item_command(g_current_room_name, command)
        continue

    if command.startswith("drop"):
        print drop_item_command(g_current_room_name, command)
        continue

    # See if the command is the name of a door
    next_room = check_move_command(g_current_room_name, command)
    if next_room != None:
        # Go to the new room
        print move_to_room(next_room)
        continue

    # See if the command is an action on an item the user
    # has, in the appropriate room
    action_result = check_item_command(g_current_room_name, command)
    if action_result != None:
        print action_result
        continue

    # See if the command is something we want to respond to
    # with special text
    action_result = check_general_command(g_current_room_name, command)
    if action_result != None:
        print action_result
        continue;

    # No idea what they want to do
    print("I'm not sure what you want me to do")

