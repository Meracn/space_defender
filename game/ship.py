import pygame


class Ship:
    def __init__(self, sd_game):
        self.screen = sd_game.screen
        self.screen_rect = sd_game.screen.get_rect()
        self.settings = sd_game.settings

        self.image = pygame.Surface((70, 50), pygame.SRCALPHA)
        self._draw_ship()
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.invincible = False
        self.invincible_start = 0
        self.invincible_duration = 2000
        self._blink_visible = True

    def _draw_ship(self):
        w, h = 70, 40
        cx = w // 2

        # Dreieck, körper vom Schiff
        pygame.draw.polygon(self.image, (192, 192, 192), [(cx, 0), (0, h), (w, h)])
        pygame.draw.polygon(self.image, (0, 0, 0), [(cx, 0), (0, h), (w, h)], 2)

        # Cockpit
        pygame.draw.ellipse(self.image, (0, 180, 220), (cx - 6, 8, 12, 10))
        pygame.draw.ellipse(self.image, (100, 220, 255), (cx - 3, 7, 6, 6))
        # Antrieb 
        for ex in [w // 4, 3 * w // 4]:
            pygame.draw.ellipse(self.image, (255, 140, 0), (ex - 8, h - 5, 16, 10))
            pygame.draw.ellipse(self.image, (255, 220, 80), (ex - 4, h - 3, 8, 6))


    def start_invincibility(self):
        self.invincible = True
        self.invincible_start = pygame.time.get_ticks()
        self._blink_visible = True

    def update(self):
        now = pygame.time.get_ticks()
        if self.invincible:
            elapsed = now - self.invincible_start
            if elapsed >= self.invincible_duration:
                self.invincible = False
                self._blink_visible = True
            else:
                self._blink_visible = (elapsed // 150) % 2 == 0

        if self.moving_right and self.rect.right < self.settings.background_rect.right + 30:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.settings.background_rect.left - 30:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > self.settings.background_rect.top + 100:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.settings.background_rect.bottom:
            self.y += self.settings.ship_speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def blitme(self):
        if self._blink_visible:
            self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
