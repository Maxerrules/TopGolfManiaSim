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
darkGray = (20, 20, 20, 0)
darkGreen = (15, 55, 10, 0)
terrains = ["fairway", "rough", "green", "water", "bunker", "hole", "teebox"]

started = False

startMenuImgPath = "Achtergrond.png"
startMenuImg = pygame.image.load(startMenuImgPath).convert_alpha()
startMenuRect = startMenuImg.get_rect()

startMenuMusic = "golfmania startmenu music.mp3"
gameMusic = "Golf game song.mp3"
youDed = "you ded.mp3"

speed = 5
enemySpeed = 2

alive = True
won = False
level = 0
tick = 0

playerImgPath = "player_v2.png"
playerImg = pygame.image.load(playerImgPath).convert_alpha()
playerImg = pygame.transform.scale_by(playerImg, 1)
playerRect = playerImg.get_rect()

FairwayImgPath = "Fairway.png"
FairwayImg = pygame.image.load(FairwayImgPath).convert_alpha()
fairwayRect = FairwayImg.get_rect()

RoughImgPath = "Rough.png"
RoughImg = pygame.image.load(RoughImgPath).convert_alpha()
RoughRect = RoughImg.get_rect()

GreenImgPath = "groem.png"
GreenImg = pygame.image.load(GreenImgPath).convert_alpha()
GreenRect = GreenImg.get_rect()

WaterImgPath = "waderr.png"
WaterImg = pygame.image.load(WaterImgPath).convert_alpha()
WaterRect = WaterImg.get_rect()

ballImgPath = "ball.png"
ballImg = pygame.image.load(ballImgPath).convert_alpha()
ballRect = ballImg.get_rect()
ballAlive = False
ballSpeed = 3, 3
ballMovementSpeed = 5
amountOfBalls = 5

ballMachineImgPath = "Golfballenmachine.png"
ballMachineimg = pygame.image.load(ballMachineImgPath).convert_alpha()
ballMachineRect = ballMachineimg.get_rect()


clubSelected = 0
clubImgPaths = ["golfClub.png", "driver.png", "putter.png"]
clubImg = pygame.image.load(clubImgPaths[clubSelected]).convert_alpha()
clubRect = clubImg.get_rect()
clubRect.x, clubRect.y = 20, height - clubImg.get_height() - 20
clubBGRect = pygame.Rect(clubRect.x - 10, clubRect.y - 10, clubRect.width + 20, clubRect.height + 20)
clubWait = False
clubClock = 0

holeImgPath = "hole.png"
holeImg = pygame.image.load(holeImgPath).convert_alpha()
holeSpriteRect = holeImg.get_rect()

enemyImgPath = "Grassmaaier.png"
enemyImg = pygame.image.load(enemyImgPath).convert_alpha()
enemyImg = pygame.transform.flip(enemyImg, True, False)
enemyRect= enemyImg.get_rect()
enemyRect.y = height - 100
enemyRect.x = 0 - enemyRect.width

oldManImgPath = "oldMan.png"
oldManImg = pygame.image.load(oldManImgPath).convert_alpha()
oldManRect = oldManImg.get_rect()
oldManRect.x = 500
oldManRect.y = 500
oldManAlive = True
oldManSpeed = 1

golfKarImgPath = "golfkar.png"
golfKarImg = pygame.image.load(golfKarImgPath).convert_alpha()
golfKarRect = golfKarImg.get_rect()
golfKarAlive = True
golfKarSpeed = 3

pygame.display.set_caption("Golfrogue")

#functions

def move(input):
  """
  Beweegt de speler op basis van toetseninput.
  :param input: Keypress (pygame.key.get_pressed())
  :return (bool): Boolean waarde of er is bewogen.
  """
  global playerRect
  global speed
  global amountOfBalls
  global clubSelected
  global clubImg
  global clubWait

  if input[pygame.K_UP] and playerRect.y >= speed:
    playerRect.y -= speed
  if input[pygame.K_DOWN] and playerRect.y <= (height - speed - playerImg.get_height()):
    playerRect.y += speed
  if input[pygame.K_RIGHT] and playerRect.x <= (width - speed - playerImg.get_width()):
    playerRect.x += speed
  if input[pygame.K_LEFT] and playerRect.x >= speed:
    playerRect.x -= speed
  if input[pygame.K_d] and not ballAlive and amountOfBalls > 0:
    spawnBallMovingRight()
    amountOfBalls = amountOfBalls - 1
  if input[pygame.K_a] and not ballAlive and amountOfBalls > 0:
    spawnBallMovingLeft()
    amountOfBalls = amountOfBalls - 1
  if input[pygame.K_s] and not ballAlive and amountOfBalls > 0:
    spawnBallMovingDown()
    amountOfBalls = amountOfBalls - 1
  if input[pygame.K_w] and not ballAlive and amountOfBalls > 0:
    spawnBallMovingUp()
    amountOfBalls = amountOfBalls - 1
  if input[pygame.K_q] and not clubWait:
    if clubSelected > 0:
      clubSelected -= 1
      clubImg = pygame.image.load(clubImgPaths[clubSelected]).convert_alpha()
      clubWait = True
    elif clubSelected == 0:
      clubSelected = 2
      clubImg = pygame.image.load(clubImgPaths[clubSelected]).convert_alpha()
      clubWait = True
  if input[pygame.K_e] and not clubWait:
    if clubSelected < 2:
      clubSelected += 1
      clubImg = pygame.image.load(clubImgPaths[clubSelected]).convert_alpha()
      clubWait = True
    elif clubSelected == 2:
      clubSelected = 0
      clubImg = pygame.image.load(clubImgPaths[clubSelected]).convert_alpha()
      clubWait = True

def spawnBallMovingRight():
  global ballAlive
  global ballSpeed

  ballAlive = True
  ballRect.x, ballRect.y = playerRect.x + 5, playerRect.y + 40
  ballSpeed = ballMovementSpeed, 0

def spawnBallMovingLeft():
  global ballAlive
  global ballSpeed

  ballAlive = True
  ballRect.x, ballRect.y = playerRect.x - 5, playerRect.y + 40
  ballSpeed = -ballMovementSpeed, 0

def spawnBallMovingUp():
  global ballAlive
  global ballSpeed

  ballAlive = True
  ballRect.x, ballRect.y = playerRect.x, playerRect.y
  ballSpeed = 0, -ballMovementSpeed

def spawnBallMovingDown():
  global ballAlive
  global ballSpeed

  ballAlive = True
  ballRect.x, ballRect.y = playerRect.x, playerRect.y + 20
  ballSpeed = 0, ballMovementSpeed

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
  for i in range(0, int(width/100) + 1):
    for j in range(0, int(height/100) + 1):
      BGimgCode = BGmap[i][j]
      if BGimgCode == 1:
        BGimg = FairwayImg
      elif BGimgCode == 2:
        BGimg = RoughImg
      elif BGimgCode == 3:
        BGimg = GreenImg
      else:
        BGimg = RoughImg
      BGSURF.blit(BGimg, (x+i*100, y+j*100))



def text_object(text, font):
  textSurface = font.render(text, True, (0, 0, 0))
  return textSurface, textSurface.get_rect()

def drawMessage(message, x, y, size):
  font = pygame.font.Font('PixeloidSans.ttf', size)
  TextSurf, TextRect = text_object(message, font)
  TextRect.center = (x, y)
  DISPLAYSURF.blit(TextSurf, TextRect)

def drawTitle(message, x, y):
  font = pygame.font.Font('Pixeboy.ttf', 300)
  TextSurf, TextRect = text_object(message, font)
  TextRect.center = (x, y)
  DISPLAYSURF.blit(TextSurf, TextRect)

pygame.mixer.music.load(startMenuMusic)
pygame.mixer.music.play(-1)
while not started:

  DISPLAYSURF.fill(transparent)
  startMenuImg = pygame.transform.scale(startMenuImg, (width, height))
  DISPLAYSURF.blit(startMenuImg, (0, 0))
  DISPLAYSURF.blit(enemyImg, enemyRect)

  drawMessage("Press space to start!", width/2, 500, 50)
  drawTitle("GOLFMANIA", width/2, 250)
  drawMessage("Press t for tutorial!", width/2, 600, 30)


  enemyRect.x += enemySpeed 
  if enemyRect.x > width - enemyImg.get_width() and (randint(1, 1000) == 1 or tick % 1000 == 0):
    enemyRect.x = 0 - enemyRect.width
    enemyRect.y = height - 100

  for event in pygame.event.get():   
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
      started = True
      pygame.mixer.music.stop()
      pygame.mixer.music.unload()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
      inTutorial = True
  pygame.display.update()
  tick += 1


drawBG(0, 0, width, height)
pygame.mixer.music.load(gameMusic)
pygame.mixer.music.play(-1)
while inTutorial:
  drawMessage("Use arrow keys to move", width/2, height/2, 50)

while started:

  enemyRect.y = 250
  enemyRect.x = 0
  holeSpriteRect.x = 1200
  holeSpriteRect.y = height/2
  holeRect = pygame.Rect(holeSpriteRect.x, holeSpriteRect.y + 75, 45, 25)
  playerRect.y = 0
  playerRect.x = 0
  enemyAlive = True
  level = 1
  oldManRect.x = 500
  oldManRect.y = 500
  oldManAlive = True
  ballMachineRect.x = width - 100
  ballMachineRect.y = 0
  ballClock = 0
  golfKarAlive = True
  golfKarRect.x = 600
  golfKarRect.y = 600
  golfKarLives = 3
  pygame.mixer.music.load(gameMusic)
  pygame.mixer.music.play(-1)
  clubWait = False
  clubClock = 0

  while alive:
    drawBG(0, 0, width, height)
    keypress = pygame.key.get_pressed()
    move(keypress)
    
    if enemyRect.x > width - enemyImg.get_width():
      enemyRect.x = 0
      enemyRect.y = randint(0, height)

    for event in pygame.event.get():   
      if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()      

    if (playerRect.colliderect(enemyRect) and enemyAlive == True) or (playerRect.colliderect(oldManRect) and oldManAlive == True) or (playerRect.colliderect(golfKarRect) and golfKarAlive == True):
      alive = False
      ballAlive = False
      enemyAlive = False
      oldManAlive = False
      golfKarAlive = False
    elif ballRect.colliderect(holeRect) and enemyAlive == False and oldManAlive == False and not golfKarAlive:
      level = level+1 
      ballAlive = False
    elif ballRect.colliderect(enemyRect) and enemyAlive and ballAlive:
      enemyAlive = False
      enemyRect.x, enemyRect.y = -enemyRect.width, -enemyRect.y
      ballAlive = False
    elif ballRect.colliderect(oldManRect) and oldManAlive and ballAlive:
      oldManAlive = False
      oldManRect.x, oldManRect.y = -oldManRect.width, -oldManRect.y
      ballAlive = False
    elif ballRect.colliderect(golfKarRect) and golfKarAlive and ballAlive:
      golfKarLives = golfKarLives - 1
      ballAlive = False

    if golfKarLives == 0:
      golfKarAlive = False


    enemyRect.x += enemySpeed
 
    if ballAlive and ballRect.x < width and ballRect.y < height and ballRect.x > 0 and ballRect.y > 0:
      ballRect.x += ballSpeed[0]
      ballRect.y += ballSpeed[1]
      DISPLAYSURF.blit (ballImg, ballRect)
    elif ballAlive and (ballRect.x >= width or ballRect.y >= height or ballRect.x <= 0 or ballRect.y <= 0):
      ballAlive = False

    if playerRect.colliderect(ballMachineRect) and tick > ballClock:
      amountOfBalls = 5
      ballClock = tick + 600
    
    if tick < ballClock - 500:
      drawMessage("You got new ballz!", width/2, height/2, 90)

    drawMessage("Balls: " + str(amountOfBalls), width - 50, height - 50, 20)

    if oldManRect.x > playerRect.x:
      oldManRect.x = oldManRect.x - oldManSpeed
    elif oldManRect.x < playerRect.x:
      oldManRect.x = oldManRect.x + oldManSpeed
    
    if oldManRect.y > playerRect.y:
      oldManRect.y = oldManRect.y - oldManSpeed
    elif oldManRect.y < playerRect.x:
      oldManRect.y = oldManRect.y + oldManSpeed

    if golfKarRect.x > playerRect.x:
      golfKarRect.x = golfKarRect.x - golfKarSpeed
    if golfKarRect.x < playerRect.x:
      golfKarRect.x = golfKarRect.x + golfKarSpeed

    if golfKarRect.y > playerRect.y:
      golfKarRect.y = golfKarRect.y - golfKarSpeed
    if golfKarRect.y < playerRect.y:
      golfKarRect.y = golfKarRect.y + golfKarSpeed

    
    if clubWait == True and clubClock <= 100:
      clubClock += 1
    elif clubClock > 100:
      clubWait = False

    if amountOfBalls == 0:
      drawMessage("You got no ballz!", width/2, height/2, 50)
    pygame.time.wait(10)

    DISPLAYSURF.blit(ballMachineimg, ballMachineRect)

    if golfKarAlive:
      DISPLAYSURF.blit(golfKarImg, golfKarRect)

    if oldManAlive == True:
      ENEMYSURF.blit(oldManImg, oldManRect)
    if oldManAlive == False and enemyAlive == False:
      DISPLAYSURF.blit(holeImg, holeSpriteRect)
    
    pygame.draw.rect(DISPLAYSURF, darkGreen, clubBGRect)
    DISPLAYSURF.blit(clubImg, clubRect)

    if enemyAlive == True:
      ENEMYSURF.blit(enemyImg, enemyRect)

    DISPLAYSURF.blit(playerImg, playerRect)

    pygame.time.wait(10)
    pygame.display.update()
    tick += 1


  pygame.mixer.music.load(youDed)
  pygame.mixer.music.play(-1)
  while not alive:
    tick = 0
    startMenuImg = pygame.transform.scale(startMenuImg, (width, height))
    DISPLAYSURF.blit(startMenuImg, (0, 0))

    drawMessage("Press space to restart", width/2, 600, 30)
    drawTitle("You Died", width/2, 300)
    for event in pygame.event.get():   
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        alive = True
    
    pygame.display.update()