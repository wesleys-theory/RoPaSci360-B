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
        print("self.upper = ", self.upper)

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
        # put your code here
        actions = []
        # convert tuple to 'Action' object


        for action in (opponent_action, player_action):
            if action[0] == "THROW":
                piece_type = action[1]
                if piece_type == "r":
                    piece = 3
                elif piece_type == "s":
                    piece = 5
                elif piece_type == "p":
                    piece = 4
                elif piece_type == "R":
                    piece = 0
                elif piece_type == "S":
                    piece = 2
                elif piece_type == "P":
                    piece = 1

                actions.append(Action(piece, action[2]))
            else:
                piece = self.board.board_dict[action[1]][1]
                actions.append(Action(piece, action[2], action[1]))

        if self.upper:
            self.board.enact_actions(actions[1], actions[0])
        else:
            self.board.enact_actions(actions[0], actions[1])
