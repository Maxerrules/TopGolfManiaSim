#libraries
import sys
import pygame
from pygame.locals import QUIT
from random import randint as randint
from BGmap import BGmap
pygame.init()

#variables
DISPLAYSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
ENEMYSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
BGSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

width = DISPLAYSURF.get_width()
height = DISPLAYSURF.get_height()
transparent = (0, 0, 0, 100)
terrains = ["fairway", "rough", "green", "water", "bunker", "hole", "teebox"]

speed = 3
enemySpeed = 1

alive = True
won = False
level = 0

playerImgPath = "player_v2.png"
playerImg = pygame.image.load(playerImgPath)
playerImg = pygame.transform.scale_by(playerImg, 1)
playerRect = playerImg.get_rect()

FairwayImgPath = "Fairway.png"
FairwayImg = pygame.image.load(FairwayImgPath)

RoughImgPath = "Rough.png"
RoughImg = pygame.image.load(RoughImgPath)

ballImgPath = "New Piskel.png"
ballImg = pygame.image.load(ballImgPath)
ballRect = ballImg.get_rect()
ballAlive = False
ballSpeed = None, None

club1ImgPath = "golfClub.png"

clubImg = pygame.image.load(club1ImgPath)
clubRect = clubImg.get_rect()
clubRect.x, clubRect.y = width - clubImg.get_width() - 20, 20

holeImgPath = "New Piskel.png"
holeImg = pygame.image.load(holeImgPath)
holeRect = holeImg.get_rect()
holeRect.x, holeRect.y = randint(0, (width - holeImg.get_width())), randint(0, (height - holeImg.get_height()))

enemyImgPath = "Grassmaaier.png"
enemyImg = pygame.image.load(enemyImgPath)
enemyImg = pygame.transform.flip(enemyImg, True, False)
enemyRect= enemyImg.get_rect()
enemyRect.y = 250


pygame.display.set_caption("Golfrogue")
#pygame.display.toggle_fullscreen()

#functions

def move(input):
  """
  Beweegt de speler op basis van toetseninput.
  :param input: Keypress (pygame.key.get_pressed())
  :return (bool): Boolean waarde of er is bewogen.
  """
  global playerRect
  global speed
  global ballAlive

  if input[pygame.K_UP] and playerRect.y >= speed:
    playerRect.y -= speed
    return True
  if input[pygame.K_DOWN] and playerRect.y <= (height - speed - playerImg.get_height()):
    playerRect.y += speed
    return True
  if input[pygame.K_RIGHT] and playerRect.x <= (width - speed - playerImg.get_width()):
    playerRect.x += speed
    return True
  if input[pygame.K_LEFT] and playerRect.x >= speed:
    playerRect.x -= speed
    return True
  if input[pygame.K_EQUALS]:
    speed += 0.1
    pygame.time.wait(0.5)
    return False
  if input[pygame.K_MINUS] and speed >= 0.1:
    speed -= 0.1
    pygame.time.wait(0.5)
    return False
  if input[pygame.K_e] and not ballAlive:
    spawnBall()
    return True
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
  BGimgCode = None
  print(BGmap)
  for i in range(0, int(width/100)):
    for j in range(0, int(height/100)):
      BGimgCode = BGmap[i][j]
      if BGimgCode == 1:
        BGimg = FairwayImg
      elif BGimgCode == 2:
        BGimg = RoughImg
      else:
        BGimg = RoughImg
      BGSURF.blit(BGimg, (x+i*100, y+j*100))

def spawnBall():
  global ballAlive
  global ballSpeed

  ballAlive = True
  ballRect.x, ballRect.y = playerRect.x, playerRect.y
  ballSpeed = 2, 2

drawBG(0, 0, width, height)
while True:
  ENEMYSURF.fill(transparent)
  drawBG(0, 0, width, height)
  keypress = pygame.key.get_pressed()
  
  moved = move(keypress)
  if moved:
    DISPLAYSURF.fill(transparent)
    drawBG(0, 0, width, height)
   
  if enemyRect.x > width - enemyImg.get_width():
    enemyRect.x = 0
    enemyRect.y = randint(0, height)

  for event in pygame.event.get():   
    if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_w: #  Om achtergrond aan te passen, niet houden voor eindproduct
      height -= 100
    if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
      height += 100
    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
      width -= 100
    if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
      width += 100

  if won:
    #level += 1
    print("========== YAY! You won! ==========")
    pygame.quit()
    sys.exit()

  if playerRect.colliderect(enemyRect):
    alive = False
  elif ballRect.colliderect(holeRect):
    won = True

  enemyRect.x += enemySpeed 
  
  if ballAlive and (ballRect.x < width or ballRect.y < height):
    ballRect.x += ballSpeed[0]
    ballRect.y += ballSpeed[1]
    DISPLAYSURF.blit(ballImg, ballRect)
  elif ballAlive and (ballRect.x >= width or ballRect.y >= height):
    ballAlive = False
    pygame.quit()
    sys.exit()

  if alive == False:
    print("========== GAME OVER ==========")
    pygame.quit()
    sys.exit()

  pygame.time.wait(10)
  
  DISPLAYSURF.blit(holeImg, holeRect)
  DISPLAYSURF.blit(clubImg, clubRect)
  ENEMYSURF.blit(enemyImg, enemyRect)
  DISPLAYSURF.blit(playerImg, playerRect)
  pygame.display.update()