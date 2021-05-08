from utility.UI_helpers import AgentBoard, Action
from utility.gametheory import solve_game
from copy import deepcopy
import random


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


def evaluate(board: AgentBoard) -> float:
    """
    Gives a score for how profitable the board is; positive means good for upper, negative means good for lower
    """

    features = []
    weights = []

    # first feature: ratio of winning pieces to losing pieces
    piece_lists = [len(board.upper_rocks), len(board.upper_scissors), len(board.upper_papers),
                   len(board.lower_papers), len(board.lower_rocks), len(board.lower_scissors)]
    inverse_pieces = [len(board.lower_scissors), len(board.lower_papers), len(board.lower_rocks),
                      len(board.upper_rocks), len(board.upper_scissors), len(board.upper_papers)]

    upper_ratio = 0
    lower_ratio = 0

    for i in range(3):
        if inverse_pieces[i] == 0 and (board.lower_throws == 0) and piece_lists[i] > 0:
            board.upper_winner = True
        else:
            upper_ratio += piece_lists[i] / (inverse_pieces[i] + 1)
    for i in range(3, 6):
        if piece_lists[i] == 0 and (board.upper_throws == 0) and inverse_pieces[i] > 0:
            board.lower_winner = True
        else:
            lower_ratio += piece_lists[i] / (inverse_pieces[i] + 1)

    ratio_feature = upper_ratio - lower_ratio
    ratio_weight = 200
    features.append(ratio_feature)
    weights.append(ratio_weight)

    # second feature: distance from upper 'winning' pieces to lower 'losing' pieces minus vice-versa
    upper_distance = \
        pieces_distance(board.upper_rocks, board.lower_scissors) + \
        pieces_distance(board.upper_scissors, board.lower_papers) + \
        pieces_distance(board.upper_papers, board.lower_rocks)
    lower_distance = \
        pieces_distance(board.lower_rocks, board.upper_scissors) + \
        pieces_distance(board.lower_scissors, board.upper_papers) + \
        pieces_distance(board.lower_papers, board.upper_rocks)

    distance_feature = 1 / (upper_distance + 1) - 1 / (lower_distance + 1)
    distance_weight = 0
    features.append(distance_feature)
    weights.append(distance_weight)

    # third feature: number of upper pieces on the board - number of lower pieces
    num_upper_pieces = len(board.upper_rocks) + len(board.upper_papers) + len(board.upper_scissors)
    num_lower_pieces = len(board.lower_rocks) + len(board.lower_papers) + len(board.lower_scissors)

    pieces_feature = num_upper_pieces - num_lower_pieces
    pieces_weight = 10
    features.append(pieces_feature)
    weights.append(pieces_weight)

    # fourth feature: difference in remaining throws
    throws_feature = board.upper_throws - board.lower_throws
    throws_weight = 3
    features.append(throws_feature)
    weights.append(throws_weight)

    # fifth feature: number of hexes with duplicate pieces
    upper_piece_lists = [board.upper_rocks, board.upper_papers, board.upper_scissors]
    lower_piece_lists = [board.lower_rocks, board.lower_papers, board.lower_scissors]

    num_upper_duplicates = 0
    num_lower_duplicates = 0
    for piece_list in upper_piece_lists:
        num_upper_duplicates += len(piece_list) - len(set(piece_list))

    for piece_list in lower_piece_lists:
        num_lower_duplicates += len(piece_list) - len(set(piece_list))

    duplicate_feature = num_lower_duplicates - num_upper_duplicates
    duplicate_weight = 3
    features.append(duplicate_feature)
    weights.append(duplicate_weight)

    output = 0
    for i in range(len(features)):
        output += features[i] * weights[i]
    return output


def pieces_distance(attacking_pieces: list, defending_pieces: list):
    """
    For each piece in defending_pieces, calculates the distance to the closest attacking piece. Returns the sum
    of these distances.
    """

    output = 0

    if len(attacking_pieces) > 0 and len(defending_pieces) > 0:
        for defender in defending_pieces:
            dist_list = []
            for attacker in attacking_pieces:
                dist_list.append(distance(defender, attacker))
            output += min(dist_list)

    return output


def choose_best_action(board: AgentBoard, upper: bool) -> Action:
    """
    Creates a payoff matrix using the 'evaluate' function and uses the given solve_game function to choose a move
    according to the probability distribution 'strategy'
    """
    upper_actions = board.generate_all(0)
    lower_actions = board.generate_all(5)

    matrix = []
    for u_action in upper_actions:
        row = []
        for l_action in lower_actions:
            board_copy = deepcopy(board)
            board_copy.enact_actions(u_action, l_action)
            row.append(evaluate(board_copy))
        matrix.append(row)

    strategy, v = solve_game(matrix, upper, upper)

    if upper:
        return random.choices(upper_actions, strategy)[0]
    else:
        return random.choices(lower_actions, strategy)[0]


def choose_random_action(board: AgentBoard, upper: bool) -> Action:
    upper_actions = board.generate_all(0)
    lower_actions = board.generate_all(5)

    if upper:
        return random.choices(upper_actions)[0]
    else:
        return random.choices(lower_actions)[0]
