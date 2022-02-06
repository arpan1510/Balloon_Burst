import mediapipe
import pygame,random
import cv2
import numpy
from handtracking import HandTracking

# capture video file



class Pin(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.handtrackingobj = HandTracking()
        self.handclosed=False
        self.image=pygame.image.load("../assets/pin.png").convert_alpha()
        self.rect=self.image.get_rect()
        self.frame=self.cap.read()
        self.frame1=self.cap.read()
        

    def load_camera(self):
        _, self.frame = self.cap.read()
        


    def set_hand_position(self):
        self.frame = self.handtrackingobj.scan_hands(self.frame)
        self.rect.center =self.handtrackingobj.get_hand_center()
        # cv2.imshow("image",self.frame)
        # cv2.waitKey(1)

    def getCamFrame(self):
        _, pyimage = self.cap.read()
        pyimage=cv2.cvtColor(pyimage,cv2.COLOR_BGR2RGB)
        # if not color:
        #     frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #     frame=cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
        pyimage=numpy.rot90(pyimage)
        pyimage=pygame.surfarray.make_surface(pyimage)
        pyimage=pygame.transform.scale(pyimage,(1280,720))
        pyimage.set_alpha(50)
        return pyimage
        

            
    def update(self):
        self.load_camera()
        self.set_hand_position()
        self.framepyimage = pygame.image.frombuffer(self.frame.tostring(), self.frame.shape[1::-1],"RGB")
        self.handclosed=self.handtrackingobj.hand_closed
        # self.rect.center=pygame.mouse.get_pos()
        # self.handtracking.display_hand()
        