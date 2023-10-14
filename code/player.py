from math import inf
from copy import deepcopy


class Player:

    def __init__(self, symbol):
        self.symbol = symbol
        self.number = 1 if self.symbol == 'X' else -1
        self.is_their_turn = True if self.symbol == 'X' else False
        self.is_ai = False

    def make_best_move_using_alpha_beta_minimax(self, other, game):

        ai_number = self.number

        def alpha_beta(board, depth, alpha, beta, number):
            move = (-1, -1)
            if depth == 0:
                return [move, 0]
            elif game.is_won(board, 1):
                return [move, 1]
            elif game.is_won(board, -1):
                return [move, -1]
            else:
                for i, j in game.blanks(board):
                    board[i][j] = number
                    score = alpha_beta(board, depth - 1, alpha, beta, -number)[1]
                    if number == 1:
                        if score > alpha:
                            move, alpha = (i, j), score
                    else:
                        if score < beta:
                            move, beta = (i, j), score
                    board[i][j] = 0
                    if alpha >= beta:
                        break
                if number == 1:
                    return [move, alpha]
                else:
                    return [move, beta]

        x, y = alpha_beta(deepcopy(game.board), len(game.blanks(game.board)), -inf, inf, ai_number)[0]
        game.board[x][y] = ai_number
        if game.is_won(game.board, ai_number):
            game.execute_win_scenario(self)
        elif game.is_draw(game.board):
            game.execute_draw_scenario()
        self.is_their_turn, other.is_their_turn = not self.is_their_turn, not other.is_their_turn

    def make_move(self, other, coordinates, game):
        x, y = coordinates
        game.board[x][y] = self.number
        if game.is_won(game.board, self.number):
            game.execute_win_scenario(self)
        elif game.is_draw(game.board):
            game.execute_draw_scenario()
        self.is_their_turn, other.is_their_turn = not self.is_their_turn, not other.is_their_turn
