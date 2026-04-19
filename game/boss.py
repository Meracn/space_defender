import pygame
from pygame.sprite import Sprite


class BossBullet(Sprite):
    """Boss projektile """

    def __init__(self, x, y, target_x, target_y, speed, screen, settings):
        super().__init__()
        self.screen = screen
        self.settings = settings
        size = 10
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 80, 0), (size // 2, size // 2), size // 2)
        pygame.draw.circle(self.image, (255, 200, 0), (size // 2, size // 2), size // 4)
        self.rect = self.image.get_rect(center=(x, y))

        # calculate ship position to target
        dx = target_x - x
        dy = target_y - y
        dist = max((dx**2 + dy**2) ** 0.5, 1)
        self.vx = speed * dx / dist
        self.vy = speed * dy / dist
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def is_off_screen(self):
        bg = self.settings.background_rect
        return (self.rect.top > bg.bottom or self.rect.right < bg.left or
                self.rect.left > bg.right or self.rect.bottom < bg.top)


class Boss(Sprite):

    def __init__(self, sd_game):
        super().__init__()
        self.sd = sd_game
        self.settings = sd_game.settings
        self.screen = sd_game.screen
        bg = self.settings.background_rect

        self.hp = self.settings.boss_base_hp + sd_game.stats.level * 5
        self.max_hp = self.hp

        # Boss draw func call
        self.image = pygame.Surface((self.settings.boss_width, self.settings.boss_height), pygame.SRCALPHA)
        self._draw_boss()
        self.rect = self.image.get_rect()
        self.rect.centerx = bg.centerx
        self.rect.y = bg.top - self.settings.boss_height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # comes down from top variables
        self.target_y = bg.top + 80
        self.descending = True
        self.move_speed = 1.5
        self.direction = 1  # horizontal

        # shooting variables
        self.bullets = pygame.sprite.Group()
        self.shoot_interval = 1200  # ms
        self.last_shot = pygame.time.get_ticks()

        self.alive = True

    def _draw_boss(self):
        w, h = self.settings.boss_width, self.settings.boss_height
        # Rumpf
        pygame.draw.ellipse(self.image, (192, 192, 192), (10, 10, w - 20, h - 20))
        # Rand
        pygame.draw.ellipse(self.image, (205, 133, 63), (10, 10, w - 20, h - 20), 3)
        # Cockpit
        pygame.draw.ellipse(self.image, (0, 200, 255), (w // 2 - 20, h // 2 - 12, 40, 24))
        # Waffenkanonen links/rechts
        pygame.draw.circle(self.image, (173, 216, 230), (15, h - 12), 10)
        pygame.draw.circle(self.image, (173, 216, 230), (w - 15, h - 12), 10)

    def update(self):
        bg = self.settings.background_rect
        now = pygame.time.get_ticks()
        # y axis movement/coming down from top
        if self.descending:
            self.y += self.move_speed
            if self.y >= self.target_y:
                self.y = self.target_y
                self.descending = False
        else:
            # x axis movement
            self.x += self.move_speed * self.direction
            if self.rect.right >= bg.right - 10:
                self.direction = -1
            elif self.rect.left <= bg.left + 10:
                self.direction = 1

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # shooting call
        if not self.descending and (now - self.last_shot) >= self.shoot_interval:
            self._shoot()
            self.last_shot = now

        self.bullets.update()
        for b in self.bullets.copy():
            if b.is_off_screen():
                self.bullets.remove(b)

    def _shoot(self):
        ship = self.sd.ship
        # shots from canons, canons are at boss width divided by two and either adding or subtracting  15 from 
        for offset_x in [-self.settings.boss_width // 2 + 15, self.settings.boss_width // 2 - 15]:
            bx = self.rect.centerx + offset_x
            by = self.rect.bottom
            bullet = BossBullet(bx, by, ship.rect.centerx, ship.rect.centery,
                                 speed=4, screen=self.screen, settings=self.settings)
            self.bullets.add(bullet)

    def hit(self, damage=1):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def draw(self, surface):
        # Boss selbst
        surface.blit(self.image, self.rect)
        # Bullets
        for b in self.bullets.sprites():
            surface.blit(b.image, b.rect)
        # HP-Balken
        self._draw_hp_bar(surface)

    def _draw_hp_bar(self, surface):
        bar_w = self.settings.boss_width
        bar_h = 8
        bg = self.settings.background_rect
        bx = bg.centerx - bar_w // 2   
        by = bg.top + 8                       
        ratio = max(self.hp / self.max_hp, 0)
        # Hintergrund
        pygame.draw.rect(surface, (60, 0, 0), (bx, by, bar_w, bar_h))
        # HP
        pygame.draw.rect(surface, (220, 0, 0), (bx, by, int(bar_w * ratio), bar_h))
        # Rahmen
        pygame.draw.rect(surface, (255, 100, 100), (bx, by, bar_w, bar_h), 1)
