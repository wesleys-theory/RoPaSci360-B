from utility.UI_helpers import AgentBoard, Action
from utility.evaluation import choose_best_action

class Player:
    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        # put your code here

        self.board = AgentBoard()
        self.upper = (player == "upper")

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here
        output = choose_best_action(self.board, self.upper)
        return output.referee_representation()

    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        piece_type = player_action[1]
        if self.upper:
            if piece_type == "r":
                piece = 0
            elif piece_type == "p":
                piece = 1
            elif piece_type == "s":
                piece = 2
        else:
            if piece_type == "r":
                piece = 3
            elif piece_type == "p":
                piece = 4
            elif piece_type == "s":
                piece = 5

        if player_action[0] == "THROW":
            our_action = Action(piece, player_action[2])
        else:
            piece = self.board.board_dict[player_action[1]][0]
            if piece > 2 and self.upper:
                piece -= 3
            elif piece < 2 and not self.upper:
                piece += 3
            our_action = Action(piece, player_action[2], player_action[1])

        piece_type = opponent_action[1]
        if not self.upper:
            if piece_type == "r":
                piece = 0
            elif piece_type == "p":
                piece = 1
            elif piece_type == "s":
                piece = 2
        else:
            if piece_type == "r":
                piece = 3
            elif piece_type == "p":
                piece = 4
            elif piece_type == "s":
                piece = 5

        if opponent_action[0] == "THROW":
            their_action = Action(piece, opponent_action[2])
        else:
            piece = self.board.board_dict[opponent_action[1]][0]
            if piece > 2 and not self.upper:
                piece -= 3
            elif piece < 2 and self.upper:
                piece += 3
            their_action = Action(piece, opponent_action[2], opponent_action[1])

        if self.upper:
            self.board.enact_actions(our_action, their_action)
        else:
            self.board.enact_actions(their_action, our_action)