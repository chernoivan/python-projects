class Settings:

    def __init__(self):
        self.screen_width = 1100
        self.screen_height = 650
        self.bg_color = (230, 230, 230)

        self.ship_limit = 3

        self.fleet_drop_speed = 10

        self.score_scale = 1.5

        self.speed_scale = 1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 10.0
        self.bullet_speed = 5.0
        self.alien_speed = 2.0
        self.alien_points = 50

        # fleet_direction 1 means move to the right; -1 - to the left
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed += self.speed_scale
        self.bullet_speed += self.speed_scale
        self.alien_speed += self.speed_scale
        self.alien_points += int(self.score_scale * self.alien_points)
