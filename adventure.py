inventory = []
room = "computerlab"
keep_going = True

# rooms is a dictionary, where the key is the room name, and the value is a "room"
# A "room" is a dictionary, where the key is one of several possible values
#   description -> string that describes the room
#   items -> list of item names
#   doors -> dictionary that maps from a door name ("north", "up", etc) to a room name

rooms = {"computerlab":
             {"description": "The computer lab is filled with glowing screens and old chairs",
              "items": ["notebook"],
              "doors": {"exit": "hallway"}},
         "hallway":
             {"description": "The hallway is filled with colorful murals",
              "items": [],
              "doors": {"north": "computerlab", "east": "lobby"}}
}


# TODO print an introduction to the game, with some helpful hints

while keep_going:
    # Print the description of the current room
    print(rooms[room]["description"])

    # TODO print a list of items in the room, if there are any

    command = raw_input("What do you want to do? ")

    # TODO support other commands, like "list" for a list of things you've picked up,
    # or "take xxx" to take an item in the current room, or "drop xxx" to drop an item
    # in that room, or "help" to list commands, or "look" to print the room description,
    # or "use xxx" to use an item

    if command == "bye":
        keep_going = False
    elif command in rooms[room]["doors"]:
        # It's a direction for leaving the current room, so go to the room in that direction
        room = rooms[room]["doors"][command]
    else:
        print("I'm not sure what you want me to do")

