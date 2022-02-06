import pygame,random

class Balloon(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image1=pygame.image.load("../assets/greenballoon.png").convert_alpha()
        self.image2=pygame.image.load("../assets/redballoon.png").convert_alpha()
        self.image3=pygame.image.load("../assets/yellowballoon.png").convert_alpha()
        self.imagelist=[self.image1,self.image2,self.image3]
        self.image=random.choice(self.imagelist)
        self.rect=self.image.get_rect()
        self.rect.center=[random.randrange(100,1180),-150]
    def update(self):
        if(self.rect.centery>=520):
            self.kill()
        else:
            self.rect.centery+=random.randint(1,6)
    def checkcollide(self,spriteGroup):
        if pygame.sprite.spritecollide(self,spriteGroup,False):
            self.kill()
            return True
        else: 
            return False