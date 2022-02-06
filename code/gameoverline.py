import pygame

class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("../assets/collisionline.png").convert_alpha()
        self.image.set_alpha(0)
        self.rect=self.image.get_rect()
        self.rect.center=[1280/2,575]