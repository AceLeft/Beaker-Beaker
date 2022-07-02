import pygame
from BackLoad import Storage

class Player(pygame.sprite.Sprite):
   def __init__(self, beakerChoice, Storage):
      pygame.sprite.Sprite.__init__(self)
      self.speedx = 0
      self.removeControls = True
      self.image = beakerChoice
      self.lives = 5
      #rect is an attribute for Sprites
      self.rect = self.image.get_rect()
      self.rect.bottom = 600
      self.rect.centerx = 250
      self.hitBox = PlayerHitBox(beakerChoice, Storage)
      self.hitBox.rect.top = self.rect.top
      self.hitBox.rect.left = self.rect.left + self.hitBox.leftDisplacement
         
      self.icon = Storage.wideIcon
      if(beakerChoice == Storage.triangleHand):
         self.icon = Storage.triangleIcon
      elif(beakerChoice == Storage.skinnyHand):
         self.icon = Storage.skinnyIcon
      
   def update(self):
      if self.speedx > 0:
         self.speedx -= 1
      if self.speedx <0:
         self.speedx +=1
      if self.speedx == 0:
         self.removeControls = False
      maxSpeed = 6
      keystate = pygame.key.get_pressed()
      if keystate[pygame.K_LEFT] and self.removeControls == False:
         if self.speedx > -1 *maxSpeed:
            self.speedx -= 2
         else:
            self.speedx = -1* maxSpeed
      if keystate[pygame.K_RIGHT] and self.removeControls == False:
         if self.speedx < maxSpeed:
            self.speedx += 2
         else:
            self.speedx = maxSpeed
      self.rect.x += self.speedx
      self.hitBox.rect.left = self.rect.left + self.hitBox.leftDisplacement
      WIDTH = 500
      if self.hitBox.rect.right > WIDTH:
         self.hitBox.rect.right = WIDTH
         self.rect.left = self.hitBox.rect.left - self.hitBox.leftDisplacement
      if self.hitBox.rect.left < 0:
         self.hitBox.rect.left = 0
         self.rect.left = self.hitBox.rect.left - self.hitBox.leftDisplacement
         
class PlayerHitBox(pygame.sprite.Sprite):
   def __init__(self,beakerChoice, Storage):
      pygame.sprite.Sprite.__init__(self)
      self.image = Storage.wideHitBox
      self.leftDisplacement = 3*2
      if(beakerChoice == Storage.triangleHand):
         self.image = Storage.triangleHitBox
         self.leftDisplacement = 9*2
      elif(beakerChoice == Storage.skinnyHand):
         self.image = Storage.skinnyHitBox
         self.leftDisplacement = 14*2
      self.rect = self.image.get_rect()