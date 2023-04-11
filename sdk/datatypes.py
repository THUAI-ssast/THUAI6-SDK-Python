from enum import Enum
import json


class Team(Enum):
    Red = 0
    Blue = 1

    def get_opposite_team(self) -> 'Team':
        return Team.Blue if self == Team.Red else Team.Red


class ForwardOrBackWard(Enum):
    Forward = 0
    Backward = 1


class LeftOrRight(Enum):
    Left = 0
    Right = 1


class LineInPortalPattern(Enum):
    # sorted by stroke order of Chinese character `日`
    LeftUp = 1
    LeftDown = 2
    Up = 4
    RightUp = 8
    RightDown = 16
    Center = 32
    Down = 64


class Direction(Enum):
    Up = LineInPortalPattern.Center
    Down = LineInPortalPattern.Down
    Left = LineInPortalPattern.LeftDown
    Right = LineInPortalPattern.RightDown


PortalPattern = int


class Vector2Int:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2Int(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2Int(self.x - other.x, self.y - other.y)


class Vector2IntEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Vector2Int):
            return {"x": obj.x, "y": obj.y}
        return super().default(obj)


class Vector2:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)


class PlayerState():

    def __init__(self, player_state_dict: dict):
        self.is_alive: bool = player_state_dict["isAlive"]
        self.is_shooting: bool = player_state_dict["isShooting"]
        self.is_changing_bullet: bool = player_state_dict["isChangingBullet"]
        self.is_placing_bomb: bool = player_state_dict["isPlacingBomb"]
        self.is_modifying_portal: bool = player_state_dict["isModifyingPortal"]
        self.is_activating_portal: bool = player_state_dict[
            "isActivatingPortal"]

        self.can_move: bool = player_state_dict["canMove"]
        self.can_rotate: bool = player_state_dict["canRotate"]
        self.can_shoot: bool = player_state_dict["canShoot"]
        self.can_change_bullet: bool = player_state_dict["canChangeBullet"]
        self.can_place_bomb: bool = player_state_dict["canPlaceBomb"]
        self.can_modify_portal: bool = player_state_dict["canModifyPortal"]
        self.can_activate_portal: bool = player_state_dict["canActivatePortal"]


class Player():
    # const properties that same for all players
    # to be decided. may be changed in the future
    # unit: meter, second, degree
    MAX_VELOCITY = 4.0
    ROTATION_SPEED = 600.0

    MAX_HP = 100
    MAX_AMMO = 30
    MAX_BOMB_COUNT = 1

    SHOOT_INTERVAL = 0.1
    CHANGE_BULLET_TIME = 2.5
    PLACE_BOMB_TIME = 2.0
    MODIFY_PORTAL_TIME = 0.5
    ACTIVATE_PORTAL_TIME = 1.0
    RESPAWN_TIME = 8.0

    BULLET_DAMAGE = 10
    BULLET_RANGE = 20.0
    # max distance between the player and the cell where the player can place a bomb
    MAX_BOMB_DISTANCE = 5.0

    def __init__(self, player_dict: dict):
        self.id: int = player_dict["id"]
        self.team: Team = player_dict["team"]
        self.state: PlayerState = PlayerState(player_dict["state"])
        self.hp: int = player_dict["hp"]
        self.ammo: int = player_dict["ammo"]
        self.bomb_count: int = player_dict["bombCount"]
        self.position: Vector2 = Vector2(player_dict["position"]["x"],
                                         player_dict["position"]["y"])
        self.rotation: float = player_dict["rotation"]


class Bomb():
    # to be decided. may be changed in the future
    # unit: meter, second
    EXPLOSION_TIME = 5.0
    EXPLOSION_RADIUS = 2.0
    EXPLOSION_DAMAGE = 100

    def __init__(self, bomb_dict: dict):
        self.position: Vector2Int = Vector2Int(bomb_dict["position"]["x"],
                                               bomb_dict["position"]["y"])


class Portal():
    # to be decided. may be changed in the future
    # the time between activation and teleportation. seconds
    WAIT_TIME = 3.0

    def __init__(self, portal_dict: dict):
        self.position: Vector2Int = Vector2Int(portal_dict["position"]["x"],
                                               portal_dict["position"]["y"])
        self.pattern: PortalPattern = portal_dict["pattern"]
        self.is_activated: bool = portal_dict["isActivated"]
