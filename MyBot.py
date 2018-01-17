"""
Welcome to your first Halite-II bot !

This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
2.a. Try to Dock in the planet if close enough
2.b If not, go towards the planet

Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
#import time
# Then let's import the logging module so we can print out information
import logging

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Settler")
# Then we print our start message to the logs
logging.info("Starting my Settler bot!")

while True:
    # TURN START
    # Get the time at the beginning of the Turn
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    # For every ship that I control
    for ship in game_map.get_me().all_ships():

      if ship.docking_status != ship.DockingStatus.UNDOCKED:
        # Skip this ship
        continue

      entities_by_distance = game_map.nearby_planets_by_distance(ship)
      nearest_planet = None
      for distance in sorted(entities_by_distance):
        nearest_planet = next((nearest_entity for nearest_entity in entities_by_distance[distance] if
                                      isinstance(nearest_entity, hlt.entity.Planet)), None)
        if nearest_planet == None:
            continue

        canDockHere = (nearest_planet.is_owned() and
                      (nearest_planet.owner == ship.owner) and
                      not nearest_planet.is_full()) or (not nearest_planet.is_owned())

        if canDockHere:
            if ship.can_dock(nearest_planet):
                # We add the command by appending it to the command_queue
                command_queue.append(ship.dock(nearest_planet))
            else:
                navigate_command = ship.navigate(
                    ship.closest_point_to(nearest_planet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)
            break
        else:
            continue   # now get after those planets not highest priority docked to



    game.send_command_queue(command_queue)

    # TURN END
# GAME END
