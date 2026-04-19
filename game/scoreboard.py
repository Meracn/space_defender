import pygame.font
import pygame
import json
from pathlib import Path

class Scoreboard:

    def __init__(self, sd_game):
        self.sd = sd_game
        self.stats = sd_game.stats
        self.screen = sd_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sd_game.settings
        self.data = self.load_data()
        self.ship_img = pygame.transform.scale(sd_game.ship.image, (40, 40))
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)
        self.highscore = self.data.get("highscore", 0)
        self.best_level = self.data.get("best_level", 1)
        self.prep_score()
        self.prep_level()
        self.show_lives()
        #pause bg settings
        self.background = pygame.image.load(Path(__file__).parent/ "images" / "background.png").convert_alpha()
        bg_width, bg_height = self.background.get_size()
        scale_factor = self.settings.screen_height / bg_height
        new_bg_width = int((bg_width * scale_factor) +200)
        new_bg_height = self.settings.screen_height
        self.hs_background = pygame.transform.scale(self.background,(new_bg_width, new_bg_height))
        self.hs_background_rect = self.hs_background.get_rect(centerx=self.screen.get_rect().centerx, top=0)
        
    def prep_score(self):
        #turns numbers into image objects
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, (0,0,0))

        #display the score at the top right
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        #score txt
        self.score_txt = self.font.render("Score:", True, self.text_color, (0,0,0))
        self.score_txt_rect = self.score_txt.get_rect()
        self.score_txt_rect.right = self.score_rect.left - 10  # links neben dem Score
        self.score_txt_rect.top = 20

    def show_score(self):
        #displays objects
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.score_txt, self.score_txt_rect)
        self.screen.blit(self.level_txt, self.level_txt_rect)

    def load_data(self):
        try:
            with open("highscore.json", "r") as f:
                return json.load(f)
        except:
            return {}
        
    def save_data(self):
        with open("highscore.json", "w") as f:
            json.dump({"highscore": self.highscore, "best_level": self.best_level}, f)

    def load_highscore(self):
        try:
            with open("highscore.json", "r") as f:
                data = json.load(f)
                return data["highscore"]
        except:
            return 0
        
    def save_highscore(self):
        with open("highscore.json", "w") as f:
            json.dump({"highscore": self.highscore}, f)

    def show_lives(self):
        #draw ships on screen top left
        for i in range(self.stats.ships_left):
            x = 10 + i * 50   
            y = 10
            self.screen.blit(self.ship_img, (x, y))

    def update_best_level(self, level):
        if level > self.best_level:
            self.best_level = level
            self.save_data()
    
    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color,self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

        self.level_txt = self.font.render("Level:", True, self.text_color, (0,0,0))
        self.level_txt_rect = self.level_txt.get_rect()
        self.level_txt_rect.right = self.level_rect.left - 10  # links neben dem Score
        self.level_txt_rect.top = self.score_rect.bottom + 10
    
   
