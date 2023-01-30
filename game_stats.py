class GameStats:
    """Track statistics for Pynvaders"""
    def __init__(self, pynvaders_game):
        """Initialize statistics."""
        self.settings = pynvaders_game.settings
        self.reset_stats()
        # Start Pynvaders in an active state
        self.game_active = True

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
