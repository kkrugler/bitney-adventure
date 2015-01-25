import textwrap

def print_intro():
    # Level - 1

    # TODO print an introduction to the game, with some helpful hints

    pprint("intro")

def print_help():
    # Level - 2

    # TODO print help text

    pprint("help")

def print_goodbye():
    # Level - 2

    global g_score

    # TODO print goodbye text, along with the player's current score

    pprint("goodbye: ", g_score)

def print_room_description(room_name):
    # Level - 5

    global g_rooms

    # TODO print the room's description and list the items it currently
    # contains, which means a loop that iterates over its item list,
    # (which you retrieve from the "items" entry in the g_rooms
    # dictionary), and then prints out the list. If the list contains
    # no items, skip that part.

    pprint("room description")

def print_items():
    # Level - 5

    global g_player_items

    # TODO print a list of the item names that the player has, which
    # means a loop that iterates over the g_game_items list, and prints
    # out the list. If the player has nothing, print "You've got nothing"

    pprint("You've got nothing")

def check_move_command(room_name, command):
    # Level - 4

    global g_rooms

    # TODO see if this is the name of a door in this room.
    # If so, call move_to_room() and return True.  Otherwise return False.

    return False

def check_general_command(room_name, command):
    # Level - 2

    # TODO see if the command is one that we want to respond to, without
    # doing anything. E.g. if they're swearing at us, tell them to keep
    # it clean. If we don't have any match, return False.

    if command.startswith("hit "):
        pprint("There's no violence allowed at Bitney!")
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
    g_current_room_name = room_name

def take_item_command(room_name, command):
    # Level - 5

    global g_player_items
    global g_rooms

    # First use the handy-dandy get_item_name utility function to extract
    # the item name from the command.
    item_name = get_item_name("take", command)

    # TODO command will be "take xxx", where xxx is the name of an
    # item in the room. If xxx isn't the name of an item in the room, then
    # print an error message. Otherwise move the item from
    # the room's list of items, and put it into the player's list of items (g_player_items),
    # and print a string that says "you now have the xxx". Though
    # you only want to do this if the item is takeable!

    pprint("I don't know how to take " + item_name)

def examine_item_command(room_name, command):
    # Level - 3

    global g_player_items
    global g_game_items

    # First use the handy-dandy get_item_name utility function to extract
    # the item name from the command.
    item_name = get_item_name("examine", command)

    # TODO if item_name isn't in the player's
    # list of items, print an error message. Otherwise print
    # the item's description. You can use the player_has_item(item_name)
    # utility function to help with this.

    pprint("I don't know how to examine %s" % item_name)

def drop_item_command(room_name, command):
    # Level - 5

    global g_player_items
    global g_rooms

    # First use the handy-dandy get_item_name utility function to extract
    # the item name from the command.
    item_name = get_item_name("drop", command)

    # TODO command should be "drop xxx", where xxx is the name of an
    # item in the player's list of items. If xxx isn't the name of an item
    # in the player's list of items (call the handy-dandy player_has_item
    # utility to find out), then print a an error message.
    # Otherwise move the item from the player's list of items to the room's
    # list of items, and print a string that says "you no longer have
    # the xxx"

    pprint("I don't know how to drop %s" % item_name)

def check_item_command(room_name, command):
    # Level - 5

    # TODO see if the command is for any of the items in the player's
    # list of items. If so, print out an appropriate message, and do
    # the action, and return True so that we know the command has been
    # handled.

    if command == "eat donut":
        if not player_has_item("donut"):
            pprint("You don't have anything to eat")
        else:
            # TODO you need to remove the donut from the player's list of
            # items, because they've eaten it.
            pprint("Yum, that was tasty!")

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

# This is a handy utility routine that wraps the text to be at most 80
# characters wide.
def pprint(text):
    print textwrap.fill(text, 80)

# This is a debugging function that ensures all rooms are reachable, and all
# doors lead to a named room.
def check_room_graph(room_name):
    global g_rooms

    current_room = room_name
    visited_rooms = set()
    check_room(visited_rooms, current_room)

    # Now verify that we visited every room.
    for room in g_rooms.keys():
        if not room in visited_rooms:
            pprint("We never visited %s" % room)

def check_room(visited_rooms, room):
    if not room in visited_rooms:
        visited_rooms.add(room)
        if not room in g_rooms:
            pprint("%s is not a room name in the g_rooms dictionary" % room)
            return

        doors = g_rooms[room]["doors"]
        for door in doors.keys():
            next_room = doors[door]
            # print "%s from %s goes to %s" % (door, room, next_room)
            check_room(visited_rooms, next_room)

# This is a debugging function that ensures all items are located in some
# room, but only one room.
def check_items():
    global g_game_items
    global g_rooms

    # We start off with a list of all items, and remove ones that we find, so what's
    # left will be the actual missing items
    missing_items = set(g_game_items.keys())

    # We start off with no found items, and we add to this as we find items, so we
    # can check for the same item being in two different rooms.
    found_items = set()

    for room in g_rooms.keys():
        if not hasattr(g_rooms[room], "items"):
            pprint("Room '%s' doesn't have an 'items' key in its dictionary" % room)
            continue

        room_items = g_rooms[room]["items"]
        for room_item in room_items:
            if room_item in found_items:
                pprint("%s is in two different rooms" % room_item)
            elif not room_item in missing_items:
                pprint("Item %s in room %s isn't a valid item name" % (room_item, room))
            else:
                # print "We found %s in %s" % (room_item, room)
                found_items.add(room_item)
                missing_items.remove(room_item)

    for missing_item in missing_items:
        pprint("%s is not in any room" % missing_item)

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

g_rooms = {"Computer Lab":
             {"description": "The computer lab is filled with glowing screens and old chairs, your back is to a white board. There is a door to the east",
              "items": ["Notebook"],
              "value": 5,
              "doors": {"east": "Hallway"}},
         "Hallway":
             {"description": "The hallway is filled with colorful murals, lockers line the western wall. There are hallways to the north and east, and a door to the east and west",
              "items": ["Key"],
              "value": 0,
              "doors": {"west": "Computer Lab", "east": "Mr. Wood's Room", "north": "North Hallway", "south": "South Hallway"}},
         "North Hallway":
             {"description": "the North Hallway contains artwork, there is a door labeled 'Boys Bathroom' to your east. to your north appears to be a more open area. To the south there is the Hallway..",
              "items": [],
              "value": 0,
              "doors": {"south": "Hallway", "north": "Atrium", "east": "Boys Bathroom"}},
         "South Hallway":
             {"description": "the south hallway also holds more artwork and murals on the walls. There is the Girls Bathroom to the east, a door to the west, and an open area to the south. to the north is the hallway.",
              "items": [],
              "value": 0,
              "doors": {"north": "Hallway", "south": "South Area", "west": "Storage Room", "east": "Girls Bathroom"}},
         "Boys Bathroom":
             {"description": "The bathroom has a sink, a mirror, a urinal, and a stall. No surprises here. the stall is occupied. The exit is to your west.",
              "items": [],
              "value": 0,
              "doors": {"west": "North Hallway"}},
         "Girls Bathroom":
             {"description": "A calming pink room with art in progress on the walls. It has 2 stalls, 2 sinks, 2 mirrors and a window. The exit is to your west.",
              "items": ["Physics Binder"],
              "value": 2,
              "doors": {"west": "South Hallway"}},
         "Storage Room":
             {"description": "The storage room is locked. Head east to return to the South Hallway.",
              "items": ["Hitler Doll"],
              "value": 0,
              "doors": {"east": "South Hallway"}},
         "Atrium":
             {"description": "A small room with a bench and some artwork. There is a door to the west, east, and north. The North Hallway is to the south...",
              "items": ["Crumpled Note"],
              "value": 5,
              "doors": {"north": "Bistro", "west": "Math Room", "east": "Atrium Deck", "south": "North Hallway"}},
         "South Area":
             {"description": "An area well lit by the windows. There is a table with some chairs. There is a hallway to your north, a door to your east, south, and west. There is another door on the south wall, but it is locked",
              "items": [],
              "value": 0,
              "doors": {"north": "South Hallway", "south": "Spanish Room", "west": "Mrs. Simpton's Room", "east": "Basketball Court"}},
         "Mr. Wood's Room":
             {"description":  "The messy room of a maddened artist. This room is barely lit and has many tables. The walls are covered in propaganda all in different languages. There are two white bords one has a map of america and the other has a map of Russia. There is a life sized statue of George Washington in the room. There is a door to the north, east, and west",
              "items": ["Statue"],
              "value": 1,
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
              "items": ["Donut"],
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
         "Picnic Tables":
             {"description": "You are outside under a green tent, surrounded by green picknic tables whose tops are pocadotted with paint and peeled away paint. There is the remnence of a freshmans lunch on a table. to the north are some teachers talking in their area. to the west is a door. to the south is a basketball court that has a few cars parked on it.",
              "items": [],
              "value": 10,
              "doors": {"north": "Teacher Area", "south": "Basketball Court", "west": "Mr. Wood's Room", "east": "Fence Post"}},
         "Fence Post":
             {"description": "You just whacked your head into a fence post. Head west or south to turn around a different direction",
              "items": [],
              "value": 50,
              "doors": {"west": "Picnic Tables", "south": "Greenhouse"}},
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
             {"description": "A single windowed room with mysterious symbols on the walls. It smells strongly of body oder. the exit is to the east... better hurry! it smells!",
              "items": [],
              "value": 10,
              "doors": {"east": "South Area"}},
         "Science Room":
             {"description": "A rather large room full of desks, chairs, and science tools. There are doors to the north, east, and south.",
              "items": [],
              "value": 10,
              "doors": {"north": "Science Bathroom", "east": "Secret Hallway", "south": "Parking Area"}},
         "Elkin's Car":
             {"description": "A brown scion is parked, and Mr. Elkin is there, happily chewing on a sandwich. You look around, and notice a deck to your south, another door off to your north, and the base of some stairs to your west. There is also the smiley guys parking lot to the east. elkin warns you not to go because you may get run over, but you may try anyways.",
              "items": [],
              "value": 30,
              "doors": {"east": "Smiley Guys Parking Lot", "south": "Office Porch", "west": "Base of Stairs", "north": "Humanities Hall"}},
         "Smiley Guys Parking Lot":
             {"description": "*crunch* *slam* *honk*. you just got hit by a car and are dead. But, seeing as you are new here, we'll give you a second chance at life. enter 'respawn' if you wish to try again",
              "items": [],
              "value": 100,
              "doors": {"respawn": "Elkin's Car"}},
         "Secret Hallway":
             {"description": "A small unlit hallway with a door at either end, not very exciting. not sure why it's 'Secret'. there is a door to the west and east",
              "items": [],
              "value": 5,
              "doors": {"east": "Humanities Hall", "west": "Science Room"}},
         "Science Bathroom":
             {"description": "A small bathroom with random scribblings on the wall, a painting made by Mr. Wood hangs above the toilet. the exit is to your east.",
              "items": ["Random Number"],
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
              "doors": {"east": "Kill Room", "west": "Secret Hallway", "south": "Elkin's Car", "north": "Humanities Bathroom"}},
         "Kill Room":
             {"description": "Completely dark.... the clanking sounds of folded chairs can be hears. the exit is to the south.",
              "items": [],
              "value": 10,
              "doors": {"south": "Humanities Hall"}},
         "Parking Area":
             {"description": "There are a bunch of parked cars around you. To the north you see a door labeled 'science'. to the east, you see a set of stairs. To the south you see a group of teachers talking.",
              "items": [],
              "value": 30,
              "doors": {"north": "Science Room", "south": "Teacher Area", "east": "Base of Stairs"}},
         "Base of Stairs":
             {"description": "you find yourself at a base of stairs. you can either go south and go up, or you can west to the parking area, or east over the Mr. Elkin",
              "items": [],
              "value": 0,
              "doors": {"south": "Back Porch", "east": "Elkin's Car", "west": "Parking Area"}},
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
              "doors": {"north": "Elkin's Car", "east": "Parking Lot", "west": "Lobby"}},
         "Basketball Court":
             {"description": "There is a basketball hoop with cars parked around it. not very good for playing basketball. there are picnic tables to the north, a door off the west, and a greenhouse to the east....",
              "items": ["Basketball"],
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
              "doors": {"west": "Teacher's Lounge", "north": "Dave's Office", "south": "Lobby"}},
         "Stair Landing":
             {"description": "there are two stairs leading up to an upper area. go east to return to the lobby, command 'up' if you wish to go up",
              "items": [],
              "value": 0,
              "doors": {"up": "Upstairs Area", "east": "Lobby"}},
         "Mr. Young's Room":
             {"description": "Where the Pop Tart king resides. This room is full of light from the windows. there is a cart, a desk, and a projector. To the north and west there are doors",
              "items": ["Meme"],
              "value": 20,
              "doors": {"north": "Lobby", "west": "Office Bathroom"}},
         "Dave's Office":
             {"description": "A small office with a round table, and a desk with a Mac on it. the exit is to the south",
              "items": [],
              "value": 20,
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

g_game_items = {
            "Notebook":
             {"description":
'''notebook containing all kinds of complex diagrams, equations, assignments
(many with very low grades), etc. in a completely random order. None of the
pages have any students names on them, but Mr. Schneider has obviously written
in the name "Peggy???" in red ink on several of the graded assignments.''',
              "takeable": True},
         "Key":
             {"description":
'''small, nondescript key''',
              "takeable": True},
         "Crumpled Note":
             {"description":
'''loose-leaf sheet of paper that was crumpled up into a ball before it was seemingly discarded. It reads,
"I can't find my stupid physics binder anywhere! Mr. Schneider is going to kill me when I get to class."''',
              "takeable": True},
         "Physics Binder":
             {"description":
'''notebook containing all kinds of complex diagrams, equations, assignments (many with very low grades),
 etc. in a completely random order. None of the pages have any students names on them, but Mr. Schneider
 has obviously written in the name "Peggy???" in red ink on several of the graded assignments.''',
              "takeable": True},
         "Donut":
             {"description":
'''a chocolate donut with multicolored sprinkles''',
              "takeable": True},
         "Meme":
             {"description":
'''an element of a culture or system of behavior that may be considered to be passed from one individual
to another by nongenetic means, especially imitation.''',
             "takeable": True},
         "Basketball":
             {"description":
'''It's a basketball, 'nuff said''',
              "takeable": True},
         "Statue":
             {"description":
'''A lifesized bronze statue of George Washington.''',
              "takeable": False},
         "Hitler Doll":
             {"description":
'''It's a doll of Germany's favorite dictator''',
              "takeable": True},
         "Random Number":
             {"description":
'''An unknown phone number written on the wall''',
              "takeable": False},
}

# ============================================================
# Start of the main game
# ============================================================

# Print out the welcome message
print_intro()

# Start the player in the hallway. Which is why this room isn't worth
# any points, as you get there automatically.
move_to_room("Hallway")

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

    if command == "check":
        check_room_graph(g_current_room_name)
        check_items()
        continue

    if command.startswith("take"):
        take_item_command(g_current_room_name, command)
        continue

    if command.startswith("drop"):
        drop_item_command(g_current_room_name, command)
        continue

    if command.startswith("examine"):
        examine_item_command(g_current_room_name, command)
        continue

    # See if the command is the name of a door
    if check_move_command(g_current_room_name, command):
        continue

    # See if the command is an action on an item the user
    # has, in the appropriate room.  If so, take that action
    # on that item.
    if check_item_command(g_current_room_name, command):
        continue

    # See if the command is something we want to respond to
    # with special text.
    if check_general_command(g_current_room_name, command):
        continue

    # No idea what they want to do
    print("I don't understand that")

