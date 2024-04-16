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

started = False

startMenuImgPath = "Achtergrond.png"
startMenuImg = pygame.image.load(startMenuImgPath).convert_alpha()
startMenuRect = startMenuImg.get_rect()

startMenuMusic = "golfmania startmenu music.mp3"
gameMusic = "Golf game song.mp3"
youDed = "you ded.mp3"

speed = 3
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

RoughImgPath = "Rough.png"
RoughImg = pygame.image.load(RoughImgPath).convert_alpha()

GreenImgPath = "groem.png"
GreenImg = pygame.image.load(GreenImgPath).convert_alpha()

WaterImgPath = "waderr.png"
WaterImg = pygame.image.load(WaterImgPath).convert_alpha()

ballImgPath = "ball.png"
ballImg = pygame.image.load(ballImgPath).convert_alpha()
ballRect = ballImg.get_rect()
ballAlive = False
ballSpeed = 3, 3

club1ImgPath = "golfClub.png"

clubImg = pygame.image.load(club1ImgPath).convert_alpha()
clubRect = clubImg.get_rect()
clubRect.x, clubRect.y = width - clubImg.get_width() - 20, 20

holeImgPath = "hole.png"
holeImg = pygame.image.load(holeImgPath).convert_alpha()
holeRect = holeImg.get_rect()

enemyImgPath = "Grassmaaier.png"
enemyImg = pygame.image.load(enemyImgPath).convert_alpha()
enemyImg = pygame.transform.flip(enemyImg, True, False)
enemyRect= enemyImg.get_rect()
enemyRect.y = height - 100
enemyRect.x = 0 - enemyRect.width

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

  if input[pygame.K_UP] and playerRect.y >= speed:
    playerRect.y -= speed
  if input[pygame.K_DOWN] and playerRect.y <= (height - speed - playerImg.get_height()):
    playerRect.y += speed
  if input[pygame.K_RIGHT] and playerRect.x <= (width - speed - playerImg.get_width()):
    playerRect.x += speed
  if input[pygame.K_LEFT] and playerRect.x >= speed:
    playerRect.x -= speed
  if input[pygame.K_SPACE] and not ballAlive:
    spawnBall()

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
  for i in range(0, int(width/100)):
    for j in range(0, int(height/100)):
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

def spawnBall():
  global ballAlive
  global ballSpeed

  ballAlive = True
  ballRect.x, ballRect.y = playerRect.x + 5, playerRect.y + 5
  ballSpeed = 2, 2

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

  drawMessage("Press G to start!", width/2, 500, 50)
  drawTitle("GOLFMANIA", width/2, 250)
  drawMessage("Use arrow keys to move", width/2, 600, 30)

  enemyRect.x += enemySpeed 
  if enemyRect.x > width - enemyImg.get_width() and (randint(1, 1000) == 1 or tick % 1000 == 0):
    enemyRect.x = 0 - enemyRect.width
    enemyRect.y = height - 100

  for event in pygame.event.get():   
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
      started = True
      pygame.mixer.music.stop()
      pygame.mixer.music.unload()
  
  pygame.display.update()
  tick += 1


drawBG(0, 0, width, height)
while started:

  enemyRect.y = 250
  enemyRect.x = 0
  holeRect.x = 1200
  holeRect.y = height/2
  playerRect.y = 0
  playerRect.x = 0
  enemyAlive = True
  level = 1
  pygame.mixer.music.load(gameMusic)
  pygame.mixer.music.play(-1)

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

    if playerRect.colliderect(enemyRect):
      alive = False
      ballAlive = False
      enemyAlive = False
    elif ballRect.colliderect(holeRect) and enemyAlive == False:
      level = level+1 
      ballAlive = False
    elif ballRect.colliderect(enemyRect):
      enemyAlive = False
      enemyRect.x, enemyRect.y = -enemyRect.width, -enemyRect.y
      ballAlive = False

    enemyRect.x += enemySpeed

    if ballAlive and ballRect.x < width and ballRect.y < height:
      ballRect.x += ballSpeed[0]
      ballRect.y += ballSpeed[1]
      DISPLAYSURF.blit(ballImg, ballRect)
    elif ballAlive and (ballRect.x >= width or ballRect.y >= height):
      ballAlive = False

    if alive == False:
      print("========== GAME OVER ==========")


    pygame.time.wait(10)
    
    DISPLAYSURF.blit(holeImg, holeRect)
    DISPLAYSURF.blit(clubImg, clubRect)

    if enemyAlive == True:
      ENEMYSURF.blit(enemyImg, enemyRect)

    DISPLAYSURF.blit(playerImg, playerRect)
    pygame.display.update()
    tick += 1

  pygame.mixer.music.load(youDed)
  pygame.mixer.music.play(-1)
  while not alive:
    tick = 0
    startMenuImg = pygame.transform.scale(startMenuImg, (width, height))
    DISPLAYSURF.blit(startMenuImg, (0, 0))

    drawMessage("Press G to restart", width/2, 600, 20)
    drawTitle("You Died", width/2, 300)
    for event in pygame.event.get():   
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
        alive = True
    
    pygame.display.update()
