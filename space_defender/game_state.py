class GameStats:
    def __init__(self, game):
        self.settings = game.settings
        self.reset_stats()
        self.level = 1 

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1