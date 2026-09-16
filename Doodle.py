import pygame

class Player:
    def __init__(self, x, y, image_right, image_left):
        self.image_right = image_right
        self.image_left = image_left
        self.image = image_right
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.y_velocity = 0

    def move(self, keys, move_speed, screen_width):
        if keys[pygame.K_LEFT]:
            self.rect.x -= move_speed
            self.image = self.image_left
        if keys[pygame.K_RIGHT]:
            self.rect.x += move_speed
            self.image = self.image_right

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