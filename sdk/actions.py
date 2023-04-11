from datatypes import ForwardOrBackWard, LeftOrRight, Vector2Int, Direction


def Move(direction: ForwardOrBackWard):
    return {"type": "Move", "direction": direction.value}


def Rotate(direction: LeftOrRight):
    return {"type": "Rotate", "direction": direction.value}


def Shoot():
    return {"type": "Shoot"}


def ChangeBullet():
    return {"type": "ChangeBullet"}


def PlaceBomb(position: Vector2Int):
    return {"type": "PlaceBomb", "position": position}


def AddLine(direction: Direction):
    return {"type": "AddLine", "direction": direction.value}


def RemoveLine(direction: Direction):
    return {"type": "RemoveLine", "direction": direction.value}


def ActivatePortal(destination_position: Vector2Int):
    return {"type": "ActivatePortal", "position": destination_position}


def Idle():
    return {"type": "Idle"}
