import json
import logging
import sys
import os

import actions as ac
import datatypes as dt


def from_start_observation(d: dict) -> dict:
    d["myTeam"] = dt.Team(d["myTeam"])
    return d


def from_observation(d: dict) -> dict:
    if "frame" not in d:
        return d
    d["players"] = [dt.Player(p) for p in d["players"]]
    d["bombs"] = [dt.Bomb(b) for b in d["bombs"]]
    d["portalsClassifiedByPattern"] = {
        dt.PortalPattern(pattern_str): [dt.Portal(p) for p in p_list]
        for pattern_str, p_list in d["portalsClassifiedByPattern"].items()
    }
    return d


if __name__ == "__main__":
    # Import contestant code
    sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
    from contestant_code import init, get_action

    logging.basicConfig(filename='ai.log', level=logging.DEBUG)

    start_obs_str = input()
    start_obs = json.loads(start_obs_str, object_hook=from_start_observation)
    try:
        init(start_obs)
    except Exception as e:
        logging.debug(start_obs_str)
        logging.exception(e)
    while True:
        obs_str = input()
        obs = json.loads(obs_str, object_hook=from_observation)

        try:
            action = get_action(obs)
            if not isinstance(action, dict):
                action = ac.Idle()
        except Exception as e:
            action = ac.Idle()
            logging.debug(obs_str)
            logging.exception(e)

        action["frame"] = obs["frame"]
        print(json.dumps(action, cls=dt.MyJSONEncoder), flush=True)
