import sys
import pygame

class KeyEvents:
    def __init__(self, sd_game):
        self.sd= sd_game
        self.settings = sd_game.settings
        self.ship = sd_game.ship
        self.ammo = sd_game.ammo

    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        if event.key == pygame.K_SPACE:
            self.ammo.fire_bullet()
        #close the game through "q"
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
        #pause with ESC
        if event.key == pygame.K_ESCAPE:
            if self.sd.show_highscore:
                self.sd.show_highscore = False
            elif self.sd.game_active:
                self.sd.paused = not self.sd.paused

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False