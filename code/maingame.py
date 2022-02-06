import pygame,sys
import pygame.camera
import pygame.image
from pygame.locals import *
import balloon
from handtracking import HandTracking
import cv2
import numpy
import gameoverline
from pin import Pin
# import mediapipe

# #subclasses
# drawingModule = mediapipe.solutions.drawing_utils  #for drawing over image
# handsModule = mediapipe.solutions.hands   #for accessing the hand class that we need

# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

pygame.init()
# pygame.camera.init()
pygame.mixer.pre_init()
pygame.mixer.init()
clock=pygame.time.Clock()
# cameras=pygame.camera.list_cameras()
# webcam = pygame.camera.Camera(cameras[0],(640,480))
# webcam.start()

#game variables
WIDTH = 1280
HEIGHT = 720
time=2000
score=0
quit = False
gameover = False
font=pygame.font.Font('freesansbold.ttf',35)
scorex=572
scorey=615

#initialize screen
pygame.display.set_caption("Balloon Burst")
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.time.set_timer(pygame.USEREVENT, time)
pygame.mouse.set_visible(False)

# music
pygame.mixer.music.load("../assets/bgmusic.mp3")
pygame.mixer.music.play(loops=-1)

#images
bgimg=pygame.image.load("../assets/gamebg.png").convert_alpha()
bgdownimg=pygame.image.load("../assets/gamebgdownpart.png").convert_alpha()

#objects
handtrackingobjmain = HandTracking()
balloon_group=pygame.sprite.Group()
gameoverobject=gameoverline.GameOver()
pin=Pin()
pin_group=pygame.sprite.Group()
pin_group.add(pin)
gameoverrectanglegrp=pygame.sprite.Group()
gameoverrectanglegrp.add(gameoverobject)

def cv2ImageToSurface(cv2Image):
    # if cv2Image.dtype.name == 'uint16':
    #     cv2Image = (cv2Image / 256).astype('uint8')
    size = cv2Image.shape[1::-1]
    if len(cv2Image.shape) == 2:
        cv2Image = numpy.repeat(cv2Image.reshape(size[1], size[0], 1), 3, axis = 2)
        format = 'RGB'
    else:
        format = 'RGBA' if cv2Image.shape[2] == 4 else 'RGB'
        format = 'RGB'
        cv2Image[:, :, [0, 2]] = cv2Image[:, :, [2, 0]]
    surface = pygame.image.frombuffer(cv2Image.flatten(), size, format)
    return surface.convert_alpha() if format == 'RGBA' else surface.convert()


#game loop
while not quit:

    if(gameover):
        # pygame.mixer.Channel(1).play(pygame.mixer.Sound('../assets/gameover.wav'), maxtime=600)
        for sprite in balloon_group:
            sprite.remove()
        SCREEN.fill((255,255,255))
        gameovertext=font.render("Game Over! Score : "+str(score),True,(255,0,0))
        SCREEN.blit(gameovertext,(1280/2-200,720/2-30))
        pygame.mouse.set_visible(True)

    else:
        # img = webcam.get_image()
        SCREEN.fill((255,255,255))
        SCREEN.blit(bgimg,(0,0))
        # npimage=numpy.asarray(pin.frame)
        SCREEN.blit(pin.getCamFrame(),(0,0))
        SCREEN.blit(bgdownimg,(0,0))
        # cv2ImageToSurface(pin.frame)
        # SCREEN.blit(pin.frame,(0,0))
        balloon_group.draw(SCREEN)
        gameoverrectanglegrp.draw(SCREEN)
        scoretext=font.render("Score : "+str(score),True,(0,0,0))
        SCREEN.blit(scoretext,(scorex,scorey))
        pin_group.draw(SCREEN)
        pin_group.update()
        if pygame.sprite.groupcollide(balloon_group,gameoverrectanglegrp,0,0):
            gameover=True
        balloon_group.update()
        print(pin.handclosed)
        if(pin.handclosed):
            # print("in if")
            for sprite in balloon_group.sprites():
                # print("in for")
                if(sprite.checkcollide(pin_group)):
                    # print("checking collide")
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('../assets/ballonblast.wav'), maxtime=600)
                    score+=1


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit=True
        elif event.type == pygame.MOUSEBUTTONUP:
            if(gameover==False):
                for sprite in balloon_group.sprites():
                    if(sprite.checkcollide(pin_group)):
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('../assets/ballonblast.wav'), maxtime=600)
                        score+=1
                        # print(score)                
        elif event.type==pygame.USEREVENT:
            if(gameover==False):
                balloon1=balloon.Balloon()
                balloon_group.add(balloon1)    
                if(time>500):
                    time-=100
                    pygame.time.set_timer(pygame.USEREVENT, time)
                else:
                    pygame.time.set_timer(pygame.USEREVENT, time)



    pygame.display.update()
    clock.tick(60)