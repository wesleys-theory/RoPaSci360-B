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


class Action:
    """
    Class used for representing moves for the agent as well as communicating with referee
    """

    def __init__(self, token_type, coord_to, coord_from=False):
        """

        Args:
            token_type: integer representation of a token (e.g. U_SCISSORS or L_ROCK)
            coord_to: coordinate the token will land on
            coord_from: coordinate the token is moving from (if it is a "SLIDE" or "SWING" action)
        """
        if coord_from is False:
            self.throw_action = True
        else:
            self.throw_action = False

        self.old_coord = coord_from
        self.token_type = token_type
        self.new_coord = coord_to

    def referee_representation(self) -> tuple:
        """
        returns 'self' as a tuple representation as specified in specification-B.pdf
        """
        # TODO: implement this method


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

    def enact_actions(self, u_action: Action, l_action: Action):
        """
        performs the given actions by updating the board data
        """
        if not self.is_legal(u_action) or not self.is_legal(l_action):
            print("Error: move is not legal")
            return

        assert(u_action.token_type in [U_ROCK, U_PAPER, U_SCISSORS] and
               l_action.token_type in [L_ROCK, L_PAPER, L_SCISSORS])

        # Move tokens to their appropriate spots

        if u_action.throw_action:
            self.upper_throws -= 1
            if u_action.token_type is U_ROCK:
                self.upper_rocks.append(u_action.new_coord)
                self.board_dict[u_action.new_coord].append(U_ROCK)
            elif u_action.token_type is U_SCISSORS:
                self.upper_scissors.append(u_action.new_coord)
                self.board_dict[u_action.new_coord].append(U_SCISSORS)
            elif u_action.token_type is U_PAPER:
                self.upper_papers.append(u_action.new_coord)
                self.board_dict[u_action.new_coord].append(U_PAPER)
        else:
            if u_action.token_type is U_ROCK:
                self.upper_rocks.remove(u_action.old_coord)
                self.board_dict[u_action.old_coord].remove(U_ROCK)
                self.upper_rocks.append(u_action.new_coord)
                self.board_dict[u_action.new_coord].append(U_ROCK)
            elif u_action.token_type is U_SCISSORS:
                self.upper_scissors.remove(u_action.old_coord)
                self.board_dict[u_action.old_coord].remove(U_SCISSORS)
                self.upper_scissors.append(u_action.new_coord)
                self.board_dict[u_action.new_coord].append(U_SCISSORS)
            elif u_action.token_type is U_PAPER:
                self.upper_papers.remove(u_action.old_coord)
                self.board_dict[u_action.old_coord].remove(U_PAPER)
                self.upper_papers.append(u_action.new_coord)
                self.board_dict[u_action.new_coord].append(U_PAPER)

        if l_action.throw_action:
            self.lower_throws -= 1
            if l_action.token_type is L_ROCK:
                self.lower_rocks.append(l_action.new_coord)
                self.board_dict[l_action.new_coord].append(L_ROCK)
            elif l_action.token_type is L_SCISSORS:
                self.lower_scissors.append(l_action.new_coord)
                self.board_dict[l_action.new_coord].append(L_SCISSORS)
            elif l_action.token_type is L_PAPER:
                self.lower_papers.append(l_action.new_coord)
                self.board_dict[l_action.new_coord].append(L_PAPER)
        else:
            if l_action.token_type is L_ROCK:
                self.lower_rocks.remove(l_action.old_coord)
                self.board_dict[l_action.old_coord].remove(L_ROCK)
                self.lower_rocks.append(l_action.new_coord)
                self.board_dict[l_action.new_coord].append(L_ROCK)
            elif l_action.token_type is L_SCISSORS:
                self.lower_scissors.remove(l_action.old_coord)
                self.board_dict[l_action.old_coord].remove(L_SCISSORS)
                self.lower_scissors.append(l_action.new_coord)
                self.board_dict[l_action.new_coord].append(L_SCISSORS)
            elif l_action.token_type is L_PAPER:
                self.lower_papers.remove(l_action.old_coord)
                self.board_dict[l_action.old_coord].remove(L_PAPER)
                self.lower_papers.append(l_action.new_coord)
                self.board_dict[l_action.new_coord].append(L_PAPER)

        # Tokens have moved, now perform any necessary battles
        self.battle(u_action.new_coord)
        self.battle(l_action.new_coord)

        self.move_count += 1

        # TODO: test the SHIT out of this method and maybe add draw/win condition checking ?

    def is_legal(self, move: Action) -> bool:
        """
        checks if the move is legal or not
        """
        if move.throw_action:
            if move.token_type >= L_ROCK:
                num_throws = 9 - self.lower_throws
                rows_available = range(-4, -4 + num_throws + 1)
            else:
                num_throws = self.upper_throws
                rows_available = range(4 - num_throws, 4 + 1)

            return move.new_coord[0] in rows_available

        assert(move.old_coord is not False)
        coord = move.old_coord
        assert(isinstance(coord, tuple))

        adjacents = [(coord[0] + 1, coord[1]), (coord[0] - 1, coord[1]), (coord[0], coord[1] + 1),
                     (coord[0], coord[1] - 1), (coord[0] - 1, coord[1] + 1), (coord[0] + 1, coord[1] - 1)]

        if move.new_coord not in adjacents:
            # Coord updated to coord moved to such that intersection of 2 adjacent sets are where possible swing
            # tokens lie

            # Swing moves
            coord = move.new_coord
            new_adjacents = [(coord[0] + 1, coord[1]), (coord[0] - 1, coord[1]), (coord[0], coord[1] + 1),
                             (coord[0], coord[1] - 1), (coord[0] - 1, coord[1] + 1), (coord[0] + 1, coord[1] - 1)]
            intersect = list(set.intersection(set(adjacents), set(new_adjacents)))

            for coord in intersect:
                if move.token_type >= L_ROCK:
                    for piece in self.board_dict[coord]:
                        if piece >= L_ROCK:
                            return True
                else:
                    for piece in self.board_dict[coord]:
                        if piece < L_ROCK:
                            return True
            return False

        elif move.new_coord not in ALL_HEXES:
            return False
        return True


def remove_all(lst: list, val):
    """
    remove all instances of 'val' from 'lst'. Used in 'battle' method
    """
    for i in range(lst.count(val)):
        lst.remove(val)