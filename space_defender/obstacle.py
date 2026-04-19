import pygame
import random
from pygame.sprite import Sprite


class Enemy(Sprite):
    """alien can be shot"""

    def __init__(self, sd_game):
        super().__init__()
        self.screen = sd_game.screen
        self.screen_rect = sd_game.screen.get_rect()
        self.settings = sd_game.settings

        self.image = pygame.Surface((self.settings.alien_size, self.settings.alien_size), pygame.SRCALPHA)
        self._draw_alien()
        self.rect = self.image.get_rect()

        # Blink-Timer — jeder Alien startet mit zufälligem Offset damit sie nicht synchron blinken
        self.blink_offset = random.randint(0, 600)
        self.blink_interval = 400  # ms

        self._set_spawn()


    def _draw_alien(self):
        s = self.settings.alien_size
        cx, cy = s // 2, s // 2
        # Raute
        pygame.draw.polygon(self.image, (0, 200, 255), [(cx, 0), (s, cy), (cx, s), (0, cy)])
        pygame.draw.polygon(self.image, (100, 230, 255), [(cx, 0), (s, cy), (cx, s), (0, cy)], 2)
        # Innere Raute
        pygame.draw.polygon(self.image, (0, 100, 180), [(cx, 8), (s-8, cy), (cx, s-8), (8, cy)])
        # Kern
        pygame.draw.circle(self.image, (180, 240, 255), (cx, cy), 4)
   
    def _set_spawn(self):
        """random spawn point, either top,left or right"""
        speed = self.settings.alien_speed
        bg = self.settings.background_rect
        side = random.choice(['top', 'left', 'right'])

        if side == 'top':
            self.rect.x = random.randint(bg.left, bg.right - self.rect.width)
            self.rect.y = bg.top - self.rect.height
            self.vx = random.uniform(-speed, speed)
            self.vy = speed

        elif side == 'left':
            self.rect.x = bg.left - self.rect.width
            self.rect.y = random.randint(bg.top, bg.centery)
            self.vx = speed
            self.vy = random.uniform(0.3 * speed, speed)

        else:  # right
            self.rect.x = bg.right
            self.rect.y = random.randint(bg.top, bg.centery)
            self.vx = -speed
            self.vy = random.uniform(0.3 * speed, speed)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

            # Blink: helle innere Raute ein/ausblenden
        now = (pygame.time.get_ticks() + self.blink_offset) // self.blink_interval
        blink_on = now % 2 == 0
        self.image.fill((0, 0, 0, 0))  # Surface leeren
        s = self.settings.alien_size
        cx, cy = s // 2, s // 2
        pygame.draw.polygon(self.image, (0, 200, 255), [(cx, 0), (s, cy), (cx, s), (0, cy)])
        pygame.draw.polygon(self.image, (100, 230, 255), [(cx, 0), (s, cy), (cx, s), (0, cy)], 2)
        if blink_on:
            pygame.draw.polygon(self.image, (0, 100, 180), [(cx, 8), (s-8, cy), (cx, s-8), (8, cy)])
            pygame.draw.circle(self.image, (180, 240, 255), (cx, cy), 4)
        else:
            pygame.draw.polygon(self.image, (0, 160, 220), [(cx, 8), (s-8, cy), (cx, s-8), (8, cy)])
            pygame.draw.circle(self.image, (255, 255, 255), (cx, cy), 4)

    def is_off_screen(self):
        bg = self.settings.background_rect
        margin = 20  # px außerhalb des Randes bevor gelöscht wird
        return (self.rect.top > bg.bottom + margin or
            self.rect.right < bg.left - margin or
            self.rect.left > bg.right + margin)


class Rock(Sprite):
    """stone cant be shoot must be avoided"""

    def __init__(self, sd_game):
        super().__init__()
        self.screen = sd_game.screen
        self.settings = sd_game.settings

        # Stein als graues Polygon zeichnen (kein eigenes Bild nötig)
        self.image = pygame.Surface((self.settings.rock_size, self.settings.rock_size), pygame.SRCALPHA)
        self._draw_rock()
        self.rect = self.image.get_rect()

        self._set_spawn()

    def _draw_rock(self):
        """Zeichnet einen unregelmäßigen Stein-Polygon."""
        # zieht eine linie von punkt n zu m bis zurück zu n
        points = [
           (8, 2), (30, 0), (44, 10),
            (44, 32), (36, 44), (14, 44),
            (0, 30), (2, 12)
        ]
        pygame.draw.polygon(self.image, (140, 130, 120), points)
        pygame.draw.polygon(self.image, (90, 80, 75), points, 2)
        # kleiner heller streifen um dem Stein tiefe zu geben
        pygame.draw.line(self.image, (200, 190, 185), (10, 6), (28, 4), 2)

    def _set_spawn(self):
        speed = max(self.settings.alien_speed * 1.3, 2.0)
        bg = self.settings.background_rect
        side = random.choice(['top', 'left', 'right'])

        if side == 'top':
            self.rect.x = random.randint(bg.left, bg.right - self.rect.width)
            self.rect.y = bg.top - self.rect.height
            self.vx = random.uniform(-speed * 0.6, speed * 0.6)
            self.vy = speed

        elif side == 'left':
            self.rect.x = bg.left - self.rect.width
            self.rect.y = random.randint(bg.top, bg.centery)
            self.vx = speed
            self.vy = random.uniform(0.5 * speed, speed)

        else:
            self.rect.x = bg.right
            self.rect.y = random.randint(bg.top, bg.centery)
            self.vx = -speed
            self.vy = random.uniform(0.5 * speed, speed)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.angle = 0.0
        self.rotation_speed = random.uniform(-2.5, 2.5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Rotation
        self.angle = (self.angle + self.rotation_speed) % 360
        rotated = pygame.transform.rotate(self.image, self.angle)
        old_center = self.rect.center
        self.rect = rotated.get_rect(center=old_center)
        self._rotated_image = rotated
        
    def draw(self, surface):
        if hasattr(self, '_rotated_image'):
            surface.blit(self._rotated_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

    def is_off_screen(self):
        bg = self.settings.background_rect
        margin = 30  # px außerhalb des Randes bevor gelöscht wird
        return (self.rect.top > bg.bottom + margin or
            self.rect.right < bg.left - margin or
            self.rect.left > bg.right + margin)
   