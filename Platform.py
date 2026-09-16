class Platform:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def scroll(self, amount):
        self.rect.y -= amount

    def draw(self, surface):
        surface.blit(self.image, self.rect)
