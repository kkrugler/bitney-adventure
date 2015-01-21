def print_intro():
    # TODO print an introduction to the game, with some helpful hints
    print "intro"

def print_help():
    # TODO print help text
    print "help"

def print_goodbye(score):
    # TODO print goodbye text, along with the player's current score
    print "goodbye: ", score

def print_room_description(room_name):
    # TODO print the room's description
    print "room description"

def print_room_items(room_name):
    # TODO print a list of items in the room, if there are any
    print "room items"

def print_inventory():
    # TODO print a list of the item names that the user has
    print "inventory"

def check_move_command(room, command):
    # TODO see if this is the name of a door in this room.
    # If so, return the name of the new room, otherwise return None
    return None

def check_item_command(room, command):
    # TODO see if we have a function for handling item-specific commands
    # If so, call it, and return its result string (which can be None)
    return None

def check_general_command(room, command):
    # TODO see if the command is one that we want to respond to, without
    # doing anything. E.g. if they're swearing at us, tell them to keep
    # it clean. If we don't have any match, return None
    return None

def has_item(item):
    # TODO return true if the user has the item, otherwise false.
    return inventory.count(item) > 0

def key_command(room, command):
    # TODO see if this is a specific command for the key.
    # E.g. use key or "turn key" in the appropriate room
    # If so, return a string indicating the result of the
    # command, otherwise return None
    if command == "turn key":
        # TODO check if the user has the key. If not, return a string
        # that tells they they don't have the key. Otherwise...
        if not has_item("key"):
            return "You need to get the key first"

        if room == "hallway":
            # TODO set the computerlab room's "locked" attribute to
            # False.
            return "I just unlocked the door"
        else:
            return "I don't see any lock around here"
    else:
        return None

def notebook_command(room, command):
    # TODO see if this is a specific command for the notebook.
    # E.g. "read notebook"
    # If so, return a string indicating the result of the
    # command, otherwise return None
    return None

def move_to_room(room):
    # TODO set the current_room to be room.
    # If this is the first time in this room (check visited_rooms) then
    # add the room's score to the player's score, and return a msg
    # about how many points they've earned.
    current_room = room
    return None

def take_item_command(room, command):
    # TODO command should be "take xxx", where xxx is the name of an
    # item in the room. If it's just "take" then return an appropriate
    # error message. If xxx isn't the name of an item in the room, then
    # return a different error message. Otherwise move the item from
    # the room's list of items, and put it into the player's inventory,
    # and return a string that says "you now have the xxx"
    return None

# This is a list of items that player has picked up. It starts off
# as empty
inventory = []

# This is the name of the current room that the player is in.
current_room = None

# This is a list of all of names of all the rooms that the player has visited.
# It starts off with just the current room that they're in.
visited_rooms = []

# This is the player's current score. They get points for visiting a room
# (but only the first time!)
score = 0

# This is a boolean variable. When it's set to False, the game should
# exit the main loop below.
keep_going = True

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

rooms = {"computerlab":
             {"description": "The computer lab is filled with glowing screens and old chairs",
              "items": ["notebook"],
              "value": 0,
              "doors": {"exit": "hallway"}},
         "hallway":
             {"description": "The hallway is filled with colorful murals",
              "items": [],
              "value": 5,
              "doors": {"north": "computerlab", "east": "lobby"}}
}

# items is a dictionary, where the key is the item name, and the value is an "item"
# Each item is also a dictionary, where the key is one of several possible values
#   description -> string that describes the item
#   action -> function that checks for item-specific actions
#   takeable -> boolean for whether the item can be taken or not.
#   room -> room name where item exists (so its starting location). This is set to
#           None when the item has been taken by the person.

items = {"notebook":
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

move_to_room("hallway")

while keep_going:
    print_room_description(current_room)
    print_room_items(current_room)

    # Get the user's command
    command = raw_input("> ")

    # See if the command is one of our special commands.
    if command == "bye":
        print_goodbye(score)
        keep_going = False
        continue

    if command == "help":
        print_help()
        continue

    if command == "list":
        print_inventory()
        continue

    if command.startswith("take"):
        print take_item_command(current_room, command)
        continue

    if command.startswith("drop"):
        print drop_item_command(current_room, command)
        continue

    # See if the command is the name of a door
    next_room = check_move_command(current_room, command)
    if next_room != None:
        # Go to the new room
        print move_to_room(next_room)
        continue

    # See if the command is an action on an item the user
    # has, in the appropriate room
    action_result = check_item_command(current_room, command)
    if action_result != None:
        print action_result
        continue

    # See if the command is something we want to respond to
    # with special text
    action_result = check_general_command(current_room, command)
    if action_result != None:
        print action_result
        continue;

    # No idea what they want to do
    print("I'm not sure what you want me to do")

