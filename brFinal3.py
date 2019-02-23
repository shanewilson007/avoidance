import pygame
import time
import random

pygame.init()

# Colors
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
brightBlue = (0,0,255)
brightRed = (255,0,0)
brightGreen = (0,255,0)

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('A Bit Racey')
clock = pygame.time.Clock()
path = '/home/shane/programming/python/abitracey/pictures/'
# Import Images
countryImg = pygame.image.load(str(path)+'country2.jpg')
countryImg = pygame.transform.scale(countryImg,(800,600))

introImg = pygame.image.load(str(path)+'country.jpg')
introImg = pygame.transform.scale(introImg,(800,600))

carImg = pygame.image.load(str(path)+'car.png')
carImg = pygame.transform.scale(carImg,(100,160))
car_width = 100
car_height = 160

rockImg = pygame.image.load(str(path)+'rock.png')
rockImg = pygame.transform.scale(rockImg,(100,100))

treeImg = pygame.image.load(str(path)+'tree.png')
treeImg = pygame.transform.scale(treeImg,(100,100))

hs = 0 # HighScore counter
hs2 = 0 # HighSpeed counter
pause = False

def score(count):
    font = pygame.font.SysFont(None,25)
    text = font.render("Score: " + str(count), True, white)
    gameDisplay.blit(text, (0,30))

def highScore(hs):
    font = pygame.font.SysFont(None,25)
    text = font.render('Highscore: ' +str(hs), True, white)
    gameDisplay.blit(text, (0,0))

def mph(speed):
    font = pygame.font.SysFont(None,25)
    text = font.render('MPH:' + str(round(speed*4,1)), True, white)
    gameDisplay.blit(text, (600,30))

def highSpeed(hs2):
    font = pygame.font.SysFont(None,25)
    text = font.render('Highest Speed: ' +str(round(hs2,1)), True, white)
    gameDisplay.blit(text, (600,0))

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def bg(roadx,roady):
    gameDisplay.blit(countryImg,(roadx,roady))
    
def obstacle1(startx,starty):
    gameDisplay.blit(rockImg,(startx,starty))

def obstacle2(startx,starty):
    gameDisplay.blit(treeImg,(startx,starty))

def text_objects(text,font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def crash():
    pygame.mixer.music.stop()
    crashSound = pygame.mixer.Sound('crash.wav')
    crashSound.set_volume(1.0)
    pygame.mixer.Sound.play(crashSound)
    
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects('You Crashed!', largeText)
    TextRect.center = ((400),(300))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    gameLoop()

def gameIntro():
    pygame.mixer.music.load('intro.wav')
    pygame.mixer.music.play()
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(introImg,(0,0))
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects('A Bit Racey', largeText)
        TextRect.center = ((400),(300))
        gameDisplay.blit(TextSurf, TextRect)

        button('Go!',150,450,100,50, green,brightGreen,'play')
        button('Quit!',550,450,100,50,red,brightRed,'quit')
        
        pygame.display.flip()
        clock.tick(15)

def pauseScreen():
    global pause
    while pause:
        pygame.mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(introImg,(0,0))
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects('Paused', largeText)
        TextRect.center = ((400),(300))
        gameDisplay.blit(TextSurf, TextRect)

        button('Resume',150,450,100,50, green,brightGreen,'resume')
        button('Quit',550,450,100,50,red,brightRed,'quit')
        
        pygame.display.flip()
        clock.tick(15)

def button(msg,x,y,w,h,ic,ac,action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	
	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
		if click[0] == 1 and action is not None:
			if action == 'play':
				gameLoop()
			elif action == 'quit':
				pygame.quit()
				quit()
			else:
				action == 'resume'
				global pause
				pygame.mixer.music.unpause()
				pause = False
	else:
		pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
		text1 = pygame.font.Font('freesansbold.ttf',25)
		TextSurf, TextRect = text_objects(msg,text1)
		TextRect.center = (((x+100/2)), (450+(50/2)))
		gameDisplay.blit(TextSurf, TextRect)

def gameLoop():
    pygame.mixer.music.load('driving.wav')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    x = (800 * 0.45) # Car x-coordinate
    y = (600 * 0.7) # Car y-coordinate
    x_change = 0
    # Score & Highscore
    dodged = 0 
    global hs  
    # Speed & Highspeed
    speed = 3 
    global hs2 
    # Obstacle startpoints
    startx = random.randrange(0,800) 
    starty = -600
    # Background Roll
    roadx = 0
    roady = 0
    roady2 = -600
           
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                    
                if event.key == pygame.K_SPACE:
                    pygame.display.toggle_fullscreen()    
                if event.key == pygame.K_ESCAPE:
                    pygame.quit
                    quit()
                if event.key == pygame.K_p:
                    global pause
                    pause = True
                    pauseScreen()
                                                   
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x_change = 0
                if event.key == pygame.K_RIGHT:
                    x_change = 0                        
        x += x_change
        
        # Background Roll
        bg(roadx,roady)
        if roady < 600:
            roady += speed
        else:
            roady >= 600
            roady = -600
        
        bg(roadx,roady2)
        if roady2 < 600:
            roady2 += speed
        else:
            roady2 >= 600
            roady2 = -600
        
        # Obstacle selection
        if round(speed) % 2 == 1:
                obstacle1(startx,starty)
                obstacle2(startx+200,starty+150)
        else:
                obstacle2(startx,starty)
                obstacle1(startx+400,starty+300)
        starty += speed

        # Function Calls
        car(x,y)
        score(dodged)
        mph(speed)
        highScore(hs)
        highSpeed(hs2)

        # Scoring                
        if starty > 600:
            starty = -100
            startx = random.randrange(0,800)
            dodged +=300
            if dodged > hs:
                hs +=300
            speed += float(0.2)
            if speed*4 > hs2:
                hs2 = speed*4       
                       
        # Crash Events
        if x > 800 - car_width or x < 0:
            crash() 
        if y+5 < starty+90:
            if startx < x + 95 and startx + 95 > x: 
                crash()
       
        pygame.display.flip()
        clock.tick(90)


gameIntro()                    
pygame.quit()
quit()
