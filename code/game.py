import pygame
import sys
import time
import numpy as np
from random import choice
from settings import *
from gui import GUI


class Game:

    def __init__(self, size=3):
        self.size = size
        self.board = np.zeros([self.size, self.size], dtype=int)
        self.is_on = False
        self.draw = False
        self.x_won = False
        self.o_won = False
        self.x_score = 0
        self.o_score = 0
        self.is_score_updated = False

    @staticmethod
    def blanks(board):
        result = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    result.append((i, j))
        return result

    def new_game(self, players):
        self.is_on = False
        self.x_won = self.o_won = self.draw = False
        self.is_score_updated = False
        if players[0].number == 1:
            players[0].is_their_turn = True
            players[1].is_their_turn = False
        else:
            players[0].is_their_turn = False
            players[1].is_their_turn = True
        players[0].is_ai = players[1].is_ai = False
        self.board = np.zeros([self.size, self.size], dtype=int)

    @staticmethod
    def is_draw(board):
        if any([board[row][col] == 0 for row in range(len(board)) for col in range(len(board[0]))]):
            return False
        return True

    @staticmethod
    def is_won(board, number):
        # check each row
        if any([all([board[row][col] == number for col in range(len(board))]) for row in range(len(board[0]))]):
            return True
        # check each column
        if any([all([board[row][col] == number for row in range(len(board))]) for col in range(len(board[0]))]):
            return True
        # check both diagonals
        if all(board[x][x] == number for x in range(len(board))):
            return True
        if all(board[-1-x][x] == number for x in range(len(board))):
            return True
        return False

    def is_empty(self):
        return len(self.blanks(self.board)) == 9

    def execute_win_scenario(self, player):
        if player.number == 1:
            self.x_won = True
        elif player.number == -1:
            self.o_won = True

    def execute_draw_scenario(self):
        self.draw = True

    def make_moves(self, players, coordinates):
        player1, player2 = players
        mouse_x, mouse_y = coordinates
        if player1.is_their_turn:
            if not player1.is_ai:
                if mouse_x and mouse_y:
                    if BOARD_LEFT_X <= mouse_x <= BOARD_RIGHT_X and BOARD_LOWER_Y <= mouse_y <= BOARD_UPPER_Y:
                        x = int(self.size * (mouse_y - BOARD_LOWER_Y) / BOARD_HEIGHT)
                        y = int(self.size * (mouse_x - BOARD_LEFT_X) / BOARD_WIDTH)
                        if self.board[x][y] == 0:
                            player1.make_move(player2, (x, y), self)
            else:
                player1.make_best_move_using_alpha_beta_minimax(player2, self)

        elif player2.is_their_turn:
            if not player2.is_ai:
                if mouse_x and mouse_y:
                    if BOARD_LEFT_X <= mouse_x <= BOARD_RIGHT_X and BOARD_LOWER_Y <= mouse_y <= BOARD_UPPER_Y:
                        x = int(self.size * (mouse_y - BOARD_LOWER_Y) / BOARD_HEIGHT)
                        y = int(self.size * (mouse_x - BOARD_LEFT_X) / BOARD_WIDTH)
                        if self.board[x][y] == 0:
                            player2.make_move(player1, (x, y), self)
            else:
                player2.make_best_move_using_alpha_beta_minimax(player1, self)

    def update_score(self):
        if self.x_won:
            self.x_score += 1
        elif self.o_won:
            self.o_score += 1
        elif self.draw:
            self.x_score += 0.5
            self.o_score += 0.5
        self.is_score_updated = True


class GameState:

    @staticmethod
    def static_elements(screen, background, game, players, buttons, small_font):

        global SCREEN_COLOR

        # display background
        screen.fill(SCREEN_COLOR)
        background.fill(BG_COLOR)
        screen.blit(background, (0, 120))

        # display buttons
        x_button, o_button = buttons
        x_text = "Xs | {0} {1}".format(game.x_score, "(AI)" if players[0].is_ai and game.is_on else "")
        x_button.draw(game.is_on and not (game.draw or game.x_won or game.o_won), players[0].is_their_turn, x_text)
        o_text = "Os | {0} {1}".format(game.o_score, "(AI)" if players[1].is_ai and game.is_on else "")
        o_button.draw(game.is_on and not (game.draw or game.x_won or game.o_won), players[1].is_their_turn, o_text)

        if game.is_on or not game.is_empty():
            GUI.display_upper_text(screen, game, players, small_font)

        if game.is_on and max(SCREEN_COLOR) > 0:
            SCREEN_COLOR = tuple(c - 1 for c in SCREEN_COLOR)

    @staticmethod
    def stage_1(screen, game, players, font, events):
        # beginning of the game
        a_pressed = False
        h_pressed = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    a_pressed = True
                elif event.key == pygame.K_h:
                    h_pressed = True

        GUI.display_choice(screen, font)
        if a_pressed:
            choice(players).is_ai = True
            game.is_on = True
        elif h_pressed:
            game.is_on = True

    @staticmethod
    def stage_2(screen, board_surface, game, players, medium_font, events, has_countdown_begun, time_0, time_1):

        mouse_coordinates = (None, None)
        any_key_pressed = False

        for event in events:
            if event.type == pygame.KEYDOWN:
                any_key_pressed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coordinates = event.pos

        GUI.display_board(screen, board_surface, game)
        if not (game.draw or game.x_won or game.o_won):
            game.make_moves(players, mouse_coordinates)
        else:
            GUI.display_lower_text(screen, medium_font)

        if (game.draw or game.x_won or game.o_won) and not has_countdown_begun:
            time_0 = time.time()
            has_countdown_begun = True

        if has_countdown_begun:
            time_1 = time.time()

        if (game.draw or game.x_won or game.o_won) and (any_key_pressed or time_1 - time_0 >= 5):
            has_countdown_begun = False
            time_0 = time_1 = 0
            game.is_on = False

        return has_countdown_begun, time_0, time_1

    @staticmethod
    def stage_3(screen, board_surface, game, players, medium_font, large_font, events):
        # end of the game
        space_pressed = False
        escape_pressed = False

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                elif event.key == pygame.K_ESCAPE:
                    escape_pressed = True

        if not game.is_score_updated:
            game.update_score()
        GUI.display_game_result_and_ask_to_play_again(screen, board_surface, game, medium_font, large_font)
        if space_pressed:
            game.new_game(players)
            global SCREEN_COLOR
            SCREEN_COLOR = WHITE
        elif escape_pressed:
            pygame.quit()
            sys.exit()
