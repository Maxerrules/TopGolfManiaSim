#libraries
import sys
import pygame
from pygame.locals import QUIT
from random import randint as randint

pygame.init()

#variables
DISPLAYSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
ENEMYSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
BGSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
x = 0
y = 0
width = DISPLAYSURF.get_width()
height = DISPLAYSURF.get_height()
transparent = (0, 0, 0, 100)
terrains = ["fairway", "rough", "green", "water", "bunker", "hole", "teebox"]
speed = 5
enemySpeed = 1
won = False
level = 0
playerImgPath = "player_v2.png"
playerImg = pygame.image.load(playerImgPath)
FairwayImgPath = "Fairway.png"
RoughImgPath = "Rough.png"
BGimg = pygame.image.load(FairwayImgPath)
enemyImgPath = "Grassmaaier.png"
enemyImg = pygame.image.load(enemyImgPath)
enemyImg = pygame.transform.flip(enemyImg, True, False)
enemyX = 0
enemyY = 250
alive = True



pygame.display.set_caption("Golfrogue")

#functions

def move(input):
  """
  Beweegt de speler op basis van toetseninput.
  :param input: Keypress (pygame.key.get_pressed())
  :return (bool): Boolean waarde of er is bewogen.
  """
  global x
  global y
  global speed

  if input[pygame.K_UP] and y >= speed:
    y -= speed
    return True
  if input[pygame.K_DOWN] and y <= (height - speed - playerImg.get_height()):
    y += speed
    return True
  if input[pygame.K_RIGHT] and x <= (width - speed - playerImg.get_width()):
    x += speed
    return True
  if input[pygame.K_LEFT] and x >= speed:
    x -= speed
    return True
  if input[pygame.K_EQUALS]:
    speed += 0.1
    pygame.time.wait(0.5)
    return False
  if input[pygame.K_MINUS] and speed >= 0.1:
    speed -= 0.1
    pygame.time.wait(0.5)
    return False
  return False

def drawBG(x, y, width, height):
  """
  Tekent de achtergrond. Aangrijpingspunt op x en y, een hoogte van height, en een breedte van width.
  :param x: De x van het startpunt.
  :param y: De y van het startpunt.
  :param width: De breedte van de te tekenen achtergrond.
  :param height: De hoogte van de te tekenen achtergrond.
  :return: None
  """
  global BGimg
  for i in range(0, int(width/100)):
    for j in range(0, int(height/100)):
      BGSURF.blit(BGimg, (x+i*100, y+j*100))

drawBG(0, 0, width, height)
while True:
  ENEMYSURF.fill(transparent)
  keypress = pygame.key.get_pressed()
  
  moved = move(keypress)
  if moved:
    DISPLAYSURF.fill(transparent)
  img = pygame.transform.scale_by(playerImg, 1)
  
  if won:
    level += 1

  if enemyX > width:
    enemyX = 0
    enemyY = randint(0, height)

  for event in pygame.event.get():   
    if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
      height -= 100
      drawBG(0, 0, width, height)
    if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
      height += 100
      drawBG(0, 0, width, height)
    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
      width -= 100
      drawBG(0, 0, width, height)
    if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
      width += 100
      drawBG(0, 0, width, height)

  
  if x >= enemyX - 35 and x <= enemyX + 35 and y <= enemyY + 100 and y >= enemyY - 35:
    alive = False


  enemyX += enemySpeed 
  
  if alive == False:
    pygame.quit()
    sys.exit()

  pygame.time.wait(1)
  
  DISPLAYSURF.blit(img, (x,y))
  ENEMYSURF.blit(enemyImg, (enemyX, enemyY))
  pygame.display.update()