import pygame
from pathlib import Path


class Menu:

    def __init__(self, sd_game):
        self.screen = sd_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sd_game.settings
        self.font = pygame.font.SysFont(None, 52)
        self.font_title = pygame.font.SysFont(None, 90)
        self.game = sd_game
        self.image = pygame.image.load(Path(__file__).parent / "images" / "menu_screen.png").convert_alpha()
        cx = self.screen_rect.centerx
        cy = self.screen_rect.centery
        self.buttons = {
            "PLAY":      pygame.Rect(0, 0, 220, 55),
            "AUDIO":     pygame.Rect(0, 0, 220, 55),
            "HIGHSCORE": pygame.Rect(0, 0, 220, 55),
        }
        for i, rect in enumerate(self.buttons.values()):
            rect.centerx = cx
            rect.centery = cy - 60 + i * 80

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        #background
        self.image = pygame.transform.scale(self.image, (1200, 600))
        self.screen.blit(self.image)
        #Title position
        title = self.font_title.render("SPACE DEFENDER", True, (105, 105, 105))
        outline_title = self.font_title.render("SPACE DEFENDER", True, (0, 0, 0))  
        center_title = title.get_rect(centerx=self.screen_rect.centerx, top=80)
        #titel highlight
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            self.screen.blit(outline_title, center_title.move(dx, dy +3))
        title_visible = (pygame.time.get_ticks() // 500) % 2 == 0
        if title_visible:
            self.screen.blit(title, center_title)
     
        for label, rect in self.buttons.items():
            color = (210, 210, 210) if rect.collidepoint(mouse_pos) else self.settings.button_color
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=8)
            txt = self.font.render(label, True, self.settings.button_text_color)
            outline = self.font.render(label, True, (0, 0, 0))  # Randfarbe
            center = txt.get_rect(center=rect.center)
            adjusted_center = center[0], center[1] +5
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                self.screen.blit(outline, center.move(dx, dy +8))
            self.screen.blit(txt, adjusted_center)

    def handle_click(self, mouse_pos):
        """Gibt den Namen des geklickten Buttons zurück, oder None."""
        for label, rect in self.buttons.items():
            if rect.collidepoint(mouse_pos):
                return label
        return None