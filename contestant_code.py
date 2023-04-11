import random

import sdk.actions as actions
from sdk.datatypes import *
import sdk.utils as utils


def init(observation: dict):
    '''
    Called at the beginning of the game.
    '''
    # SDK won't use these global variables.
    # You can edit them as you like.
    # Note: global variables cannot be type-annotated.
    global map_info
    global my_id
    global my_team
    map_info = observation["map"]
    my_id = observation["myId"]
    my_team = observation["myTeam"]


def get_action(observation: dict):
    '''
    Called every frame.
    '''
    players: list[Player] = observation["players"]
    bombs: list[Bomb] = observation["bombs"]
    portals: dict[PortalPattern,
                  list[Portal]] = observation["portalsClassifiedByPattern"]

    my_player: Player = players[my_id]
    p = random.random()
    if p < 0.01:
        return actions.PlaceBomb(utils.to_cell(
            my_player.position)) if my_player.bomb_count > 0 else actions.Idle(
            )
    elif p < 0.05:
        return actions.Idle()
    elif p < 0.20:
        return actions.Rotate(LeftOrRight.Left)
    elif p < 0.25:
        return actions.Rotate(LeftOrRight.Right)
    elif p < 0.60:
        return actions.Shoot() if my_player.ammo > 0 else actions.ChangeBullet(
        )
    else:
        return actions.Move(ForwardOrBackWard.Forward)
