"""
Functions and data structures that help with communicating between players and the referee
"""

# Global constants for list of all hex coordinates
HEX_RANGE = range(-4, 4 + 1)
ALL_HEXES = [(r, q) for r in HEX_RANGE for q in HEX_RANGE if -r - q in HEX_RANGE]

# Global constants for Rock/Paper/Scissor symbols
U_ROCK = 0
U_PAPER = 1
U_SCISSORS = 2
L_ROCK = 3
L_PAPER = 4
L_SCISSORS = 5


class AgentBoard:
    """
    Representation of the game board used for searching by Player class
    """

    def __init__(self):
        # counter for number of moves, after move 360, game is draw
        self.move_count = 0

        # remaining "throw" tokens for both sides
        self.upper_throws = 9
        self.lower_throws = 9

        # board dictionary indexed by coordinates where each coordinate is initially empty
        self.board_dict = {coord: [] for coord in ALL_HEXES}

        # list of token locations for each token type for both players
        self.upper_rocks = []
        self.upper_papers = []
        self.upper_scissors = []
        self.lower_rocks = []
        self.lower_papers = []
        self.lower_scissors = []

    def battle(self, coord: tuple):
        """
        battle and remove losing type(s) from the board
        """
        tokens = self.board_dict[coord].copy()
        if len(tokens) == 0:
            return
        if U_ROCK in tokens or (L_ROCK in tokens):
            remove_all(self.board_dict[coord], U_SCISSORS)
            remove_all(self.board_dict[coord], L_SCISSORS)
            remove_all(self.upper_scissors, coord)
            remove_all(self.lower_scissors, coord)
        if U_PAPER in tokens or (L_PAPER in tokens):
            remove_all(self.board_dict[coord], U_ROCK)
            remove_all(self.board_dict[coord], L_ROCK)
            remove_all(self.upper_rocks, coord)
            remove_all(self.lower_rocks, coord)
        if U_SCISSORS in tokens or (L_SCISSORS in tokens):
            remove_all(self.board_dict[coord], U_PAPER)
            remove_all(self.board_dict[coord], L_PAPER)
            remove_all(self.upper_papers, coord)
            remove_all(self.lower_papers, coord)


def remove_all(lst: list, val):
    """
    remove all instances of 'val' from 'lst'. Used in 'battle' method
    """
    for i in range(lst.count(val)):
        lst.remove(val)