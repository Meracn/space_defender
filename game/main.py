import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from fleet import Fleet
from ammunition import Ammunition
from scoreboard import Scoreboard
from menu import Menu
from key_events import KeyEvents
from hud import HUD
from game_state import GameStats

class SpaceDefender:

    def __init__(self):
        #starts the background enviorment for pygame actions
        pygame.init()
        #creates clock to control time or framerate        
        self.clock = pygame.time.Clock()
        #imports the Settings class value as self.settings
        self.settings = Settings()
        # gamestate
        self.stats = GameStats(self)
        #pygame creates a Screen
        self.screen = self.settings.screen
        self.bg_color = (self.settings.bg_color)
        #creates a ship from the Ship class and calls this instance of Ship self.ship
        self.ship = Ship(self)
        #is a pygame function that gives the instances of the Bullet class the atributes of a sprite in pygame
        #through this i can check the instances on things like collision or speed etc"""
        self.bullet = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        # variable for fleet
        self.fleet = Fleet(self)
        self.fleet.create_fleet()
        # Munutions klasse
        self.ammo = Ammunition(self)
        # Key events klasse
        self.key_events = KeyEvents(self)
        # HUD klasse
        self.hud = HUD(self)
        #Scoreboard
        self.sb = Scoreboard(self)
        #game flag
        self.game_active = False
        #pause Flag
        self.paused = False
        #menu flag/ positioning
        self.menu = Menu(self)
        #highscore flag
        self.show_highscore = False
        
    def run_game(self):
        """main loop for game"""
        while True:
            #keyboard and mouse inputs are events, which are moved in their own function fpr better understanding
            self._check_events()
            #fills the background with the bg_color from __init__, also moved to its own function for better understanding
            self._update_screen()
            #controlls the frame rate
            self.clock.tick(60)
            #display the latest image
            pygame.display.flip()
            #dependend on life of ships
            if self.game_active and not self.paused:
                #imports the newest movement to screen
                self.ship.update()
                #displays deletes and limits the bullets
                self.ammo._update_bullet()
                #displays the alien groups
                self.fleet._update_alien()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # mouse control
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked = self.menu.handle_click(mouse_pos)
                if clicked == "PLAY":
                    self.start_a_game()
                elif clicked == "AUDIO":
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif clicked == "HIGHSCORE":
                    self.show_highscore = True
            
            #ESC for entering menu and giving up run and exiting hihscore menu
            if event.type == pygame.KEYDOWN:
                if self.show_highscore:
                    self.show_highscore = False
                elif event.key == pygame.K_ESCAPE:
                    self.stats.reset_stats()
                    self.sb.prep_score()
                    self.sb.prep_level()
                    self.bullet.empty()
                    self.aliens.empty()
                    self.fleet.rocks.empty()
                    self.fleet.boss = None
                    self.ship.center_ship()
                    self.ship.invincible = False
                    self.ship._blink_visible = True
                    self.game_active = False
                    pygame.mouse.set_visible(True)

            #movement and other inputs
            if event.type == pygame.KEYDOWN:
                self.key_events._check_keydown_events(event)

            if event.type == pygame.KEYUP:
                self.key_events._check_keyup_events(event)


    def _update_screen(self):
        """updates images on screen and flips to the new screen"""
        self.screen.fill(self.bg_color)
        self.screen.blit(self.settings.background,self.settings.background_rect)
        for bullets in self.bullet.sprites():
            bullets.draw_bullet()
        self.ship.blitme()
        

        self.aliens.draw(self.screen)
        self.fleet.draw_rocks(self.screen)
        self.fleet.draw_boss(self.screen)
        if self.show_highscore:
            self.screen.blit(self.sb.hs_background, self.sb.hs_background_rect)
            self.hud._draw_highscore_screen()
        elif not self.game_active:
            self.menu.draw()
        elif self.paused:
            self.hud._draw_pause_screen()
        elif self.game_active:
            self.sb.show_score()
            self.sb.show_lives()

    def _ship_hit(self):
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.ship.start_invincibility()
        else:
            self.stats.ships_left = 0
            self.game_active = False
            pygame.mouse.set_visible(True)
            # Höchstes Level speichern
            self.sb.update_best_level(self.stats.level)
            
    def start_a_game(self):
        pygame.mouse.set_visible(False)
        #reset the game stat
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.bullet.empty()
        self.aliens.empty()
        self.fleet.rocks.empty()
        #make new objects and recenter ship
        self.fleet.create_fleet()
        self.ship.center_ship()
        self.ship.invincible = False
        self.ship._blink_visible = True
        self.game_active = True


if __name__ == '__main__':
    """runs the game"""
    sd = SpaceDefender()
    sd.run_game()
