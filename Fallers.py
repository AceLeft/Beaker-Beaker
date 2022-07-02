import pygame
import random
from BackLoad import ColorHolder


class Beaker(pygame.sprite.Sprite):
   def __init__(self, Storage):
      pygame.sprite.Sprite.__init__(self)
      randomNumber = random.randint(0,2)
      if randomNumber ==0: 
         self.pointValue = 25
      elif randomNumber == 1:
         self.pointValue = 78
      else:
         self.pointValue = 51
      self.image = Storage.beakersList[randomNumber]
      self.rect = self.image.get_rect()
      self.rect.bottom = -1
      self.rect.centerx = random.randint(25, 450)
      self.speedy = random.randint(2,4)
   
   def update(self):
      self.rect.y += self.speedy
      if self.rect.top > 600:
         self.kill()
      
      
      
class Enemy(pygame.sprite.Sprite):
   def __init__(self, Storage):
      pygame.sprite.Sprite.__init__(self)
      self.image = Storage.enemiesList[random.randint(0,2)]
      self.rect = self.image.get_rect()
      self.rect.bottom = -1
      self.speedy = random.randint(2,3)
      self.rect.centerx = random.randint(25, 450)
      self.hitBox = EnemyHitBox(self.image, Storage)
   
   def update(self):
      self.rect.y += self.speedy
      self.hitBox.rect.bottom = self.rect.bottom
      self.hitBox.rect.left = self.rect.left
      
      if self.rect.top > 600:
         self.hitBox.kill()
         self.kill()
      
      
class EnemyHitBox(pygame.sprite.Sprite):
   def __init__(self,image, Storage):
      pygame.sprite.Sprite.__init__(self)
      self.image = Storage.bombBox
      if image == Storage.enemiesList[1]:
         self.image = Storage.hammerBox
      elif image == Storage.enemiesList[2]:
         self.image = Storage.bowlingBallBox
      self.rect = self.image.get_rect()
      