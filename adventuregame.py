import textwrap

class Player:
    def __init__(self, game):

        # This is the global Game that all players are using
        self.game = game

        # This is a set of items that player has taken. It starts off
        # as empty. When you take an item, it gets added to this set, and when
        # you drop an item, it gets removed from this set.
        self.items = set()

        # This is the name of the current room that the player is in.
        self.current_room_name = None

        # This is a set of all of names of all the rooms that the player has visited.
        self.visited_room_names = set()

        # This is the player's current score. They get points for visiting a room
        # (but only the first time!)
        self.score = 0

        # This is the list of messages (split by line) for the player.
        self.msgs = []

    def pprint(self, msg):
        # add msg to current list of messages, and
        # prune that list if it's longer than our max
        self.msgs += textwrap.wrap(msg, 80)
        self.msgs = self.msgs[-50:]

    def get_messages(self):
        return self.msgs

    def check_move_command(self, command):
        door_name = command

        next_room_name = self.game.get_room_from_door(self.current_room_name, door_name)

        if next_room_name != None:
            self.move_to_room(next_room_name)
            return True
        else:
            return False

    def move_to_room(self, room_name):

        # Update the global current room name.
        self.current_room_name = room_name

        # If this is the first time in this room (check visited_rooms) then
        # add the room's score to the player's score, and print a msg
        # about how many points they've earned.
        if room_name in self.visited_room_names:
            self.pprint("You are in the %s" % room_name)
            return

        # Remember that the user has now been here
        self.visited_room_names.add(room_name)

        # Print the room description
        self.game.print_room_description(room_name)

        # The player has earned the new room's value
        room_value = self.game.get_room_score(room_name)

        # Congratulate the player on his/her progress
        if (room_value > 0):
            self.score += room_value
            self.pprint("You just earned %s points!" % room_value)

    def take_item_command(self, room_name, command):

        # First use the handy-dandy get_item_name utility function
        # to extract the item name from the command.
        item_name = self.get_item_name("take", command)

        # If it's just "take" then return an appropriate
        # error message.
        if (not item_name):
            self.pprint("You didn't specify what to take")
            return

        # Get the room's item list
        room_item_names = self.game.get_room_items(room_name)

        # If xxx isn't the name of an item in the room, then
        # return a different error message.
        if not item_name in room_item_names:
            self.pprint("There is no %s in this room" % item_name)
            return

        # Otherwise, move the item from the room's list of items,
        # add the item to the player's inventory,
        # and print a confirmation string
        # TODO catch case of someone else removing the same item
        # before we get to, which should then throw an exception
        self.game.remove_item_from_room(room_name, item_name)

        self.add_item(item_name)
        self.pprint("You now have the %s" % item_name)

    def examine_item_command(self, room_name, command):

        # First use the handy-dandy get_item_name utility function
        # to extract the item name from the command.
        item_name = self.get_item_name("examine", command)

        # If it's just "examine" then return an appropriate
        # error message.
        if (not item_name):
            self.pprint("You didn't specify what to examine")
            return

        # Use the handy-dandy player_has_item utility function to check if
        # the player has the item in his/her possession, and print an
        # error message if not.
        if (not self.has_item(item_name)):
            self.pprint("You don't have a " + item_name + " in your possession")
            return

        self.pprint(self.game.get_item_description(item_name))

    def drop_item_command(self, room_name, command):

        # First use the handy-dandy get_item_name utility function
        # to extract the item name from the command.
        item_name = self.get_item_name("drop", command)

        # If it's just "drop" then return an appropriate
        # error message.
        if (not item_name):
            self.pprint("You didn't specify what to drop")
            return

        # Use the handy-dandy player_has_item utility function to check if
        # the player has the item in his/her possession, and print an
        # error message if not.
        if (not self.has_item(item_name)):
            self.pprint("You don't have a " + item_name + " in your possession")
            return

        # Otherwise, remove the item from the player's inventory,
        # and add it to the room's list of items, and print a
        # confirmation string.
        self.game.add_item_to_room(room_name, item_name)
        self.remove_item(item_name)
        self.pprint("You no longer have the %s" % item_name)

    # Return True if the player has an item named item_name
    def has_item(self, item_name):
        return item_name in self.items

    # Remove item_name from the player's set of items
    def remove_item(self, item_name):
        self.items.remove(item_name)

    def add_item(self, item_name):
        self.items.add(item_name)


class Game:

    def __init__(self):

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

        self.rooms = {"computer lab":
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

        self.items = {"notebook":
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

    def get_room_description(self, room_name):

        # Retrieve the current room by name
        room = self.rooms[room_name]

        # Print the room's description
        room_description = textwrap.wrap(room['description'])

        # Get the room's item list
        item_names = room['items']

        # Print a comma-separated list of the room's items, if any.
        if (len(item_names) > 0):
            items_text = "the room contains the following items: "
            for item_name in item_names:
                items_text += (item_name + ", ")
            items_text = items_text[:-2] # remove that last comma & space
            room_description.append(items_text)

        return room_description

    def get_room_score(self, room_name):
        room = self.rooms[room_name]
        return room['value']

    # Give a door_name in a room_name, return the name of the room you get to through
    # that door, or None if that's not a door name for the room.
    def get_room_from_door(self, room_name, door_name):
        room = self.rooms[room_name]
        doors = room["doors"]
        if door_name in doors:
            return doors[door_name]
        else:
            return None

    def get_intro(self):
        # TODO return an introduction to the game, with some helpful hints

        return "intro"

    def get_help(self):
        # TODO return help text

        return "help"

    def get_goodbye(self, score):
        # TODO print goodbye text, along with the player's current score

        return "goodbye: %d" % score

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
        # If so, call move_to_room() and return True.  Otherwise return False.

        #return True
        return check_move_command_soln(room_name, command)

    def check_general_command(room_name, command):
        # Level - 2

        # TODO see if the command is one that we want to respond to, without
        # doing anything. E.g. if they're swearing at us, tell them to keep
        # it clean. If we don't have any match, return False.

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
        move_to_room_soln(room_name)

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

        #print "I don't know how to take " + item_name
        take_item_command_soln(room_name, command)

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

        #print "I don't know how to examine " + item_name
        examine_item_command_soln(room_name, command)

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

        #print "I don't know how to drop " + item_name
        drop_item_command_soln(room_name, command)

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

    # This is a debugging function that ensures all rooms are reachable, and all
    # doors lead to a named room.
    def check_room_graph(self):
        current_room = self.rooms.keys().pop(0)
        visited_rooms = set()
        self.check_room(visited_rooms, current_room)

        # Now verify that we visited every room.
        for room in self.rooms.keys():
            if not room in visited_rooms:
                print "We never visited %s" % room
            else:
                print "We visited %s" % room

    def check_room(self, visited_rooms, room):
        if not room in visited_rooms:
            visited_rooms.add(room)
            doors = self.rooms[room]["doors"]
            for door in doors.keys():
                next_room = doors[door]
                print "%s from %s goes to %s" % (door, room, next_room)
                self.check_room(visited_rooms, next_room)

    # This is a debugging function that ensures all items are located in some
    # room, but only one room.
    def check_items(self):
        missing_items = set(self.items.keys())
        found_items = set()

        for room in g_rooms.keys():
            room_items = self.rooms[room]["items"]
            for room_item in room_items:
                if room_item in found_items:
                    print "%s is in two different rooms" % room_item
                else:
                    print "We found %s in %s" % (room_item, room)
                    found_items.add(room_item)

                missing_items.remove(room_item)

        for missing_item in missing_items:
            print "%s is not in any room" % missing_item


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

    if command == "check":
        check_room_graph()
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

