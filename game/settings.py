import pygame
from pathlib import Path

class Settings:

    def __init__(self):
        
        """makes music"""
        pygame.mixer.init()
        pygame.mixer.music.load(Path(__file__).parent/"sounds"/"music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        #screen settings
        self.screen_width = 1200
        self.screen_height = 600
        """pygame creates a Screen"""
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height)) 
        pygame.display.set_caption("Merci, Space Defender")
        #importing a bmp as background
        self.background = pygame.image.load(Path(__file__).parent/ "images" /"space.png").convert_alpha()
        #determine scale of of img as x, y cordinates
        bg_width, bg_height = self.background.get_size()
        #determine scale factor needed to stretch till top
        scale_factor = self.screen_height / bg_height
        #determine new width and height for appropriate scaling
        new_bg_width = int(bg_width * scale_factor)
        new_bg_height = self.screen_height
        self.background = pygame.transform.scale(self.background, (new_bg_width, new_bg_height))
        #center bmp
        self.background_rect = self.background.get_rect(centerx=self.screen.get_rect().centerx, top=0)
        self.bg_color = (0,0,0)
        #ship settings
        self.ship_speed = 5.5
        self.ship_limit = 3

        #bullet settings
        self.bullet_speed = 1
        self.bullet_width = 5 
        self.bullet_height = 20
        self.bullet_color = (150,20,20)
        self.bullet_allowed = 5
        
        # sound maker
        self.bullet_sound = pygame.mixer.Sound(Path(__file__).parent/"sounds"/"laser.mp3")
        self.bullet_volume = self.bullet_sound.set_volume(0.6)

        #Enemy/Alien setting
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.alien_size = 40

        #rock setting
        self.rock_size = 45

        #button settings
        self.button_color = (0,0,0)
        self.button_text_color = (255,255,255)

        self.wave_size = 10         
        # ms zwischen Spawns
        self.spawn_interval = 800   

        #scaling factor
        self.sdeedup_scale = 1.2
        
        #boss settings
        self.boss_spawn_n_levels = 3
        self.boss_width = 180
        self.boss_height = 80
        self.boss_base_hp = 20
        self.boss_canon_1 = -52
        self.boss_canon_2 = 52


        self.initilaize_dynamic_settings()

    def initilaize_dynamic_settings(self):
            #changing values
        self.ship_speed = 3
        self.bullet_speed = 4
        self.alien_speed = 0.9
        self.fleet_direction = 1
        self.alien_points = 1
            
    def increase_speed(self):
            #increases values
        self.ship_speed *= self.sdeedup_scale
        self.bullet_speed *= self.sdeedup_scale
        self.alien_speed *= self.sdeedup_scale
        self.fleet_direction *= self.sdeedup_scale