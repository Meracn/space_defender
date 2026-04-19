import pygame


class HUD:
    def __init__(self, sd_game):
        self.sd= sd_game
        self.settings = sd_game.settings
        self.screen = sd_game.screen
    
    def _draw_pause_screen(self):
        font = pygame.font.SysFont(None, 80)
        #pause text and postion
        text = font.render("PAUSED", True, (255, 255, 255))
        rect = text.get_rect(center=(self.screen.get_rect().centerx, self.screen.get_rect().centery - 150))
        #current score text and postion 
        hs_text = font.render("SCORE", False, (255,255,255))
        hs_rect = hs_text.get_rect(center=(self.screen.get_rect().centerx, self.screen.get_rect().centery ))
        #dynamic score value and postion
        score_str = str(self.sd.stats.score)
        current_score = font.render(score_str, True, (255, 0, 255))
        score_rect = current_score.get_rect(center=(self.screen.get_rect().centerx, self.screen.get_rect().centery + 100))
        #drawing pause menu on screen
        self.screen.blit(text, rect)
        self.screen.blit(hs_text, hs_rect)
        self.screen.blit(current_score, score_rect)

    def _draw_highscore_screen(self):
        font_big = pygame.font.SysFont(None, 80)
        font_mid = pygame.font.SysFont(None, 56)
        font_sm  = pygame.font.SysFont(None, 44)
        cx = self.screen.get_rect().centerx
        cy = self.screen.get_rect().centery

        # Highscore titel
        title = font_big.render("HIGHSCORE", True, (0, 0, 0))
        outline_title = font_big.render("HIGHSCORE", True, (255, 255, 255))  
        center_title = title.get_rect(center=(cx, cy - 140))
        #titel highlight
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            self.screen.blit(outline_title, center_title.move(dx, dy))
        self.screen.blit(title, title.get_rect(center=(cx, cy - 140)))
        #the highscore itself
        score = font_big.render(str(self.sd.sb.highscore), True, (80, 0, 80))
        outline_score = font_big.render(str(self.sd.sb.highscore), True, (255, 255, 255))  
        center_score = score.get_rect(center=(cx, cy - 60))
        #score highlight
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            self.screen.blit(outline_score, center_score.move(dx, dy))
        self.screen.blit(score, score.get_rect(center=(cx, cy - 60)))

        # Höchstes Level
        lvl_title = font_mid.render("BESTES LEVEL", True, (0, 0, 0))
        outline_lvl_title = font_mid.render("BESTES LEVEL", True, (255, 255, 255))  
        center_lvl_title = lvl_title.get_rect(center=(cx, cy + 50))
        #lvl highlight
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            self.screen.blit(outline_lvl_title, center_lvl_title.move(dx, dy))
        self.screen.blit(lvl_title, lvl_title.get_rect(center=(cx, cy + 50)))

        lvl_val = font_big.render(str(self.sd.sb.best_level), True, (80, 0, 80))
        outline_lvl_val = font_big.render(str(self.sd.sb.best_level), True, (255, 255, 255))  
        center_lvl_val = outline_lvl_val.get_rect(center=(cx, cy + 130))
        #titel highlight
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            self.screen.blit(outline_lvl_val, center_lvl_val.move(dx, dy))
        self.screen.blit(lvl_val, lvl_val.get_rect(center=(cx, cy + 130)))

        hint = font_sm.render("ESC zum Schließen", True, (255, 255, 255))
        outline_hint = font_sm.render("ESC zum Schließen", True, (0, 0, 0))  
        center_hint = outline_hint.get_rect(center=(cx, cy + 210))
        #titel highlight
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            self.screen.blit(outline_hint, center_hint.move(dx, dy))
        self.screen.blit(hint, hint.get_rect(center=(cx, cy + 210)))