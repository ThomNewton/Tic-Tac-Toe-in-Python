import pygame
from settings import *


class GUI:
    @staticmethod
    def display_board(screen, board_surface, game):
        board_surface.fill(BOARD_COLOR)
        pygame.draw.line(board_surface,
                         LINE_COLOR,
                         (0, BOARD_HEIGHT // 3),
                         (BOARD_WIDTH, BOARD_HEIGHT // 3),
                         LINE_WIDTH)
        # 2nd horizontal
        pygame.draw.line(board_surface,
                         LINE_COLOR,
                         (0, 2 * BOARD_HEIGHT // 3),
                         (BOARD_WIDTH, 2 * BOARD_HEIGHT // 3),
                         LINE_WIDTH)
        # 1st vertical
        pygame.draw.line(board_surface,
                         LINE_COLOR,
                         (BOARD_WIDTH // 3, 0),
                         (BOARD_WIDTH // 3, BOARD_HEIGHT),
                         LINE_WIDTH)
        # 2nd vertical
        pygame.draw.line(board_surface,
                         LINE_COLOR,
                         (2 * BOARD_WIDTH // 3, 0),
                         (2 * BOARD_WIDTH // 3, BOARD_HEIGHT),
                         LINE_WIDTH)

        # Xs and Os
        for row in range(game.size):
            for col in range(game.size):
                if game.board[row][col] == 1:
                    x_left = int(col * BOARD_WIDTH / 3) + 40
                    x_right = int(col * BOARD_WIDTH / 3 + BOARD_WIDTH / 3) - 40
                    y_up = int(row * BOARD_HEIGHT / 3 + BOARD_HEIGHT / 3) - 30
                    y_down = int(row * BOARD_HEIGHT / 3) + 30
                    pygame.draw.line(board_surface, GREY, (x_left, y_down), (x_right, y_up), X_WIDTH)
                    pygame.draw.line(board_surface, GREY, (x_left, y_up), (x_right, y_down), X_WIDTH)
                elif game.board[row][col] == -1:
                    x = int(col * BOARD_WIDTH / 3 + BOARD_WIDTH / 6)
                    y = int(row * BOARD_HEIGHT / 3 + BOARD_HEIGHT / 6)
                    pygame.draw.circle(board_surface, WHITE, (x, y), CIRCLE_RADIUS, CIRCLE_WIDTH)

        screen.blit(board_surface, (BOARD_CENTER_X, BOARD_CENTER_Y))

    @staticmethod
    def display_game_result_and_ask_to_play_again(screen, board_surface, game, medium_font, large_font):

        board_surface.fill(BOARD_COLOR)

        result_message = ""
        color = WHITE

        # Xs
        x_left = int(BOARD_WIDTH / 3) + 40
        x_right = int(2 * BOARD_WIDTH / 3) - 40
        y_up = int(2 * BOARD_HEIGHT / 3) - 30
        y_down = int(BOARD_HEIGHT / 3) + 30

        # Os
        x = int(BOARD_WIDTH / 2)
        y = int(BOARD_HEIGHT / 2)

        if game.draw:

            result_message += "It's a draw!"

            # exact horizontal correction
            extra_dist = BOARD_WIDTH // 6
            x_left -= extra_dist
            x_right -= extra_dist
            x += extra_dist

            # draw X and O
            pygame.draw.line(board_surface, GREY, (x_left, y_down), (x_right, y_up), X_WIDTH)
            pygame.draw.line(board_surface, GREY, (x_left, y_up), (x_right, y_down), X_WIDTH)
            pygame.draw.circle(board_surface, WHITE, (x, y), CIRCLE_RADIUS, CIRCLE_WIDTH)

        elif game.x_won:

            color = XS_COLOR
            result_message += "X's won. Congratulations!"

            # draw X
            pygame.draw.line(board_surface, GREY, (x_left, y_down), (x_right, y_up), X_WIDTH)
            pygame.draw.line(board_surface, GREY, (x_left, y_up), (x_right, y_down), X_WIDTH)

        elif game.o_won:

            result_message += "O's won. Congratulations!"

            # draw O
            pygame.draw.circle(board_surface, WHITE, (x, y), CIRCLE_RADIUS, CIRCLE_WIDTH)

        # result message

        result_message = large_font.render(result_message, False, color)
        result_message_rect = result_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + BOARD_WIDTH // 3))

        # ask to play again
        play_again_message = "Press [Space] to play again or [Esc] to quit"
        play_again_message = medium_font.render(play_again_message, False, BG_COLOR)
        play_again_rect = play_again_message.get_rect(center=(SCREEN_WIDTH // 2, 7 * SCREEN_HEIGHT // 8 + 55))

        screen.blit(board_surface, (BOARD_CENTER_X, BOARD_CENTER_Y))

        # print out message
        screen.blit(result_message, result_message_rect)
        screen.blit(play_again_message, play_again_rect)

    @staticmethod
    def display_upper_text(screen, game, players, small_font):
        message = ""
        if game.is_empty():
            message += "Begin or choose a player"
        elif not game.is_on or game.draw or game.x_won or game.o_won:
            message += "Game over"
        elif players[0].is_their_turn:
            message += "{0}'s turn".format(players[0].symbol)
        elif players[1].is_their_turn:
            message += "{0}'s turn".format(players[1].symbol)
        message = small_font.render(message, False, GREY)
        message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
        screen.blit(message, message_rect)

    @staticmethod
    def display_lower_text(screen, medium_font):
        escape_message = "Press any key to continue"
        escape_message = medium_font.render(escape_message, False, BG_COLOR)
        escape_rect = escape_message.get_rect(center=(SCREEN_WIDTH // 2, 7 * SCREEN_HEIGHT // 8 + 55))
        screen.blit(escape_message, escape_rect)

    @staticmethod
    def display_choice(screen, font):
        choice_message = "Play against AI (press [a]) or human (press [h])"
        choice_message = font.render(choice_message, False, GREY)
        choice_message_rect = choice_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(choice_message, choice_message_rect)


class Button:
    def __init__(self, pos, screen, font):
        # attributes
        self.width = SCREEN_WIDTH//4
        self.height = 50
        self.elevation = 5
        self.dynamic_elevation = 5
        self.original_y_pos = pos[1]
        self.screen = screen
        self.font = font

        # top rectangle
        self.top_rect = pygame.Rect((0, 0), (self.width, self.height))
        self.top_rect.center = pos
        self.top_color = BUTTON_COLOR

        # bottom rectangle
        self.bottom_rect = pygame.Rect((0, 0), (self.width, 5))
        self.bottom_rect.center = pos
        self.bottom_color = BG_COLOR

    def draw(self, game_state, player_state, text):
        # elevation logic
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        self.check_state(game_state, player_state)

        # text
        text_surf = self.font.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.top_rect.center)

        # display
        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
        self.screen.blit(text_surf, text_rect)

    def check_state(self, game_state, player_state):
        if game_state and player_state:
            self.dynamic_elevation = self.elevation
            self.top_color = BUTTON_COLOR
        else:
            self.dynamic_elevation = 0

