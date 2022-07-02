import pygame

class Storage:
   #class is essentially a misc variables and methods container
   def __init__(self):
      oldTriangleHand = pygame.image.load("images/triangleHand.gif").convert()
      oldSkinnyHand = pygame.image.load("images/skinnyHand.gif").convert()
      oldWideHand = pygame.image.load("images/wideHand.gif").convert()
      #these numbers are double the w and height of the originals
      self.triangleHand = pygame.transform.scale(oldTriangleHand, (108,160))
      self.skinnyHand = pygame.transform.scale(oldSkinnyHand, (88,200))
      self.wideHand = pygame.transform.scale(oldWideHand, (170,150))
      
      self.triangleIcon = pygame.transform.scale(oldTriangleHand, (22,32))
      self.skinnyIcon = pygame.transform.scale(oldSkinnyHand, (18,40))
      self.wideIcon = pygame.transform.scale(oldWideHand, (34,30))
      
      
      triangleBeaker = pygame.image.load("images/triangleBeaker.gif").convert()
      wideBeaker = pygame.image.load("images/wideBeaker.gif").convert()
      skinnyBeaker = pygame.image.load("images/skinnyBeaker.gif").convert()
      #list in order of start menu appearance
      self.beakersList = [wideBeaker, skinnyBeaker, triangleBeaker]
      #attributes are the large ones
      self.triangleBeaker = pygame.transform.scale(triangleBeaker, (100,160))
      self.wideBeaker = pygame.transform.scale(wideBeaker, (150,150))
      self.skinnyBeaker = pygame.transform.scale(skinnyBeaker, (50,200))
      
      self.pointer = pygame.image.load("images/pointer.gif").convert()
      
      hammer = pygame.image.load("images/hammer.gif").convert()
      bomb = pygame.image.load("images/bomb.gif").convert()
      bowlingBall = pygame.image.load("images/bowlingBall.gif").convert()
      self.enemiesList = [bomb, hammer, bowlingBall]
      self.hammerBox =pygame.image.load("images/hammerBox.gif").convert()
      self.bombBox = pygame.image.load("images/bombBox.gif").convert()
      self.bowlingBallBox = pygame.image.load("images/bowlingBallBox.gif").convert()
      
      oldTriangleHitBox = pygame.image.load("images/triangleBox.gif").convert()
      oldWideHitBox = pygame.image.load("images/wideBox.gif").convert()
      oldSkinnyHitBox = pygame.image.load("images/skinnyBox.gif").convert()
      self.triangleHitBox = pygame.transform.scale(oldTriangleHitBox, (64,16))
      self.skinnyHitBox = pygame.transform.scale(oldSkinnyHitBox, (54,24))
      self.wideHitBox = pygame.transform.scale(oldWideHitBox, (147,16))
      
      self.choosingBackground = pygame.image.load("images/choosingBackground.gif").convert()
   
   def drawText(surface,text,size, colorHolder):
      fontName = pygame.font.match_font("helvetica", True, False)
      font = pygame.font.Font(fontName, size)
      textSurface = font.render(text, True ,colorHolder.color)
      textRect = textSurface.get_rect()
      textRect.midtop = (colorHolder.x, colorHolder.y)
      surface.blit(textSurface,textRect)
   
   
   
   def openingSequence(self, surface):
      #these are beakers instead of hands because the disembodied hand
      #looked weird
      optionWide = Decoration( ColorHolder(25, 300, self.wideBeaker))
      optionSkinny = Decoration( ColorHolder(250, 225, self.skinnyBeaker))
      optionTriangle = Decoration( ColorHolder(375, 275, self.triangleBeaker))
      firstDrawGroup = pygame.sprite.Group()
      firstDrawGroup.add(optionWide, optionSkinny, optionTriangle)
      for sprite in firstDrawGroup.sprites():
         sprite.rect.bottom = 400
      pointer = Decoration( ColorHolder(0, 425, self.pointer))
      pointer.rect.centerx = optionWide.rect.centerx
      firstDrawGroup.add(pointer)
      
      pointerPlaces = [optionWide.rect.centerx, optionSkinny.rect.centerx, optionTriangle.rect.centerx]
      
      result = self.wideHand
      choosing = True
      while choosing:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               return "quit"
            if event.type == pygame.KEYUP:
               wait = False
         keystate = pygame.key.get_pressed()
         if keystate[pygame.K_RETURN]:
            choosing = False
            
         if keystate[pygame.K_1]:
            pointer.rect.centerx = optionWide.rect.centerx
            result = self.wideHand           
         if keystate[pygame.K_2]:
            pointer.rect.centerx = optionSkinny.rect.centerx
            result = self.skinnyHand
         if keystate[pygame.K_3]:
            pointer.rect.centerx = optionTriangle.rect.centerx
            result = self.triangleHand

         surface.fill((0,0,255))
         surface.blit(self.choosingBackground, self.choosingBackground.get_rect())
         firstDrawGroup.draw(surface)
         Storage.drawText(surface, "BEAKER BEAKER", 32, ColorHolder(250,110,(255,255,255)))
         Storage.drawText(surface, "by AceLeft", 19, ColorHolder(250,150,(255,255,255)))
         Storage.drawText(surface, "(Beaker beaker: a beaker that holds other beakers)", 15, ColorHolder(250,175,(255,255,255)))
         Storage.drawText(surface, "Use 1, 2, or 3 to choose a beaker", 24, ColorHolder(250,475,(255,190,0)))
         Storage.drawText(surface, "and press enter to select", 24,ColorHolder(250,510,(255,190,0)))
         pygame.display.flip()
      return result
   
   def deadSequence(self, surface, score):
      deciding = True
      while deciding:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               deciding = False
               return "quit"
         surface.fill((0,0,0))
         
         Storage.drawText(surface, "Final score: " + str(score), 30,ColorHolder(250,250,(255,190,0)))
         Storage.drawText(surface, "Press enter to try again", 17,ColorHolder(240,285,(255,190,0)))
         Storage.drawText(surface, "Remember to always wear" , 34,ColorHolder(250,400,(255,0,0)))
         Storage.drawText(surface, "the proper safety equipment!" , 34,ColorHolder(250,435,(255,0,0)))
         
         keystate = pygame.key.get_pressed()
         if keystate[pygame.K_RETURN]:
            deciding = False
            keydown = True
            while keydown:
               for event in pygame.event.get():
                  if event.type == pygame.KEYUP:
                     keydown = False
                     return self.openingSequence(surface)
         pygame.display.flip()
         
   def makeLivesList(self,player):
      life1 = Decoration( ColorHolder(5, 0, player.icon))
      life2 = Decoration( ColorHolder(40, 0, player.icon))
      life3 = Decoration( ColorHolder(75, 0, player.icon))
      life4 = Decoration( ColorHolder(110, 0, player.icon))
      life5 = Decoration( ColorHolder(145, 0, player.icon))
      return [life1,life2,life3,life4,life5]
         
   def makeLivesGroup(self,lifeList):
      group = pygame.sprite.Group()
      for life in lifeList:
         group.add(life)
         life.rect.bottom = 600
      return group
class ColorHolder:
   def __init__(self, x, y, color):
      self.x = x
      self.y = y
      self.color = color
      
      
class Decoration(pygame.sprite.Sprite):
   def __init__(self, colorHolder):
      pygame.sprite.Sprite.__init__(self)
      self.image = colorHolder.color
      self.rect = self.image.get_rect()
      self.rect.x = colorHolder.x
      self.rect.y = colorHolder.y

