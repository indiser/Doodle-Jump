import pygame

class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.y_velocity = 0

    def move(self, keys, move_speed, screen_width):
        if keys[pygame.K_LEFT]:
            self.rect.x -= move_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += move_speed

        # Screen Wrap
        if self.rect.right < 0:
            self.rect.left = screen_width
        elif self.rect.left > screen_width:
            self.rect.right = 0

    def apply_gravity(self, gravity):
        self.y_velocity += gravity
        self.rect.y += self.y_velocity

    def jump(self, strength, boost_multiplier=1.0):
        self.y_velocity = strength * boost_multiplier

    def draw(self, surface):
        surface.blit(self.image, self.rect)