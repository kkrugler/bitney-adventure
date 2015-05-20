import textwrap
import re

# TODO - maybe get Dave's help in coming up with content?

# TODO - fix up room descriptions for typos, etc.
# TODO - put back in (part of) Michael's description of Dave's office
# TODO - entering the stall w/deoderant should print different msg the first time you do that
'''TODO - make sure all items play a roll
    you need key (from ???) to unlock storage room to get plunger
    use plunger in stall, voice says "The price has been paid", and you have something in possession...what?
    you need to eat the donut to leave the Bistro, but you have to go to the bistro to get something
    have another locked door besides storage room, but key doesn't work in it
    meme can be swapped for anything, but it then gets put in some random other room. Same thing happens to it
        whenever you pick anything up.
    donut has to magically reappear after being eaten, for other players (The friendly staff at the Bistro put another delicious donut on the plate)

    notebook - has some clue
    note - has a clue about connection between notebook and student
    basketball - if you give this to Mr. Peterson, you get something
    statue - ???
    random number - examining it provides a clue about a locker combo. Do they have those?
    pop tart - ???. Something about exchanging it for the donut?

'''

# Multi-player stuff
# When entering a room, or exiting a room, update every other player's msg queue
# Be able to swap items if player in room with you
# Be able to get a hall pass from Angelina that lets you "swap" for something, but then hall pass disappears
#   But to get the hall pass, you have to answer a question correctly

# TODO - change all xxx_command functions into check_xxx_command functions, so they can
#        be responsible for handling things like "drop the xxx" vs. "drop xxx"
# TODO - use a Player class versus a player dictionary and a bunch of functions
# TODO - use a Room class versus a room dictionary and a bunch of functions
# TODO - use an Item class versus an item dictionary and a bunch of functions
# TODO - catch print calls by trapping stdout ala codecademy framework, and warn if so
# TODO - look needs to handle special description - push that logic into print function?

# TODO - need way to broadcast a msg to everyone when somebody enters a room (everybody in that room gets it)
#        same thing when an item magically appears in a room.

class Player:

    def __init__(self, name):
        self.name = name
        self.room = None
        self.visited_rooms = set()
        self.items = set()
        self.score = 0
        self.msgs = []

    def get_msgs(self):
        return self.msgs

    def remove_msgs(self):
        result = self.msgs
        self.msgs = []
        return result

    def add_msg(self, msg):
        # msg might be coming in with leading spaces before
        # each line, which we want to remove. So use handy
        # regular expression (re) to remove those.
        msg = re.sub("(^|\n)[ ]+", " ", msg)

        # wrap (or re-wrap) msg so that each line (which ends
        # with a \n) will be at most 70 characters long. This
        # will also turn the msg string into a list of strings,
        # one per (wrapped to 70 chars) line.
        msg_lines = textwrap.wrap(msg, 70)

        # Get the player's current list of messages, and add
        # our new list of messages.
        self.msgs += msg_lines

        # Add a blank line between each group of lines that
        # get added.
        self.msgs += [""]

        # Limit the player's messages to at most 20 lines.
        self.msgs = self.msgs[-20:]

    def get_room(self):
        return self.room

    def set_room(self, room_name):
        self.room = room_name
        if not room_name in self.visited_rooms:
            self.visited_rooms.add(room_name)
            return True
        else:
            return False

# Add the player "player_name" to the game, by creating a new player dictionary
# and filling it with default values (no score, no messages, etc)
def player_add(player_name):
    global g_players

    player = {"name": player_name, "room": None, "visited_rooms": set(), "items": set(), "score":0, "msgs": []}
    g_players[player_name] = player

# Get the list of messages for the player
def player_get_msgs(player_name):
    global g_players

    return g_players[player_name]["msgs"]

# Remove all of the player's current messages.
def player_remove_msgs(player_name):
    global g_players

    msgs = g_players[player_name]["msgs"]
    g_players[player_name]["msgs"] = []
    return msgs

# Add a message for the player.
def player_add_msg(player_name, msg):
    global g_players

    # msg might be coming in with leading spaces before
    # each line, which we want to remove. So use handy
    # regular expression (re) to remove those.
    msg = re.sub("(^|\n)[ ]+", " ", msg)

    # wrap (or re-wrap) msg so that each line (which ends
    # with a \n) will be at most 70 characters long. This
    # will also turn the msg string into a list of strings,
    # one per (wrapped to 70 chars) line.
    msg_lines = textwrap.wrap(msg, 70)

    # Get the player's current list of messages, and add
    # our new list of messages.
    msgs = player_get_msgs(player_name)
    msgs += msg_lines

    # Add a blank line between each group of lines that
    # get added.
    msgs += [""]

    # Limit the player's messages to at most 20 lines.
    msgs = msgs[-20:]

    # Update the player's messages with the result of above.
    g_players[player_name]["msgs"] = msgs

# Get the name of the room where the player is currently located
def player_get_room(player_name):
    global g_players

    return g_players[player_name]["room"]

# Move the player to the room <room_name>
def player_set_room(player_name, room_name):
    global g_players

    g_players[player_name]["room"] = room_name
    if not room_name in player_get_visited_rooms(player_name):
        g_players[player_name]["visited_rooms"].add(room_name)
        return True
    else:
        return False

# Get the set of room names that the player has visited
def player_get_visited_rooms(player_name):
    global g_players

    return g_players[player_name]["visited_rooms"]

# Get the player's current score
def player_get_score(player_name):
    global g_players

    return g_players[player_name]["score"]

# Set the player's current score
def player_set_score(player_name, score):
    global g_players

    g_players[player_name]["score"] = score

# Get the player's set of item names that they've taken
def player_get_items(player_name):
    return g_players[player_name]["items"]

# Add an item to the player's set of item names.
def player_add_item(player_name, item_name):
    player_get_items(player_name).add(item_name)

# Remove an item named <item_name> from the player's set of
# items.
def player_remove_item(player_name, item_name):
    player_get_items(player_name).remove(item_name)

def player_has_item(player_name, item_name):
    return item_name in player_get_items(player_name)

# Print the room's description by adding ot the player's
# list of messages.
def print_room_description(player_name, room_name):
    global g_rooms

    # Retrieve the current room by name
    room = g_rooms[room_name]

    # Print the room's description
    player_add_msg(player_name, room['description'])

    # If we're entering the stall w/o the deoderant, we are going to be printing out a special message and
    # then immediately exiting the room without printing a list of items.
    # TODO use more general approach to this
    if room_name == "Stall" and not player_has_item(player_name, "deoderant"):
        return

    # Get the room's item list
    item_names = room['items']

    # Print a comma-separated list of the room's items, if any.
    items_text = format_item_names(item_names, "see")
    if (items_text):
        player_add_msg(player_name, items_text)

def check_move_command(player_name, room_name, command):
    global g_rooms

    shortcuts = {"n": "north", "s": "south", "e": "east", "w": "west"}
    if command in shortcuts:
        command = shortcuts[command]

    # Get the current room by name
    room = g_rooms[room_name]

    # See if command is the name of a door in this room.
    doors = room['doors']

    # If so, move there and return True, otherwise return False.
    if doors.has_key(command):
        move_to_room(player_name, doors[command])
        return True
    elif command in {"north", "south", "east", "west", "up", "down"}:
        player_add_msg(player_name, "You can't go %s from here" % command)
        return True
    else:
        return False

# Handle special cases for entering a room.
# TODO add enter_special_room and exit_special_room
def enter_special_room(player_name, room_name):
    if room_name == "Stall" and not player_has_item(player_name, "deoderant"):
        player_add_msg(player_name, "You wake up to find yourself back in the Boys Bathroom")
        player_set_room(player_name, "Boys Bathroom")

    return


def move_to_room(player_name, room_name):

    visited_room_before = room_name in player_get_visited_rooms(player_name)

    # Update the player's current room
    player_set_room(player_name, room_name)

    # If they've already visited the room,
    # print a short message and return.
    if visited_room_before:
        # Handle "You are in in Mr. xxx's rooom", where there is no "the " before the
        # room name.
        preposition = "the "
        if "preposition" in g_rooms[room_name]:
            preposition = g_rooms[room_name]["preposition"]

        player_add_msg(player_name, "You are in %s%s" % (preposition, room_name))
        enter_special_room(player_name, room_name)
        return

    # TODO add special logic here to handle visiting Dave's Room for the
    # first time. You'd need to set a new attribute for the user, to keep
    # track of how many times they'd been in his room, and change the description
    # that gets printed out when they "look".
    #
    # Since this is the first time in this room, print the full room
    # description and add the room's score to the player's score, and
    # print a msg about how many points they've earned.

    # Print the room description
    print_room_description(player_name, room_name)

    # Get the new room by name
    room = g_rooms[room_name]

    # The player has earned the new room's value
    room_value = room['value']

    # Congratulate the player on his/her progress
    if (room_value > 0):
        player_set_score(player_name, player_get_score(player_name) + room_value)
        player_add_msg(player_name, "You just earned %s points!" % room_value)

    enter_special_room(player_name, room_name)


def check_take_command(player_name, command):
    global g_rooms

    # First use the handy-dandy get_item_name utility function
    # to extract the item name from the command.
    item_name = get_item_name("take", command)

    if (item_name == None):
        # If it isn't "take" or "take xxx" then return false, it's not
        # the take command
        return False
    elif item_name == "":
        player_add_msg(player_name, "You didn't specify what to take")
        return True

    # Get the current room by name
    room_name = player_get_room(player_name)
    room = g_rooms[room_name]

    # Get the room's item list
    room_item_names = room['items']

    # If xxx isn't the name of an item in the room, then
    # add a different error message.
    if (room_item_names.count(item_name) == 0):
        player_add_msg(player_name, "There is no %s in this room" % item_name)
        return True

    # if xxx isn't takeable, add an error message.
    if not g_items[item_name]["takeable"]:
        player_add_msg(player_name, "You can't take the %s" % item_name)
        return True

    # Otherwise, move the item from the room's list of items,
    # add the item to the player's inventory,
    # and print a confirmation string
    room_item_names.remove(item_name)
    player_add_item(player_name, item_name)
    player_add_msg(player_name, "You now have the %s" % item_name)
    return True

def examine_item_command(player_name, room_name, command):
    global g_items

    # First use the handy-dandy get_item_name utility function
    # to extract the item name from the command.
    item_name = get_item_name("examine", command)

    # If it's just "examine" then return an appropriate
    # error message.
    if (item_name == None):
        player_add_msg(player_name, '''Lexi & Emilie say - "You didn't say what to examine"''')
        return

    # Use the handy-dandy player_has_item utility function to check if
    # the player has the item in his/her possession, and print an
    # error message if not.
    if not player_has_item(player_name, item_name):
        # But wait - you can examine an item not in your possession if it's in the
        # room with you and it's not takeable.
        if item_name in g_rooms[room_name]["items"] and not g_items[item_name]["takeable"]:
            # OK, drop through to following code.
            None
        else:
            player_add_msg(player_name, '''Lexi & Emilie say - "No way, Jose. You do not have the %s"''' % item_name)
            return

    item = g_items[item_name]
    if item_name == "notebook" and g_items["notebook"]["open"]:
        description = item["open description"]
    else:
        description = item["description"]

    player_add_msg(player_name, '''Lexi & Emilie say - "%s"''' % description)

def drop_item_command(player_name, room_name, command):
    global g_rooms

    # First use the handy-dandy get_item_name utility function
    # to extract the item name from the command.
    item_name = get_item_name("drop", command)

    # If it's just "drop" then return an appropriate
    # error message.
    if (not item_name):
        player_add_msg(player_name, '''Sol says - "You didn't say what to drop"''')
        return

    # Get the current room by name
    room = g_rooms[room_name]

    # Get the room's item list
    room_item_names = room['items']

    # Use the handy-dandy player_has_item utility function to check if
    # the player has the item in his/her possession, and print an
    # error message if not.
    if not item_name in player_get_items(player_name):
        player_add_msg(player_name, '''Sol says - "Listen buddy, you don't have the %s"''' % item_name)
        return

    # Otherwise, remove the item from the player's inventory,
    # and add it to the room's list of items, and print a
    # confirmation string.
    player_remove_item(player_name, item_name)
    room_item_names.append(item_name)
    player_add_msg(player_name, '''Sol says - "You no longer have the %s"''' % item_name)


# End of solution code

def print_intro(player_name):
    player_add_msg(player_name, '''Yinneboma says - "Welcome to The Bitney Adventure Game, %s. This is the campus,
    you will be exploring the grounds, finding items, and navigating in all directions
    like North, South, East, West, Up and Down. Play the Bitney Adventure Game alone or
    play with your friends. There are 44 rooms filled with adventure
    and finding Items and Keys to Unlock locked doors. Play The Adventure that is Bitney."''' % player_name)

def print_help(player_name):
    player_add_msg(player_name, '''Aschia says - "Play the game by typing commands to move north, south, east or west and
    up or down in certain situations. Also you may type commands to
    interact with objects in the rooms. For example: take, drop, examine, eat, etc.
    And there are commands to list, look, plus bye to end the game"''')

def print_goodbye(player_name):
    player_add_msg(player_name, '''Ben says - "Thank you for exploring the wonderful Bitney campus, %s.
    We hope you enjoyed your adventure and learned a little bit more about the interesting
    things that go on here. You have %d Bitney points"''' % (player_name, player_get_score(player_name)))

def format_item_names(item_names, verb):
    if (len(item_names) > 0):
        items_text = "You %s the following item%s: " % (verb, ("" if len(item_names) == 1 else "s"))
        for item_name in item_names:
            items_text += (item_name + ", ")
        items_text = items_text[:-2] # remove that last comma & space
        return items_text
    else:
        return None

# Print the name of every item that the player has taken.

def print_items(player_name):

    # Use player_get_items to get the set of items the player has.
    item_names = player_get_items(player_name)
    items_text = format_item_names(item_names, "have")
    if items_text == None:
        items_text = "You've got nothing"

    player_add_msg(player_name, items_text)

def check_general_command(player_name, room_name, command):

    # TODO see if the command is one that we want to respond to, without
    # doing anything. E.g. if they're swearing at us, tell them to keep
    # it clean. If we don't have any match, return False.
    swearing = {"fuck", "shit", "cunt", "bastard"}
    for word in command.split():
        if word.lower() in swearing:
            player_add_msg(player_name, '''Makenna says - "Keep it clean, %s"''' % player_name)
            return True

    if command.startswith("hit"):
        print '''Makenna says - "There's no violence allowed at Bitney!"'''
        return True

    return False

    if command.startswith("hit "):
        player_add_msg(player_name, "There's no violence allowed at Bitney!")
        return True
    else:
        return False

def check_item_command(player_name, room_name, command):

    # TODO see if the command is for any of the items in the player's
    # list of items. If so, print out an appropriate message, and do
    # the action, and return True so that we know the command has been
    # handled.

    if command == "eat donut":
        if not "donut" in player_get_items(player_name):
            player_add_msg(player_name, "You don't have a donut to eat")
        else:
            # TODO you need to remove the donut from the player's list of
            # items, because they've eaten it.
            player_add_msg(player_name, "Yum, that was tasty!")
            player_remove_item(player_name, "donut")

        # We handled the command, so return True
        return True
    elif command == "open notebook":
        if not "notebook" in player_get_items(player_name):
            player_add_msg(player_name, "You don't have a notebook to open")
        elif g_items["notebook"]["open"]:
            player_add_msg(player_name, "You already opened the notebook")
        else:
            player_add_msg(player_name, g_items["notebook"]["open description"])
            g_items["notebook"]["open"] = True

        return True
    elif command == "close notebook":
        if not "notebook" in player_get_items(player_name):
            player_add_msg(player_name, "You don't have a notebook to close")
        elif not g_items["notebook"]["open"]:
            player_add_msg(player_name, "The notebook is already closed")
        else:
            player_add_msg(player_name, "You closed the notebook")
            g_items["notebook"]["open"] = False

        return True

    else:
        # We didn't handle the command, so return False
        return False

def game_complete(player_name):
    if player_get_score(player_name) >= 300:
        player_add_msg(player_name, "Eli says - congratulations on beating the game!")
        return True
    else:
        return False

# This is a handy utility routine that you give an action (like "take")
# and a command (like "take key"), and it returns just the item (e.g. "key")
# It lower-cases the thing being taken, so that it's easier to compare to
# the item names (keys) in g_items dictionary
def get_item_name(action, command):
    if (command == action) or (command == action + " the"):
        # They didn't specify what to take
        return ""
    elif command.startswith(action + " the "):
        return command[len(action) + len(" the "):]
    elif command.startswith(action + " "):
        return command[len(action) + len(" "):]
    else:
        return None

# This is a debugging function that ensures all rooms are reachable, and all
# doors lead to a named room.
def check_room_graph():
    current_room = g_rooms.keys().pop(0)
    visited_rooms = set()
    check_room(visited_rooms, current_room)

    # Now verify that we visited every room.
    for room in g_rooms.keys():
        if not room in visited_rooms:
            print "We never visited %s" % room

def check_room(visited_rooms, room):
    if not room in visited_rooms:
        visited_rooms.add(room)
        if not room in g_rooms.keys():
            print "The room %s doesn't exist" % room
            return

        doors = g_rooms[room]["doors"]
        for door in doors.keys():
            next_room = doors[door]
            # print "%s from %s goes to %s" % (door, room, next_room)
            check_room(visited_rooms, next_room)

# This is a debugging function that ensures all items are located in some
# room, but only one room.
def check_items():
    global g_items
    global g_rooms

    missing_items = set(g_items.keys())
    found_items = set()

    for room in g_rooms.keys():
        if not "items" in g_rooms[room].keys():
            print "Room %s is missing its list of items" % room
            return

        room_items = g_rooms[room]["items"]
        for room_item in room_items:
            if room_item in found_items:
                print "%s is in two different rooms" % room_item
            elif not room_item in missing_items:
                print "%s isn't a known item" % room_item
            else:
                # print "We found %s in %s" % (room_item, room)
                found_items.add(room_item)
                missing_items.remove(room_item)

    for missing_item in missing_items:
        print "%s is not in any room" % missing_item

def print_and_clear_msgs(player_name):
    msgs = player_remove_msgs(player_name)
    for msg in msgs:
        print msg

# g_players is a dictionary, where the key is the player name, and the value is a "player"
# Each player is also a dictionary, where the key is one of several possible player attributes
#   name:           Player name
#   room:           Name of room the player is in
#   visited_rooms:  Set of room names the player has visited. It starts
#                   off with just the current room the player is in, and
#                   gets added to as a player visits new rooms.
#   items:          Set of items the player has taken. It starts off empty.
#                   When the player takes an item, it gets moved from the
#                   room's set of items to the player's set of items. The
#                   inverse happens when a player drops an item they have.
#   score:          The player's current score. They get points for visiting
#                   a room, but only the first time.
#   msgs:           List of messages generated for the player.

g_players = {}

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

g_rooms = {
    "Computer Lab": {
        "description": "The computer lab is filled with glowing screens and old chairs. Your back is to a white board. There is a door to the east.",
        "items": ["notebook"],
        "value": 5,
        "doors": {"east": "Hallway"}
    },

    "Hallway": {
        "description": "The hallway is filled with colorful murals, lockers line the western wall. The hallway extends north and south, and there are doors to the east and west.",
        "items": [],
        "value": 0,
        "doors": {"west": "Computer Lab", "east": "Mr. Wood's Room", "north": "North Hallway", "south": "South Hallway"}
    },

    "North Hallway": {
        "description": "The north hallway is decorated with colorful artwork. You see a door labeled 'Boys Bathroom' to your east. To the north appears to be a more open area, and to the south there is the hallway.",
        "items": [],
        "value": 0,
        "doors": {"south": "Hallway", "north": "Atrium", "east": "Boys Bathroom"}
    },

    "South Hallway": {
        "description": "The south hallway also holds more artwork and murals on the walls. There is the Girls Bathroom to the east, a door to the west, and an open area to the south. To the north is the hallway.",
        "items": [],
        "value": 0,
        "doors": {"north": "Hallway", "south": "South Area", "west": "Storage Room", "east": "Girls Bathroom"}
    },

    "Boys Bathroom": {
        "description": "The bathroom has a sink, a mirror, a urinal, and a stall. No surprises here. The stall appears to be occupied. The exit is to your west.",
        "items": ["meme"],
        "value": 0,
        "doors": {"west": "North Hallway", "east": "Stall"}
    },

    "Stall": {
        "description":
'''You walk in and notice the floor is flooded inside the stall yet outside it no water can be found. An incredible stench fills the air. A voice from the toilet speaks 'the price must be paid'.
Your eyes water, and you fall to the floor.''',
        "description_with_deoderant":
'''You walk in and notice the floor is flooded inside the stall yet outside it no water can be found. An incredible stench fills the air, but the lavendar scent from your potpourri fights back, and you manage to
remain conscious. You notice the toilet is overflowing with water.''',
        "items": [],
        "value": 5,
        "doors": {"west": "Boys Bathroom"}
    },

    "Girls Bathroom": {
        "description": '''A calming pink room with art in progress on the walls. It has 2 stalls, 2 sinks, 2 mirrors
        and a window. The exit is to your west.''',
        "items": [],
        "value": 2,
        "doors": {"west": "South Hallway"}
    },

    "Storage Room": {
        "description": "The storage room is strangely unlocked. Head east to return to the South Hallway.",
        "items": ["plunger"],
        "value": 0,
        "doors": {"east": "South Hallway"}
    },

     "Atrium": {
         "description": "A small room with a bench and some artwork. There is a door to the west, east, and north. The North Hallway is to the south...",
              "items": ["crumpled note"],
              "value": 5,
              "doors": {"north": "Bistro", "west": "Math Room", "east": "Atrium Deck", "south": "North Hallway"}},
         "South Area":
             {"description": "An area well lit by the windows. There is a table with some chairs. There is a hallway to your north, a door to your east, south, and west. There is another door on the south wall, but it is locked",
              "items": [],
              "value": 0,
              "doors": {"north": "South Hallway", "south": "Spanish Room", "west": "Mrs. Simpton's Room", "east": "Basketball Court"}},
         "Mr. Wood's Room":
             {"description":  "The messy room of a maddened artist. This room is barely lit and has many tables. The walls are covered in propaganda all in different languages. There are two white bords one has a map of america and the other has a map of Russia. There is a life sized statue of George Washington in the room. There is a door to the north, east, and west",
              "items": ["statue"],
              "value": 1,
              "preposition": "",
              "doors": {"north": "Art Closet", "west": "Hallway", "east": "Picnic Tables"}},
         "Art Closet":
             {"description": "A cluttered confusion of art supplies. The odor of paint fills your nose. the exit is to your south.",
              "items": [],
              "value": 0,
              "doors": {"south": "Mr. Wood's Room"}},
         "Math Room":
             {"description": "There are some tables and... math books? There is a door to the north and a door to the east.",
              "items": [],
              "value": 0,
              "doors": {"north": "Atrium Deck", "east": "Atrium"}},
         "Bistro":
             {"description": "The place to be at lunch time. The bistro is a small closet of a room with quotes on every inch of the wall. It contains an abundance of tasty lunch-time snacks. there is a door to the east and a door to the south.",
              "items": ["key", "donut"],
              "value": 10,
              "doors": {"south": "Atrium", "east": "Atrium Deck"}},
         "Spanish Room":
             {"description": "Mrs. Phillips is single-handedly teaching Spanish to all grades in a small, rectangular room. the exit is to the north.",
              "items": [],
              "value": 3,
              "doors": {"north": "South Area"}},
         "Atrium Deck":
             {"description": "You end up outside on a deck. To the east you see some teachers talking in their area. To the west is a door",
              "items": [],
              "value": 5,
              "doors": {"east": "Teacher Area", "west": "Atrium"}},

    "Picnic Tables": {
        "description": '''You are outside under a green tent, surrounded by green picnic tables whose tops are
        polka-dotted with paint and bare spots. There is the remnant of a freshman's lunch on a table. To the
        north are some teachers talking in their area. To the west is a door. To the south is a basketball court
        that has a few cars parked on it.''',
        "items": [],
        "value": 10,
        "doors": {"north": "Teacher Area", "south": "Basketball Court", "west": "Mr. Wood's Room", "east": "Fence Post"}
    },

    "Fence Post": {
        "description": '''You just whacked your head into a fence post. Head west or south to turn around a different
        direction''',
        "items": [],
        "value": 50,
        "doors": {"west": "Picnic Tables", "south": "Greenhouse"}
    },

         "Greenhouse":
             {"description": "you just whacked your head into the greenhouse.... that must have hurt.... head west to take a break at the Basketball Court tables",
              "items": [],
              "value": 40,
              "doors": {"north": "Fence Post", "west": "Basketball Court"}},
         "Teacher Area":
             {"description": "you listen in on the teachers as they are discussing a student with low grades. they shoo you off claiming the conversation is confidential. to the north there is the parking area, to the south there is the Picnic tables. to the west there is a deck of sorts",
              "items": [],
              "value": 5,
              "doors": {"north": "Parking Area", "south": "Picnic Tables", "west": "Atrium Deck"}},
         "Mrs. Simpton's Room":
             {"description": "A single windowed room with mysterious symbols on the walls. It smells strongly of body oder. The exit is to the east... better hurry! It smells!",
              "items": ["deoderant"],
              "value": 10,
              "preposition": "",
              "doors": {"east": "South Area"}},
         "Science Room":
             {"description": "A rather large room full of desks, chairs, and science tools. There are doors to the north, east, and south.",
              "items": ["pop tart"],
              "value": 10,
              "doors": {"north": "Science Bathroom", "east": "Secret Hallway", "south": "Parking Area"}},
         "Mr. Elkin's Car":
             {"description": "A brown scion is parked, and Mr. Elkin is there, happily chewing on a sandwich. You look around, and notice a deck to your south, another door off to your north, and the base of some stairs to your west. There is also the smiley guys parking lot to the east. elkin warns you not to go because you may get run over, but you may try anyways.",
              "items": [],
              "value": 30,
              "preposition": "",
              "doors": {"east": "Smiley Guys Parking Lot", "south": "Office Porch", "west": "Base of Stairs", "north": "Humanities Hall"}},
         "Smiley Guys Parking Lot":
             {"description": "*crunch* *slam* *honk*. you just got hit by a car and are dead. But, seeing as you are new here, we'll give you a second chance at life. enter 'respawn' if you wish to try again",
              "items": [],
              "value": 100,
              "doors": {"respawn": "Mr. Elkin's Car"}},
         "Secret Hallway":
             {"description": "A small unlit hallway with a door at either end, not very exciting. not sure why it's 'Secret'. there is a door to the west and east",
              "items": [],
              "value": 5,
              "doors": {"east": "Humanities Hall", "west": "Science Room"}},
         "Science Bathroom":
             {"description": "A small bathroom with random scribblings on the wall, a painting made by Mr. Wood hangs above the toilet. The exit is to the south.",
              "items": ["random number"],
              "value": 20,
              "doors": {"south": "Science Room"}},
         "Humanities Bathroom":
             {"description": "A cramped bathroom, the walls are painted a vibrant orange color. the exit is to the south.",
              "items": [],
              "value": 10,
              "doors": {"south": "Humanities Hall"}},
         "Humanities Hall":
             {"description": "Several long tables form a 'U' shape facing a podium. There is an odd door to the north. there are also doors to the east, south, and west.",
              "items": [],
              "value": 20,
              "doors": {"east": "Kill Room", "west": "Secret Hallway", "south": "Mr. Elkin's Car", "north": "Humanities Bathroom"}},
         "Kill Room":
             {"description": "Completely dark.... the clanking sounds of folded chairs can be hears. the exit is to the south.",
              "items": [],
              "value": 10,
              "doors": {"west": "Humanities Hall"}},
         "Parking Area":
             {"description": "There are a bunch of parked cars around you. To the north you see a door labeled 'science'. to the east, you see a set of stairs. To the south you see a group of teachers talking.",
              "items": [],
              "value": 30,
              "doors": {"north": "Science Room", "south": "Teacher Area", "east": "Base of Stairs"}},
         "Base of Stairs":
             {"description": "you find yourself at a base of stairs. you can either go south and go up, or you can west to the parking area, or east over the Mr. Elkin",
              "items": [],
              "value": 0,
              "doors": {"south": "Back Porch", "east": "Mr. Elkin's Car", "west": "Parking Area"}},
         "Back Porch":
             {"description": "you find yourself on a porch to the back of the office building. you can either go north down the stairs in the direction of the parking area, or you can go east to a door that leads inside.",
              "items": [],
              "value": 10,
              "doors": {"north": "Base of Stairs", "east": "Upstairs Area"}},
         "Upstairs Area":
             {"description": "There is a long table with many chairs around it. There are four doors, but two are labeled off limits. there is a door open to the north and south. there is also a door to the west. you also notice two sets of stairs heading down to a landing... you can go that way by commanding 'down'",
              "items": [],
              "value": 20,
              "doors": {"north": "Russ' Office", "south": "Kitchen", "west": "Back Porch", "down": "Stair Landing"}},
         "Parking Lot":
             {"description": "*BRAAAAP*, you just got slammed by Dave on his bike. 'respawn' if you want to try and live again",
              "items": [],
              "value": 90,
              "doors": {"respawn": "Office Porch"}},
         "Office Porch":
             {"description": "This is where the cool kids chill out. to the north you see Mr. elkin chewing on a sandwich. to the west there is a great wooden double door. to the east is the parking lot, which looks dangerous, but you may try to escape there for some food...",
              "items": [],
              "value": 40,
              "doors": {"north": "Mr. Elkin's Car", "east": "Parking Lot", "west": "Lobby"}},
         "Basketball Court":
             {"description": "There is a basketball hoop with cars parked around it. not very good for playing basketball. there are picnic tables to the north, a door off the west, and a greenhouse to the east....",
              "items": ["basketball"],
              "value": 10,
              "doors": {"north": "Picnic Tables", "west": "South Area", "east": "Greenhouse"}},
         "Lobby":
             {"description": "The lobby is a place where people go to chill. There are stairs to the west, there is a door to the south and east, and an approachable desk to the north",
              "items": [],
              "value": 2,
              "doors": {"west": "Stair Landing", "north": "Angelina's Desk Area", "south": "Mr. Young's Room", "east": "Office Porch"}},
         "Angelina's Desk Area":
             {"description": "part of the office lobby where Angelina resides. There is a door to the north and west. A lobby is to your south",
              "items": [],
              "value": 10,
              "preposition": "",
              "doors": {"west": "Teacher's Lounge", "north": "Dave's Office", "south": "Lobby"}},
         "Stair Landing":
             {"description": "there are two stairs leading up to an upper area. go east to return to the lobby, command 'up' if you wish to go up",
              "items": [],
              "value": 0,
              "doors": {"up": "Upstairs Area", "east": "Lobby"}},
         "Mr. Young's Room":
             {"description": "Where the Pop Tart king resides. This room is full of light from the windows. there is a cart, a desk, and a projector. To the north and west there are doors",
              "items": [],
              "value": 20,
              "preposition": "",
              "doors": {"north": "Lobby", "west": "Office Bathroom"}},
         "Dave's Office":
             {"description": "A small office with a round table, and a desk with a Mac on it. the exit is to the south",
              "items": [],
              "value": 20,
              "preposition": "",
              "doors": {"south": "Angelina's Desk Area"}},
         "Teacher's Lounge":
             {"description": "There is a table with chairs surrounding it, and a printer in the corner. There are several bookshelves. There is also a closet that has a sign saying 'KEEP OUT'. the exit is to the east.",
              "items": [],
              "value": 5,
              "doors": {"east": "Angelina's Desk Area"}},
         "Russ' Office":
             {"description": "The room where Russ resides and handles the daily responsiblies of a principal which is upstairs of the office. the exit is to the south",
              "items": [],
              "value": 30,
              "preposition": "",
              "doors": {"south": "Upstairs Area"}},
         "Kitchen":
             {"description": "This room contains a refridgerator, stove, sink, and countertops. A couple windows. the exit is to the north.",
              "items": [],
              "value": 20,
              "doors": {"north": "Upstairs Area"}},
         "Office Bathroom":
             {"description": "A bathroom that smells weird. there is a small window that is slightly ajar... not big enough to fit through. the exit is to the east.",
              "items": [],
              "value": 0,
              "doors": {"east": "Mr. Young's Room"}},
}

# items is a dictionary, where the key is the item name, and the value is an "item"
# Each item is also a dictionary, where the key is one of several possible values
#   description -> string that describes the item
#   takeable -> boolean for whether the item can be taken or not.
#
# You can also have other item-specific attributed, e.g. a bottle of water could have
# an "empty": False attribute, and this changes to True after you've had a drink.
# Use your imagination.

g_items = {
    "notebook": {
        "open": False,
        "description":
'''It's a typical lab notebook with a red cover''',
        # Description after the notebook has been opened
        "open description":
'''The notebook containing all kinds of complex diagrams, equations, assignments
(many with very low grades), etc. in a completely random order. None of the
pages have any students names on them, but Mr. Schneider has obviously written
in the name "Peggy???" in red ink on several of the graded assignments.''',
        "takeable": True
    },

    "plunger": {
        "description": "You are holding a typical toilet plunger with a 3ft long wooden handle.",
        "takeable": True
    },

    "key": {
        "description": "It's a small, nondescript key",
        "takeable": True
    },

    "crumpled note": {
        "description":
'''You are holding a sheet of paper that was crumpled up into a ball before it was seemingly discarded. It reads,
"I can't find my stupid physics binder anywhere! Mr. Schneider is going to kill me when I get to class."''',
        "takeable": True
    },

    "donut": {
        "description": "a chocolate donut with multicolored sprinkles",
        "takeable": True
    },

    "meme": {
        "description":
'''an element of a culture or system of behavior that may be considered to be passed from one individual
to another by nongenetic means, especially imitation.''',
        "takeable": True
    },

    "basketball": {
        "description":
'''It's a basketball, 'nuff said''',
        "takeable": True
    },

    "statue": {
        "description":
'''A life-sized bronze statue of George Washington.''',
        "takeable": False
    },

    "random number": {
        "description":
'''An unknown phone number written on the wall''',
        "takeable": False
    },

    "deoderant": {
        "description": "A basket of potpourri with a lovely lavdendar scent",
        "takeable": True
    },

    "pop tart": {
        "description": "this pop tart has a smiling alien face on time",
        "takeable": False
    },
}


# ============================================================
# Start of the main game
# ============================================================

def player_start(player_name, room_name="Hallway"):
    player_add(player_name)

    # Print out the welcome message
    player_add_msg(player_name, "")
    print_intro(player_name)

    # Start the player in room_name.
    player_set_room(player_name, room_name)

    # Print out where the user is starting.
    print_room_description(player_name, player_get_room(player_name))

def player_command(player_name, command):
    # FUTURE a better/cleaner approach would be to take the command that the
    # user entered and split it into the first word and the rest of the command.
    # Then use a dictionary to map from the first word (e.g. "take") to a function
    # that knows how to handle that command. So we'd have functions for handling
    # commands like "bye", "help", "list", etc.

    # Lower-case, so that "Bye" is the same as "bye", and remove trailing
    # and leading spaces to simplify parsing.
    command = command.lower().strip()

    # See if the command is one of our special commands.
    if command == "bye":
        # Print a goodbye message, and tell the caller we're all done.
        print_goodbye(player_name)
        return False

    if command == "help":
        print_help(player_name)

    elif command == "list":
        print_items(player_name)

    elif command == "look":
        print_room_description(player_name, player_get_room(player_name))

    elif command == "check":
        check_room_graph()
        check_items()

    elif check_take_command(player_name, command):
        None

    elif command.startswith("drop"):
        drop_item_command(player_name, player_get_room(player_name), command)

    elif command.startswith("examine"):
        examine_item_command(player_name, player_get_room(player_name), command)

    # See if the command is the name of a door
    elif check_move_command(player_name, player_get_room(player_name), command):
        # OK, it was a move command... we need to put something here so Python
        # is happy (can't have an empty elif block)
        None

    # See if the command is an action on an item the player
    # has, in the appropriate room.  If so, take that action
    # on that item.
    elif check_item_command(player_name, player_get_room(player_name), command):
        # OK, it was an action on an item... we need to put something here so Python
        # is happy (can't have an empty elif block)
        None

    # See if the command is something we want to respond to
    # with special text.
    elif check_general_command(player_name, player_get_room(player_name), command):
        # We responded... we need to put something here so Python
        # is happy (can't have an empty elif block)
        None

    # No idea what they want to do
    else:
        player_add_msg(player_name, "I don't understand that")

    return True

