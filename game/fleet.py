import pygame
import random
from obstacle import Enemy, Rock
from boss import Boss


class Fleet: 

    def __init__(self, sd_game):
        self.sd = sd_game
        self.aliens = sd_game.aliens
        self.settings = sd_game.settings
        self.rocks = pygame.sprite.Group()
        self.boss = None

        self.WAVE_SIZE = self.settings.wave_size
        self.SPAWN_INTERVAL = self.settings.spawn_interval
        self.remaining_spawns = 0
        self.last_spawn_time = 0

    def create_fleet(self):
        """Startet eine neue Welle."""
        self.aliens.empty()
        self.rocks.empty()
        self.boss = None
        
        level = self.sd.stats.level
        if level > 1 and level % self.settings.boss_spawn_n_levels == 0:
            self._spawn_boss()
        else:
            self.remaining_spawns = self.WAVE_SIZE
            self.last_spawn_time = pygame.time.get_ticks()

    def _spawn_boss(self):
        self.boss = Boss(self.sd)
        self.remaining_spawns = 0
    
    def _spawn_next(self):
        # spawns either rock or enemy
        if random.random() < 0.3:
            self.rocks.add(Rock(self.sd))
        else:
            self.aliens.add(Enemy(self.sd))
        self.remaining_spawns -= 1

    def _remove_offscreen(self):
        #removes offscreen objects
        for alien in self.aliens.copy():
            if alien.is_off_screen():
                self.aliens.remove(alien)
        for rock in self.rocks.copy():
            if rock.is_off_screen():
                self.rocks.remove(rock)

    def _wave_complete(self):
        return (self.remaining_spawns == 0 and
                len(self.aliens) == 0 and
                len(self.rocks) == 0 and
                self.boss is None)

    def _update_alien(self):
        now = pygame.time.get_ticks()

        if self.boss is not None:
            self.boss.update()
            self._check_boss_bullet_ship_collision()
            self._check_player_bullet_boss_collision()
            self._check_boss_ship_collision()
            if not self.boss.alive:
                self.sd.stats.score += 20 + self.sd.stats.level * 5
                self.sd.sb.prep_score()
                self.boss = None
                self._next_wave()
            return

        if self.remaining_spawns > 0 and (now - self.last_spawn_time) >= self.SPAWN_INTERVAL:
            self._spawn_next()
            self.last_spawn_time = now

        self.aliens.update()
        self.rocks.update()
        self._remove_offscreen()

        self._check_alien_ship_collision()
        self._check_rock_ship_collision()

        if self._wave_complete():
            self._next_wave()

    def _check_alien_ship_collision(self):
        if not self.sd.ship.invincible:
            if pygame.sprite.spritecollideany(self.sd.ship, self.aliens):
                self.sd._ship_hit()

    def _check_rock_ship_collision(self):
        if not self.sd.ship.invincible:
            if pygame.sprite.spritecollideany(self.sd.ship, self.rocks):
                self.sd._ship_hit()

    def _check_boss_ship_collision(self):
        if not self.sd.ship.invincible and self.boss:
            if self.sd.ship.rect.colliderect(self.boss.rect):
                self.sd._ship_hit()

    def _check_boss_bullet_ship_collision(self):
        if self.sd.ship.invincible or self.boss is None:
            return
        for bullet in self.boss.bullets.copy():
            if bullet.rect.colliderect(self.sd.ship.rect):
                self.sd._ship_hit()
                bullet.kill()
                break

    def _check_player_bullet_boss_collision(self):
        if self.boss is None:
            return
        for bullet in self.sd.bullet.copy():
            if bullet.rect.colliderect(self.boss.rect):
                self.boss.hit()
                self.sd.bullet.remove(bullet)

    def _next_wave(self):
        self.sd.bullet.empty()
        self.settings.increase_speed()
        self.sd.stats.level += 1
        self.sd.sb.prep_level()
        self.create_fleet()

    def draw_rocks(self, surface):
        #draws rocks 
        for rock in self.rocks.sprites():
            rock.draw(surface)

    def draw_boss(self, surface):
        if self.boss:
            self.boss.draw(surface)
