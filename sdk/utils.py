import math

from datatypes import Vector2, Vector2Int, Direction


def to_cell_center(pos: Vector2Int):
    '''
    Convert a cell position to the center of the cell
    '''
    return Vector2(pos.x + 0.5, pos.y + 0.5)


def to_cell(pos: Vector2):
    '''
    Convert a position to the cell it is in
    '''
    return Vector2Int(int(pos.x), int(pos.y))


def distance(pos1: Vector2, pos2: Vector2):
    '''
    Calculate the distance between two positions
    '''
    return ((pos1.x - pos2.x)**2 + (pos1.y - pos2.y)**2)**0.5


def angle(pos1: Vector2, pos2: Vector2):
    '''
    Calculate the angle p
    '''
    return math.atan2(pos2.y - pos1.y, pos2.x - pos1.x)


def is_in_portal(position: Vector2, portal_position: Vector2Int):
    return (position.x >= portal_position.x and position.x <
            portal_position.x + 1) and (position.y >= portal_position.y
                                        and position.y < portal_position.y + 2)


def is_in_map(cell_position: Vector2Int, map_info: list[list[int]]):
    return (cell_position.x >= 0 and cell_position.x < len(map_info)) and (
        cell_position.y >= 0 and cell_position.y < len(map_info[0]))


def is_road(cell_position: Vector2Int, map_info: list[list[int]]):
    return is_in_map(
        cell_position,
        map_info) and map_info[cell_position.x][cell_position.y] == 0


def can_modify_portal_line(cell_position: Vector2Int, direction: Direction,
                           map_info: list[list[int]]):
    if not is_road(cell_position, map_info):
        return False
    if direction == Direction.Up:
        return is_road(cell_position + Vector2Int(0, 1), map_info)
    elif direction == Direction.Down:
        return is_road(cell_position + Vector2Int(0, -1), map_info)
    elif direction == Direction.Left:
        return is_road(cell_position + Vector2Int(-1, 0), map_info)
    elif direction == Direction.Right:
        return is_road(cell_position + Vector2Int(1, 0), map_info)
    else:
        return False
