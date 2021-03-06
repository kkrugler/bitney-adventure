# Bitney adventure game that you play from the console

import bag_engine

# Get the new player's name, and add them to the game.
player_name = raw_input("What is your name? ")
bag_engine.player_start(player_name)

# Keep looping until the game is complete (or the user enters "bye")
while not bag_engine.game_complete(player_name):

    # Print any messages that have been accumulated for the player
    bag_engine.print_and_clear_msgs(player_name)

    # Get the user's command
    command = raw_input("> ")

    # When player_command returns False, we're all done
    if not bag_engine.player_command(player_name, command):
        break;

# Output any final text
bag_engine.print_and_clear_msgs(player_name)
