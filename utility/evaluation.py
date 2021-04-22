

def distance(coord1, coord2):
    """
    calculates the number of moves required to go directly from one coordinate to another,
    using the ideas discussed from here: https://www.redblobgames.com/grids/hexagons/

    Note that this code was used in Project COMP30024 part A
    """
    r1 = coord1[0]
    r2 = coord2[0]
    q1 = coord1[1]
    q2 = coord2[1]
    y1 = -(sum(coord1))
    y2 = -(sum(coord2))
    dr = r2 - r1
    dq = q2 - q1
    dy = y2 - y1

    return (abs(dr) + abs(dq) + abs(dy)) // 2