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

won = False
level = 0

playerImgPath = "player_v2.png"
playerImg = pygame.image.load(playerImgPath)
playerRect = playerImg.get_rect()

FairwayImgPath = "Fairway.png"
FairwayImg = pygame.image.load(FairwayImgPath)

RoughImgPath = "Rough.png"
RoughImg = pygame.image.load(RoughImgPath)

ballImgPath = "New Piskel.png"
ballImg = pygame.image.load(ballImgPath)

enemyImgPath = "Grassmaaier.png"
enemyImg = pygame.image.load(enemyImgPath)
enemyImg = pygame.transform.flip(enemyImg, True, False)
enemyRect= enemyImg.get_rect()
alive = True



pygame.display.set_caption("Golfrogue")
pygame.display.toggle_fullscreen()

#functions

def move(input):
  """
  Beweegt de speler op basis van toetseninput.
  :param input: Keypress (pygame.key.get_pressed())
  :return (bool): Boolean waarde of er is bewogen.
  """
  global playerRect
  global speed

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
  global ballImg
  for i in range(0, int(width/100)):
    for j in range(0, int(height/100)):
      #BGimgCode = BGmap[i][j]
      #if BGimgCode == 1:
      #  BGimg = FairwayImg
      #elif BGimgCode == 2:
      #  BGimg = RoughImg
      #else:
      BGimg = ballImg
      BGSURF.blit(BGimg, (x+i*100, y+j*100))
      print(j)
    print(i)

drawBG(0, 0, width, height)
while True:
  ENEMYSURF.fill(transparent)
  drawBG(0, 0, width, height)
  keypress = pygame.key.get_pressed()
  
  moved = move(keypress)
  if moved:
    DISPLAYSURF.fill(transparent)
    drawBG(0, 0, width, height)
 
  img = pygame.transform.scale_by(playerImg, 1)
  
  if won:
    level += 1

  if enemyRect.x > width - enemyImg.get_width()  :
    enemyRect.x = 0
    enemyRect.y = randint(0, height)

  for event in pygame.event.get():   
    if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
      height -= 100
    if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
      height += 100
    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
      width -= 100
    if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
      width += 100

  
  #if playerX >= enemyX - 35 and playerX <= enemyX + 35 and playerY <= enemyY + 100 and playerY >= enemyY - 35:
  if enemyRect.colliderect(playerRect) and pygame.key.get_pressed()[pygame.K_q]:
    alive = False


  enemyRect.x += enemySpeed 
  
  if alive == False:
    print("========== GAME OVER ==========")
    pygame.quit()
    sys.exit()

  pygame.time.wait(10)
  
  DISPLAYSURF.blit(img, playerRect)
  ENEMYSURF.blit(enemyImg, enemyRect)
  pygame.display.update()