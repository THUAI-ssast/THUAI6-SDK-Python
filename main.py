from collections import defaultdict
import logging
import random
from typing import List, Dict

import sdk.actions as actions
from sdk.controller import run_ai
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
    players: List[Player] = observation["players"]
    bombs: List[Bomb] = observation["bombs"]
    portals_by_pattern: Dict[
        PortalPattern,
        List[Portal]] = observation["portalsClassifiedByPattern"]

    bombs_map = defaultdict(list)
    for bomb in bombs:
        bombs_map[bomb.position].append(bomb)
    portals_map = {
        portal.position: portal
        for portals in portals_by_pattern.values() for portal in portals
    }

    my_player: Player = players[my_id]
    my_state: PlayerState = my_player.state
    my_cell = utils.to_cell(my_player.position)
    p = random.random()
    if p < 0.01:
        if my_player.bomb_count > 0 and my_state.can_place_bomb:
            return actions.PlaceBomb(my_cell)
    elif p < 0.02:
        if my_state.can_activate_portal:
            if my_portal := portals_map.get(my_cell):
                dest_portal = random.choice(
                    portals_by_pattern[my_portal.pattern])
                return actions.ActivatePortal(dest_portal.position)
        if my_state.can_modify_portal:
            while True:
                direction = random.choice(list(Direction))
                if utils.can_modify_portal_line(my_cell, direction, map_info):
                    return actions.AddLine(direction)
        return actions.Idle()
    elif p < 0.20:
        return actions.Rotate(LeftOrRight.Left)
    elif p < 0.25:
        return actions.Move(ForwardOrBackWard.Backward)
    elif p < 0.50:
        return actions.Shoot() if my_player.ammo > 0 else actions.ChangeBullet(
        )
    else:
        return actions.Move(ForwardOrBackWard.Forward)
    return actions.Idle()


# Don't change this.
run_ai(init, get_action)
