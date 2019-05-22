from btnode import BTNode
from board import Board
import random
import copy


class BTree:
    def __init__(self, board=None):
        self._root = BTNode(board)

    def build_tree(self, player_character, other_character):
        """
        Build a tree from given only first board
        :return: best move of to randomly selected
        """

        def recurse(top, depth):
            """
            recursive tree traversal and counting winning positions
            :param top: top vertex of subtree to count winning positions on
            :return: coefficient representing how good the position is
            """
            if top is None:
                return -10000, None
            if top.board.winner() == player_character:
                return 1, None
            if top.board.winner() == "Draw":
                return 0, None
            if top.board.winner():
                return -1, None
            if depth % 2 == 0:
                character = player_character
            else:
                character = other_character

            possible_positions = top.board.possible_moves()
            position_left = ()
            position_right = ()
            if len(possible_positions) > 0:
                position_right = random.choice(possible_positions)
                possible_positions.remove(position_right)
                new_board = copy.deepcopy(top.board)
                new_board.make_move(position_right, character)
                top.right = BTNode(new_board)
            if len(possible_positions) > 0:
                position_left = random.choice(possible_positions)
                possible_positions.remove(position_left)
                new_board = copy.deepcopy(top.board)
                new_board.make_move(position_left, character)
                top.left = BTNode(new_board)
            rec_right = recurse(top.right, depth + 1)[0]
            rec_left = recurse(top.left, depth + 1)[0]
            if rec_right > rec_left:
                return rec_right + rec_left, position_right
            else:
                return rec_right + rec_left, position_left

        return recurse(self._root, 0)
