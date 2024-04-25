#libraries
import sys
import pygame
from pygame.locals import QUIT
from random import randint as randint
from BGmap import BGmap
pygame.init()

#variables
DISPLAYSURF = pygame.display.set_mode((0,0), pygame.RESIZABLE)
ENEMYSURF = pygame.display.set_mode((0,0), pygame.RESIZABLE)
BGSURF = pygame.display.set_mode((0,0), pygame.RESIZABLE)

width = DISPLAYSURF.get_width()
height = DISPLAYSURF.get_height()
transparent = (0, 0, 0, 100)
darkGray = (20, 20, 20, 0)
darkGreen = (15, 55, 10, 0)
terrains = ["fairway", "rough", "green", "water", "bunker", "hole", "teebox"]

started = 0

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
level = 1
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

SandImgPath = "samd.png"
SandImg = pygame.image.load(SandImgPath).convert_alpha()

ballImgPath = "ball.png"
ballImg = pygame.image.load(ballImgPath).convert_alpha()
ballRect = ballImg.get_rect()
ballAlive = False
ballSpeed = 3, 3
ballMovementSpeed = 5
ballRandomness = 1
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

bossImgPath = "boss.png"
bossImg = pygame.image.load(bossImgPath).convert_alpha()
bossRect = bossImg.get_rect()
bossLives = 20
bossSpeed = 3

bossStoneLeftImgPath = "stone.png"
bossStoneLeftImg = pygame.image.load(bossStoneLeftImgPath).convert_alpha()
bossStoneLeftRect = bossStoneLeftImg.get_rect()

bossStoneRightImg = pygame.image.load(bossStoneLeftImgPath).convert_alpha()
bossStoneRightRect = bossStoneRightImg.get_rect()

bossStoneUpImg = pygame.image.load(bossStoneLeftImgPath).convert_alpha()
bossStoneUpRect = bossStoneUpImg.get_rect()

bossStoneDownImg = pygame.image.load(bossStoneLeftImgPath).convert_alpha()
bossStoneDownRect = bossStoneDownImg.get_rect()





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
  global clubWait
  global shot

  funcReturn = False

  if input[pygame.K_UP] and playerRect.y >= speed:
    playerRect.y -= speed
    funcReturn = True
  if input[pygame.K_DOWN] and playerRect.y <= (height - speed - playerImg.get_height()):
    playerRect.y += speed
    funcReturn =  True
  if input[pygame.K_RIGHT] and playerRect.x <= (width - speed - playerImg.get_width()):
    playerRect.x += speed
    funcReturn =  True
  if input[pygame.K_LEFT] and playerRect.x >= speed:
    playerRect.x -= speed
    funcReturn =  True
  if input[pygame.K_d] and not ballAlive and amountOfBalls > 0:
    spawnBallMovingRight()
    amountOfBalls = amountOfBalls - 1
    shot = True
  if input[pygame.K_a] and not ballAlive and amountOfBalls > 0:
    spawnBallMovingLeft()
    amountOfBalls = amountOfBalls - 1
    shot = True
  if input[pygame.K_s] and not ballAlive and amountOfBalls > 0:
    spawnBallMovingDown()
    amountOfBalls = amountOfBalls - 1
    shot = True
  if input[pygame.K_w] and not ballAlive and amountOfBalls > 0:
    spawnBallMovingUp()
    amountOfBalls = amountOfBalls - 1
    shot = True
  
  return funcReturn

def switchClub(input):
  global ballMovementSpeed
  global ballRandomness
  global clubClock
  global clubImg
  global clubSelected
  global clubWait

  if input[pygame.K_q] and not clubWait:
    if clubSelected == 0:
      clubSelected = 2
      ballMovementSpeed = 2
      ballRandomness = 0
      clubImg = pygame.image.load(clubImgPaths[clubSelected]).convert_alpha()
      clubClock = 0
      clubWait = True
    elif clubSelected == 1:
      clubSelected = 0
      ballMovementSpeed = 5
      ballRandomness = 2
      clubImg = pygame.image.load(clubImgPaths[clubSelected]).convert_alpha()
      clubClock = 0
      clubWait = True
    elif clubSelected == 2:
      clubSelected = 1
      ballMovementSpeed = 7
      ballRandomness = 4
      clubImg = pygame.image.load(clubImgPaths[clubSelected]).convert_alpha()
      clubClock = 0
      clubWait = True
    return True
  if input[pygame.K_e] and not clubWait:
    if clubSelected == 0:
      clubSelected = 1
      ballMovementSpeed = 7
      ballRandomness = 4
      clubImg = pygame.image.load(clubImgPaths[clubSelected]).convert_alpha()
      clubClock = 0
      clubWait = True
    elif clubSelected == 1:
      clubSelected = 2
      ballMovementSpeed = 2
      ballRandomness = 0
      clubImg = pygame.image.load(clubImgPaths[clubSelected]).convert_alpha()
      clubClock = 0
      clubWait = True
    elif clubSelected == 2:
      clubSelected = 0
      ballMovementSpeed = 5
      ballRandomness = 2
      clubImg = pygame.image.load(clubImgPaths[clubSelected]).convert_alpha()
      clubClock = 0
      clubWait = True
    return True

def spawnBallMovingRight():
  global ballAlive
  global ballSpeed

  ballAlive = True
  ballRect.x, ballRect.y = playerRect.x + 5, playerRect.y + 40
  ballSpeed = ballMovementSpeed, randint(-ballRandomness, ballRandomness)/10

def spawnBallMovingLeft():
  global ballAlive
  global ballSpeed

  ballAlive = True
  ballRect.x, ballRect.y = playerRect.x - 5, playerRect.y + 40
  ballSpeed = -ballMovementSpeed, randint(-ballRandomness, ballRandomness)/10

def spawnBallMovingUp():
  global ballAlive
  global ballSpeed

  ballAlive = True
  ballRect.x, ballRect.y = playerRect.x, playerRect.y
  ballSpeed = randint(-ballRandomness, ballRandomness)/10, -ballMovementSpeed

def spawnBallMovingDown():
  global ballAlive
  global ballSpeed

  ballAlive = True
  ballRect.x, ballRect.y = playerRect.x, playerRect.y + 20
  ballSpeed = randint(-ballRandomness, ballRandomness)/10, ballMovementSpeed

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
      elif BGimgCode == 4:
        BGimg = SandImg
      elif BGimgCode == 5:
        BGimg = WaterImg
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
while started == 0:

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
      started = 1
      print("Main started")
      pygame.mixer.music.stop()
      pygame.mixer.music.unload()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
      started = 2
      print("Tutorial started")
      
  pygame.display.update()
  tick += 1


drawBG(0, 0, width, height)
pygame.mixer.music.load(gameMusic)
pygame.mixer.music.play(-1)
moved = False
shot = False
switched = False
ballDispenserAlive = False
ballMachineRect.x = width - 100
ballMachineRect.y = 0
enemyAlive = False
ballsReplenishd = False
enemyKilled = False
holeRect = pygame.Rect(holeSpriteRect.x, holeSpriteRect.y + 75, 45, 25)
while started == 2:
  drawBG(0, 0, width, height)

  for event in pygame.event.get():   
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
      pygame.quit()
      sys.exit()
  keypress = pygame.key.get_pressed()
  
  if move(keypress):
    moved = True
  if switchClub(keypress):
    switched = True


  if not moved:
    drawMessage("Use arrow keys to move", width/2, height/2, 80)
  elif moved and not shot:
    drawMessage("Use WASD to shoot", width/2, height/2, 80)
  elif shot and not switched:
    drawMessage("Switch clubs with Q or E", width/2, height/2 - 50, 80)
    drawMessage("Faster clubs are less accurate", width/2, height/2 + 50, 80)
  elif switched and amountOfBalls > 0 and not ballDispenserAlive:
    drawMessage("You have " + str(amountOfBalls) + " balls", width/2, height/2, 80)
    drawMessage("try to use them all", width/2, height/2 + 100, 80)
  elif amountOfBalls == 0 and not enemyKilled:
    drawMessage("To replenish your balls", width/2, height/2 - 100, 80)
    drawMessage("walk over the ball dispenser", width/2, height/2, 80)
    drawMessage("in the top right", width/2, height/2 + 100, 80)
    ballDispenserAlive = True
  elif ballDispenserAlive and ballsReplenishd and not enemyKilled:
    drawMessage("Shoot the enemy to kill them", width/2, height/2, 80)
    drawMessage("but don't touch the enemy", width/2, height/2 + 100, 80)
    enemyAlive = True
  elif enemyKilled:
    drawMessage("When all enemies are dead", width/2, height/2 -100, 80)
    drawMessage("shoot in the hole", width/2, height/2, 80)
    drawMessage("to advance to the next wave", width/2, height/2 + 100, 80)
    



  if ballAlive and ballRect.x < width and ballRect.y < height and ballRect.x > 0 and ballRect.y > 0:
    ballRect.x += ballSpeed[0]
    ballRect.y += ballSpeed[1]
    DISPLAYSURF.blit (ballImg, ballRect)
  elif ballAlive and (ballRect.x >= width or ballRect.y >= height or ballRect.x <= 0 or ballRect.y <= 0):
    ballAlive = False

  drawMessage("Balls: " + str(amountOfBalls), width - 100, height - 50, 30)

  if clubWait and clubClock <= 10:
      clubClock += 1
  elif clubClock > 10:
    clubWait = False

  if playerRect.colliderect(ballMachineRect):
    amountOfBalls = 5
    ballsReplenishd = True

  if ballRect.colliderect(enemyRect) and enemyAlive:
    enemyAlive = False
    enemyKilled = True
    ballAlive = False

  if ballRect.colliderect(holeRect) and enemyKilled:
    started = 1
    print("Main started")

  pygame.draw.rect(DISPLAYSURF, darkGreen, clubBGRect)
  DISPLAYSURF.blit(clubImg, clubRect)

  DISPLAYSURF.blit(playerImg, playerRect)

  if enemyKilled:
    DISPLAYSURF.blit(holeImg, holeSpriteRect)

  if enemyAlive:
    DISPLAYSURF.blit(enemyImg,enemyRect)

  if ballDispenserAlive:
    DISPLAYSURF.blit(ballMachineimg, ballMachineRect)

  if ballAlive: 
    DISPLAYSURF.blit(ballImg, ballRect)

  pygame.time.wait(10)
  pygame.display.update()




while started == 1:
  enemyRect.y = randint(0, height)
  enemyRect.x = randint(0, width)
  holeSpriteRect.x = 1200
  holeSpriteRect.y = height/2
  holeRect = pygame.Rect(holeSpriteRect.x, holeSpriteRect.y + 75, 45, 25)
  playerRect.y = 0
  playerRect.x = 0
  enemyAlive = True
  level = 1
  oldManRect.x = randint(0, width)
  oldManRect.y = randint(0, height)
  oldManAlive = True
  ballMachineRect.x = width - 100
  ballMachineRect.y = 0
  ballClock = 0
  golfKarAlive = True
  golfKarRect.x = randint(0, width)
  golfKarRect.y = randint(0, height)
  golfKarLives = 5
  amountOfBalls = 5
  clubWait = False
  clubClock = 0
  enemyLives = 1
  oldManLives = 1
  enemyMaxLives = 1
  oldManMaxLives = 1
  golfKarMaxLives = 5
  bossAlive = False
  leveledUp = True
  dead = False
  pygame.mixer.music.load(gameMusic)
  pygame.mixer.music.play(-1)

  while alive:
    drawBG(0, 0, width, height)
    keypress = pygame.key.get_pressed()
    move(keypress)
    switchClub(keypress)

    if enemyRect.x > width - enemyImg.get_width():
      enemyRect.x = 0
      enemyRect.y = randint(0, height)

    for event in pygame.event.get():   
      if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()      

    if (playerRect.colliderect(enemyRect) and enemyAlive) or (playerRect.colliderect(oldManRect) and oldManAlive) or (playerRect.colliderect(golfKarRect) and golfKarAlive) or (playerRect.colliderect(bossRect) and bossAlive):
      alive = False
      dead = True
      print("You died")
    elif ballRect.colliderect(holeRect) and not enemyAlive and not oldManAlive and not golfKarAlive and not bossAlive:
      level += 1
      print("Progressing to level", level)
      leveledUp = False
      ballAlive = False
      enemyAlive = True
      golfKarAlive = True
      oldManAlive = True
      golfKarRect.x = randint(0, width)
      golfKarRect.y = randint(0, height)
      oldManRect.x = randint(0, width)
      oldManRect.y = randint(0, height)
      enemyRect.x = randint(0, width)
      enemyRect.y = randint(0, height)
      golfKarLives = golfKarMaxLives
      enemyLives = enemyMaxLives
      oldManLives = oldManMaxLives

    elif ballRect.colliderect(enemyRect) and enemyAlive and ballAlive:
      ballAlive = False
      enemyLives = enemyLives - 1
    elif ballRect.colliderect(oldManRect) and oldManAlive and ballAlive:
      ballAlive = False
      oldManLives = oldManLives - 1
    elif ballRect.colliderect(golfKarRect) and golfKarAlive and ballAlive:
      golfKarLives = golfKarLives - 1
      ballAlive = False
    elif ballRect.colliderect(bossRect) and bossAlive and ballAlive:
      bossLives = bossLives - 1
      ballAlive = False


    if golfKarLives == 0:
      golfKarAlive = False
    if oldManLives == 0:
      oldManAlive = False
    if enemyLives == 0:
      enemyAlive = False
    if bossLives == 0:
      bossAlive = False


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
      drawMessage("You got new ballz!", width/2, height/5, 90)

    drawMessage("Balls: " + str(amountOfBalls), width - 80, height - 30, 30)
    if level < 9:
      drawMessage("Wave: " + str(level), width - 80, height - 60, 30)
    else:
      drawMessage("Bossfight", width - 80, height - 60, 30)


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

    if golfKarRect.y > playerRect.y + 30:
      golfKarRect.y -= golfKarSpeed
    if golfKarRect.y < playerRect.y + 30:
      golfKarRect.y += golfKarSpeed

    if bossRect.x > playerRect.x:
      bossRect.x = bossRect.x - bossSpeed
    if bossRect.x < playerRect.x:
      bossRect.x = bossRect.x + bossSpeed

    if bossRect.y > playerRect.y:
      bossRect.y -= bossSpeed
    if bossRect.y < bossRect.y:
      bossRect.y += bossSpeed

    if level == 2 and not leveledUp:
      enemySpeed = enemySpeed + 1
      oldManSpeed = oldManSpeed + 1
      leveledUp = True
      golfKarLives = golfKarMaxLives
      enemyLives = enemyMaxLives
      oldManLives = oldManMaxLives
    if level == 3 and not leveledUp:
      oldManMaxLives = 2
      enemySpeed = enemySpeed + 1
      leveledUp = True
      golfKarLives = golfKarMaxLives
      enemyLives = enemyMaxLives
      oldManLives = oldManMaxLives
    if level == 4 and not leveledUp:
      oldManSpeed = oldManSpeed + 1
      golfKarMaxLives = 6
      leveledUp = True
      golfKarLives = golfKarMaxLives
      enemyLives = enemyMaxLives
      oldManLives = oldManMaxLives
    if level == 5 and not leveledUp:
      enemyMaxLives = 2
      enemySpeed = enemySpeed + 1
      leveledUp = True
      golfKarLives = golfKarMaxLives
      enemyLives = enemyMaxLives
      oldManLives = oldManMaxLives
    if level == 6 and not leveledUp:
      oldManSpeed = oldManSpeed + 1
      golfKarSpeed = golfKarSpeed + 1
      speed = speed + 1
      leveledUp = True
      golfKarLives = golfKarMaxLives
      enemyLives = enemyMaxLives
      oldManLives = oldManMaxLives
    if level == 7 and not leveledUp:
      golfKarMaxLives = 7
      enemyMaxLives = 3
      leveledUp = True
      golfKarLives = golfKarMaxLives
      enemyLives = enemyMaxLives
      oldManLives = oldManMaxLives
    if level == 8 and not leveledUp:
      enemyMaxLives = 4
      oldManMaxLives = 3
      leveledUp = True
      golfKarLives = golfKarMaxLives
      enemyLives = enemyMaxLives
      oldManLives = oldManMaxLives
    if level == 9 and not leveledUp:
      golfKarAlive = False
      enemyAlive = False
      oldManAlive = False
      bossAlive = True
    if level == 10 and not leveledUp:
      alive = False
      dead = False
    

    
    if clubWait and clubClock <= 10:
      clubClock += 1
    elif clubClock > 10:
      clubWait = False

    if amountOfBalls == 0:
      drawMessage("You got no ballz!", width/2, height/6, 50)
    pygame.time.wait(10)

    DISPLAYSURF.blit(ballMachineimg, ballMachineRect)

    if golfKarAlive:
      DISPLAYSURF.blit(golfKarImg, golfKarRect)

    if oldManAlive:
      ENEMYSURF.blit(oldManImg, oldManRect)

    if not oldManAlive and not enemyAlive and not golfKarAlive and not bossAlive:
      DISPLAYSURF.blit(holeImg, holeSpriteRect)
    
    if bossAlive:
      DISPLAYSURF.blit(bossImg, bossRect)
    
    pygame.draw.rect(DISPLAYSURF, darkGreen, clubBGRect)
    DISPLAYSURF.blit(clubImg, clubRect)

    if enemyAlive:
      ENEMYSURF.blit(enemyImg, enemyRect)

    DISPLAYSURF.blit(playerImg, playerRect)

    pygame.time.wait(10)
    pygame.display.update()
    tick += 1


  
  while not alive:
    ballAlive = False
    enemyAlive = False
    oldManAlive = False
    golfKarAlive = False
    pygame.mixer.music.load(youDed)
    pygame.mixer.music.play(-1)
    printed = False

    while not dead and not alive:
      tick = 0
      DISPLAYSURF.fill(transparent)
      DISPLAYSURF.blit(startMenuImg, (0, 0))
      if not printed:
        print("YAY, you won!\nNot bad, not bad at all!")
        printed = True
      startMenuImg = pygame.transform.scale(startMenuImg, (width, height))

      drawMessage("Press space to restart", width/2, 600, 30)
      drawTitle("You Won!", width/2, 300)
      for event in pygame.event.get():   
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
          started = 0
          level = 1
          alive = True
          dead = False
          enemyLives = enemyMaxLives
          enemyAlive = True
          oldManLives = oldManMaxLives
          oldManAlive = True
          golfKarLives = golfKarMaxLives
          golfKarAlive = True
          DISPLAYSURF.fill(transparent)
      

      pygame.display.update()

    while dead:
      tick = 0
      DISPLAYSURF.fill(transparent)
      startMenuImg = pygame.transform.scale(startMenuImg, (width, height))
      DISPLAYSURF.blit(startMenuImg, (0, 0))

      drawMessage("Press space to restart", width/2, 600, 30)
      drawTitle("You Died", width/2, 300)
      for event in pygame.event.get():   
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
          print("RESTARTING!! Good luck!")
          playerRect.x, playerRect.y = (width + playerRect.width/2), (height + playerRect.width)/2
          alive = True
          dead = False
          enemyLives = enemyMaxLives
          enemyAlive = True
          oldManLives = oldManMaxLives
          oldManAlive = True
          golfKarLives = golfKarMaxLives
          golfKarAlive = True
      
      pygame.display.update()
