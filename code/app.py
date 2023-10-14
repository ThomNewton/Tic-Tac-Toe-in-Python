import pygame
import sys
from settings import *
from player import Player
from game import Game, GameState
from gui import Button


class App:

    def __init__(self):
        # pygame setup
        pygame.init()
        self.icon = pygame.image.load('../graphics/tic_tac_toe_icon.png')
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption('Tic-Tac-Toe')
        self.clock = pygame.time.Clock()

        # display setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.Surface((BG_WIDTH, BG_HEIGHT))
        self.board_surface = pygame.Surface([BOARD_WIDTH, BOARD_HEIGHT])

        # font setup
        self.large_font = pygame.font.Font('../font/pixel_type.ttf', 70)
        self.medium_font = pygame.font.Font('../font/pixel_type.ttf', 45)
        self.small_font = pygame.font.Font('../font/pixel_type.ttf', 30)

        # players setup
        self.players = [Player('X'), Player('O')]

        # buttons setup
        self.x_button = Button((0.25 * SCREEN_WIDTH, SCREEN_HEIGHT//25), self.screen, self.medium_font)
        self.o_button = Button((0.75 * SCREEN_WIDTH, SCREEN_HEIGHT//25), self.screen, self.medium_font)
        self.buttons = [self.x_button, self.o_button]

        # game setup
        self.game = Game()

        # time
        self.has_countdown_begun = False
        self.time_0 = self.time_1 = 0

    def run(self):
        while True:

            GameState.static_elements(self.screen,
                                      self.background,
                                      self.game,
                                      self.players,
                                      self.buttons,
                                      self.small_font)

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            game_has_not_yet_began = not self.game.is_on and self.game.is_empty()
            game_is_on = self.game.is_on
            game_is_over = not self.game.is_on and not self.game.is_empty()

            if game_has_not_yet_began:
                GameState.stage_1(self.screen,
                                  self.game,
                                  self.players,
                                  self.medium_font,
                                  events)

            elif game_is_on:
                c = GameState.stage_2(self.screen,
                                      self.board_surface,
                                      self.game,
                                      self.players,
                                      self.medium_font,
                                      events,
                                      self.has_countdown_begun,
                                      self.time_0,
                                      self.time_1)
                
                self.has_countdown_begun, self.time_0, self.time_1 = c

            elif game_is_over:
                GameState.stage_3(self.screen,
                                  self.board_surface,
                                  self.game,
                                  self.players,
                                  self.medium_font,
                                  self.large_font,
                                  events)

            pygame.display.update()
            self.clock.tick(60)

