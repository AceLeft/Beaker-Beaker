import pygame
import random
from PlayerClass import Player 
from BackLoad import *
from Fallers import *

#BEAKER BEAKER by AceLeft
#music thanks to Centurion_of_war on opengameart
#glass shattering sound thanks to spookymodem
WIDTH = 500
HEIGHT = 600
FPS = 60

#get the screen up n running
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beaker Beaker")
clock = pygame.time.Clock()

#colors 
RED = (255,0,0)
BLUE = (0,0,255)
GOLD = (255,190,0)
BLACK = (0,0,0)
WHITE = (255,255,255)



STORAGE = Storage()

#gameplaying must be initilized before the opening sequence
gameplaying = True

playersChoice = STORAGE.openingSequence(screen)
if playersChoice == "quit":
   gameplaying = False


player = Player(playersChoice, STORAGE)



firstDrawGroup = pygame.sprite.Group()
secondDrawGroup = pygame.sprite.Group()
thirdDrawGroup = pygame.sprite.Group()
secondDrawGroup.add(player)

beakersGroup = pygame.sprite.Group()
enemiesGroup = pygame.sprite.Group()
enemiesHitBoxGroup = pygame.sprite.Group()

#the list is necessary so lives are killed in order
livesIcons = pygame.sprite.Group()
livesList = STORAGE.makeLivesList(player)
livesIcons.add(STORAGE.makeLivesGroup(livesList))

thirdDrawGroup.add(livesIcons)

allSprites = pygame.sprite.Group()
allSprites.add(player)

pygame.mixer.music.load("music/arbitternon_metal.ogg")
pygame.mixer.music.set_volume(.77)
pygame.mixer.music.play(loops=-1)
channelBreak = pygame.mixer.Channel(0)
channelCatch = pygame.mixer.Channel(1)

shatter = pygame.mixer.Sound("music/BottleBreakTrimmed.wav")
shatter.set_volume(.6)
blip = pygame.mixer.Sound("music/blip.wav")
blip.set_volume(1)

introing = True
while introing:
   #for future reference, clock.tick slows input reading down a lot
   clock.tick(FPS)
   for event in pygame.event.get():
      #check for closing window 
      if event.type == pygame.QUIT:
         gameplaying = False
         introing = False
   keystate = pygame.key.get_pressed()
   if keystate[pygame.K_LEFT] or keystate[pygame.K_RIGHT]:
      introing = False
         
   player.update()
   
   screen.fill(BLACK)
   Storage.drawText(screen, "Catch the beakers!", 30, ColorHolder(250,100,RED))
   Storage.drawText(screen, "(you can only catch beakers with the mouth of your beaker)", 17, ColorHolder(240,135,RED))
   Storage.drawText(screen, "Use the left and right arrowkeys to move", 24, ColorHolder(210,175,RED))
   Storage.drawText(screen, "(press left or right to start)", 17, ColorHolder(150,210,RED))
   secondDrawGroup.draw(screen)
   thirdDrawGroup.draw(screen)
   pygame.display.flip()

score = 0
while gameplaying:
   clock.tick(FPS)
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         gameplaying = False

      
   if pygame.time.get_ticks() % 35 == 0:
      beaker = Beaker(STORAGE)
      firstDrawGroup.add(beaker)
      beakersGroup.add(beaker)
      allSprites.add(beaker)
   if pygame.time.get_ticks() % random.randint(75,100) == 0:
      enemy = Enemy(STORAGE)
      firstDrawGroup.add(enemy)
      enemiesGroup.add(enemy)
      enemiesHitBoxGroup.add(enemy.hitBox)
      allSprites.add(enemy)
   
   beakersCaught = pygame.sprite.spritecollide(player.hitBox,beakersGroup,True)
   for beaker in beakersCaught:
         score += beaker.pointValue
         channelCatch.play(blip)
         
   playerHit = False
   enemiesCaught = pygame.sprite.spritecollide(player.hitBox,enemiesGroup,False)
   for enemy in enemiesCaught:
      if enemy.hitBox in pygame.sprite.spritecollide(player.hitBox,enemiesHitBoxGroup,False):
         playerHit = True
         enemy.hitBox.kill()
         enemy.kill()
   if playerHit:
      #shatter is just ever so slightly delayed and I cant fix it
      channelBreak.play(shatter)
      player.lives -=1
      player.rect.centerx = 250
      player.speedx = 0
      for enemy in enemiesGroup:
         enemy.hitBox.kill()
         enemy.kill()
      for beaker in beakersGroup:
         beaker.kill()
      livesList[player.lives].kill()
   
   #player death
   if player.lives <= 0:
      pygame.mixer.music.pause()
      player.hitBox.kill()
      player.kill()
      playersChoice = STORAGE.deadSequence(screen,score)
      score = 0
      if playersChoice == "quit":
         gameplaying = False
      player = Player(playersChoice, STORAGE)
      secondDrawGroup.add(player)
      allSprites.add(player)
      livesList = STORAGE.makeLivesList(player)
      livesIcons.add(STORAGE.makeLivesGroup(livesList))
      thirdDrawGroup.add(livesIcons)
      pygame.mixer.music.unpause()
              
   allSprites.update()
   scoreString = "Score: " + str(score)
   
   screen.fill(BLACK)
   screen.blit(STORAGE.choosingBackground, STORAGE.choosingBackground.get_rect())
   Storage.drawText(screen, scoreString, 24, ColorHolder(50,75,WHITE))
   firstDrawGroup.draw(screen)
   secondDrawGroup.draw(screen)
   thirdDrawGroup.draw(screen)
   pygame.display.flip()
   
pygame.quit()