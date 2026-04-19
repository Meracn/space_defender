import pygame 
from bullets import Bullet

class Ammunition:
    def __init__(self, sd_game):
        self.sd= sd_game
        self.settings = sd_game.settings
        self.bullet = sd_game.bullet  

    def fire_bullet(self):
        if len(self.bullet) < self.settings.bullet_allowed:
            new_bullet = Bullet(self.sd)
            self.bullet.add(new_bullet)

    def _update_bullet(self):
        self.bullet.update()
        """deletes bullets"""
        for bullets in self.bullet.copy():
            if bullets.rect.bottom <= 0:
                self.bullet.remove(bullets)
        self._bullet_alien_collsion()

    def _bullet_alien_collsion(self):
        collisions = pygame.sprite.groupcollide(self.sd.bullet, self.sd.aliens, False, True)
        #counting points
        if collisions:
            self.sd.stats.score += self.settings.alien_points
            self.sd.sb.prep_score()
        #updating points to highscore board
        if self.sd.stats.score > self.sd.sb.highscore:
            self.sd.sb.highscore = self.sd.stats.score
            self.sd.sb.save_highscore()
        # Bullets prallen an Steinen ab (Stein bleibt, Bullet verschwindet)
        pygame.sprite.groupcollide(self.sd.bullet, self.sd.fleet.rocks, True, False)
