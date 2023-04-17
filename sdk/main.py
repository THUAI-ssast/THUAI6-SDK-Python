import json
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

    start_observation: dict = json.loads(input(),
                                         object_hook=from_start_observation)
    try:
        init(start_observation)
    except Exception as e:
        print(e, file=sys.stderr)

    while True:
        observation: dict = json.loads(input(), object_hook=from_observation)

        try:
            action = get_action(observation)
            if not isinstance(action, dict):
                action = ac.Idle()
        except Exception as e:
            action = ac.Idle()
            print(e, file=sys.stderr)

        action["frame"] = observation["frame"]
        print(json.dumps(action, cls=dt.MyJSONEncoder), flush=True)
