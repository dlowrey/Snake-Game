#Chris Marler & Dane Lowrey
#CS 1411-001
#Snake Project
#
#PROJECT DESC:
#A simple snake game made using x/y coordinate and printing blits. Complete with title screen (with multiple options), an info screen (to tell you how to play if you don't already know), and an exit function.
#
#INPUT/OUTPUT:
#Input: Different keys (Q, W, E, Up, Down, Left, Right, Y, N)
#output: (Game start, Game exit, move up, move down, move left, move right, yes (play again), no (don't play again and exit))
#
#ALGORITHM:
#import pygame, sys, random
#initiate mixer and pygame
#set colors
#Pull up the start screen menu picture and run intro snake, as well as start the intro music on infinite loop
#Take key inputs (q,w,e - start, info, exit)
#If E, exit
#If W, show game info
#If in game info, push Q to start a game, E to exit, or M to return to main menu
#If Q start main game funciton
#start game music on infinite loop
#Start snake movements using a coordinate system that prints and deletes blits depending on the length of the list(s) of coords (x and y)
#Take key inputs to determine snake movement. Do not allow snake to move the opposite direction that it is currently traveling.
#If snake collides with something return a true value
#if collides with food, append one x/y coordinate pair to your lists and add +1 to score
#if collide with self, run the end/continu function
#if collide with boundary, run the end/continu function
#If end score is greater than current high score: update the high score
#Ask user if they would like to play again (Yes, no, or main menu)
#Either end program, start new game, or go to main menu
#
#MODULES NEEDED:
#Pygame
#Sys
#Random
#
#FILES NEEDED:
#This file
#Snake_Music1.mp3
#Snake_Music2.mp3
#high_score.txt
#
#SOURCES:
#http://stackoverflow.com/questions/2936914/pygame-sounds-dont-play
#http://stackoverflow.com/questions/14845896/pygame-cannot-open-sound-file
#http://www.nosoapradio.us/
#https://www.youtube.com/watch?v=Y7joZ67mC6o&list=PLQVvvaa0QuDcxG_Cajz1JyTH6eAvka93C
#pygame.org
#http://programarcadegames.com/python_examples/show_file.php?file=high_score.py
#http://www.pygame.org/project-pySnake-2486-.html
#http://www.pygame.org/project-Snake+in+35+lines-818-.html
#http://www.pygame.org/tags/snake
#https://docs.python.org/3.4


#Import pygame, sys, and random
import pygame, sys, random
#Import everything from pygame
from pygame.locals import *
#pre init mixer settings
pygame.mixer.pre_init(44100, 16, 2, 4096)
#initiate pygame
pygame.init()
#initiate mixer
pygame.mixer.init()

#Colors (Won't need them all, but it's nice to have a reference :] )
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,175,0)
blue = (0,0,255)
yellow = (0,255,255)
orange = (255,255,0)
purple = (255,0,255)
blue2 = (10,0,100,10)
silver = (180,180,180)

#Start menu music function
def start_music():
    #import mp3 file
    pygame.mixer.music.load("Snake_Music2.mp3")
    #play file on infinite loop
    pygame.mixer.music.play(-1)
                            
    
#Game music function
def game_music():
    #import mp3 file
    pygame.mixer.music.load("Snake_Music.mp3")
    #play file on infinite loop
    pygame.mixer.music.play(-1)




#Continue function
def continu():
    #set continue screen display
    cont = pygame.display.set_mode((750,750))
    #fill w/ color
    cont.fill(white)
    #select font
    cont_font = pygame.font.SysFont('Times New Roman', 50)
    m_font = pygame.font.SysFont('Times New Roman', 20)
    #render the message
    cont_rend = cont_font.render('Play again? (Y/N)', True, red)
    m_rend = m_font.render('Press M To Return To Main Menu', True, red)
    #print the message to screen at given coords
    cont.blit(cont_rend, (200,260))
    cont.blit(m_rend, (235,500))
    #update display
    pygame.display.update()
    #while true
    while True:
        #detect events (specifically key presses)
        for event4 in pygame.event.get():
            #if they push the X, then quit
            if event4.type == QUIT:
                pygame.quit()
                sys.exit()
            #if they push down one of the following keys then do the task that relates to that key
            elif event4.type == KEYDOWN:
                #if yes
                if event4.key == K_y:
                    #start new game
                    main_game()
                elif event4.key == K_m:
                    pygame.mixer.music.fadeout(800)
                    pygame.time.wait(1000)
                    start_screen()
                #if no
                elif event4.key == K_n:
                    #say goodbye and exit game
                    cont.fill(silver)
                    bye_font = pygame.font.SysFont('Times New Roman', 80)
                    bye = bye_font.render('G O O D B Y E!', True, red)
                    cont.blit(bye, (100,280))
                    pygame.display.update()
                    pygame.mixer.music.fadeout(1400)
                    pygame.time.wait(1500)
                    pygame.quit()
                    sys.exit()
                    

#snake_Hx is the x coordinate of snakes head. snfd_Ex will be the end of the snake (x coordinate of tail.. to check if the snake collided with its tail) OR it is the x
#coordinate of the food (to check if the snake collides with the food). snake_Hy is the y coordinate of the snakes head. snfd_Ey is the y coordinate of the end of the snake or
#the y coordinate of where the food is (again helps to checck if the snake collides with the food or if it collides with its tail). w-h1 are the hitbox width and height. they will be 20, so that when the
#snake collides with himself, he will properly hit himeself and the game will end. If less, the snake can travel through himself. If more, the snake
#can barely move anywhere without the game ending. w1 and h1 will also be changed to 10 at some points (redefines the hitbox for the food), so that the snake can actually eat the food when he collides with them. Too small
#and he passes right through because the hitbox is too small. Too big and he magically ingests food just by being within a mile of it, because the hitbox is huge. 
def snake_collision(snake_Hx, snfd_Ex, snake_Hy, snfd_Ey, w, w1, h, h1):
    #If the snake hits its tail or some food, then return true (and end the game or collect the food, depending on situation)
    #
    #This function basically creates a range, and if the snakes front piece gets in a certain range of either the snakes tail or a piece of food, it will return true (and either end the game or pick up the food)
    if snake_Hx+w > snfd_Ex and snake_Hx < snfd_Ex+w1 and snake_Hy+h > snfd_Ey and snake_Hy < snfd_Ey+h1:
        return True
    else:
        return False
#When game ends, show score screen
def end(screen, score):
    #set font
    font1 = pygame.font.SysFont('Times New Roman', 50)
    #tell user the score they achieved
    score_render = font1.render('Your score was: '+str(score), True, red)
    file = open("high_score.txt", "r")
    high_score = int(file.read())
    file.close()
    if score > high_score:
        hs_ = font1.render('NEW HIGH SCORE!', True, red)
        screen.blit(hs_, (150, 350))
        file = open("high_score.txt", "w")
        file.write(str(score))
        file.close()
    screen.blit(score_render, (180, 200))
    pygame.display.update()
    pygame.time.wait(3000)
    continu()

    


def main_game():
    #Start music
    game_music()
    #The following two lines are the x/y coordinates for the snakes starting postion. The snake starts with
    #7 pieces (number of x/y coordinate pairs)
    x_coords = [315, 315, 315, 315, 315, 315, 315]
    y_coords = [315, 295, 275, 255, 235, 215, 205]
    
    #The starting direction is down
    direc = 0
    #Score starts at 0 and will increase depending on how much food the player picks up.
    score = 0
    #Create the image for food
    food_img = pygame.Surface((12, 12))
    #set color for food (blue)
    food_img.fill((0, 0, 128))
    #Spawn the first food within coordinate range of (10-590,10-590)
    food_pos = (random.randint(10, 730), random.randint(10, 730))
    #create the games screen
    game_screen = pygame.display.set_mode((750, 750))
    #color the screen
    game_screen.fill(silver)
    #Names program
    pygame.display.set_caption('SNAKE_GAME_V1.0')
    #set image for snake
    snake = pygame.Surface((14, 14))
    #set color for snake (green, of course)
    snake.fill(green)
    #set font for score board
    font3 = pygame.font.SysFont('Times New Roman', 20)
    #start clock
    clock = pygame.time.Clock()
    #Set boolean
    done = False


    #While not done with the game
    while not done:
        #set the clock
        clock.tick(15)
        #detect event types
        for event in pygame.event.get():
            #if they push the X, then quit
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            #if they push down one of the following keys then set the direction to the corresponding keys direction
            elif event.type == KEYDOWN:
                if event.key == K_DOWN and direc != 2:
                    direc = 0
                elif event.key == K_UP and direc != 0:
                    direc = 2
                elif event.key == K_RIGHT and direc != 3:
                    direc = 1
                elif event.key == K_LEFT and direc != 1:
                    direc = 3
        #length of snake body
        snake_length = (len(x_coords)-1)
        #if the snake is actually long enough to hit itself (5 or more and it starts at 7), then...
        while snake_length >=5:
            #if it hits itself, smite it down like the vermin it is :)
            if snake_collision(x_coords[0], x_coords[snake_length], y_coords[0], y_coords[snake_length], 20, 20, 20, 20):
                end(game_screen,score)
            #Subtract one from the snakes length
            snake_length -=1
            
        #If the snake collides with some food...
        if snake_collision(x_coords[0], food_pos[0], y_coords[0], food_pos[1], 20, 10, 20, 10):
            #add one to the score
            score += 1
            #increase the snakes size by adding another x/y coordinate to the lists. Number does not matter, because
            #now all you want is another x/y coordinate, while before you wanted the starting coordinates on the screen
            x_coords.append(315)
            y_coords.append(315)
            #spawn new food on screen
            food_pos = (random.randint(10, 730), random.randint(10, 730))
        #If the snake collides with a screen boundary, then end the game.
        if x_coords[0] < 0 or x_coords[0] > 730 or y_coords[0] < 0 or y_coords[0] > 730:
            end(game_screen, score)
        #length of snake body
        snake_length = (len(x_coords)-1)
        #While the snake body is longer than 1, make sure that the snakes tail pieces actually follow it.
        while snake_length >= 1:
            x_coords[snake_length] = x_coords[snake_length-1]
            y_coords[snake_length] = y_coords[snake_length-1]
            snake_length -= 1
        #Change direction of snake depending on input from user (the user changed direc w/ input)
        if direc == 0:
            y_coords[0] += 20
        elif direc == 2:
            y_coords[0] -= 20
        elif direc == 3:
            x_coords[0] -= 20
        elif direc == 1:
            x_coords[0] += 20
        #refill screen with color so there isnt a trail following the snake other than its tail
        game_screen.fill(silver)
        #print the snake to the screen
        for snake_length in range(0, len(x_coords)):
            game_screen.blit(snake, (x_coords[snake_length], y_coords[snake_length]))
        #Print the food to the screen
        game_screen.blit(food_img, food_pos)
        #Print the score to the screen
        score_render = font3.render(str(score), True, (0,0,0))
        game_screen.blit(score_render, (10,10))
        #update pygame display
        pygame.display.update()
    



#Game start screen
def start_screen():
    #Start the start screen music :D
    start_music()
    #make display
    start = pygame.display.set_mode((750,750))
    #fill background color
    start.fill(silver)
    #create and render title/instructions
    font4 = pygame.font.SysFont('Times New Roman', 50)
    font5 = pygame.font.SysFont('Times New Roman', 20)
    font6 = pygame.font.SysFont('Times New Roman', 16)
    Title = font4.render('S N A K E', True, red)
    play = font5.render('Press Q to start, W for game info, or E to exit', True, red)
    names = font6.render('By Chris Marler and Dane Lowrey',True,black)
    start.blit(Title, (265,280))
    start.blit(play, (200,340))
    start.blit(names,(263,450))
    filler = pygame.Surface((14, 14))
    filler.fill(silver)
    #set image for snake2
    snake2 = pygame.Surface((14, 14))
    #set color for snake2 (green again)
    snake2.fill(green)
    #starting x-coordinate for snakes on intro screen
    x = 750
    #ending x coordinate for snakes
    x2 = 0
    #a counter
    loop = 0
    #update screen so that it shows the title and options
    pygame.display.update()
    #wait so that the snakes don't immediately start going across the screen
    pygame.time.wait(500)
    while True:
        #If x is less than or equal to -101 (-101 to allow my filler to fill in the final 5 snake2 blitz), then break 
        if x <= x2-101:
            break
        #otherwise, print 5 snake2 blits and add one to the left every 30ms. at the same time delete one from the right every 30s. This creates my illusion of motion.
        else:
            
            start.blit(snake2, (x,600))
            pygame.time.wait(30)
            x -= 20
            loop += 1
            pygame.display.update()
            
            if loop >= 5:
                start.blit(filler, (x+120, 600))
                pygame.time.wait(30)
                pygame.display.update()
            elif loop >= 10:
                start.blit(filler, (x+120, 600))
                pygame.time.wait(30)
                pygame.display.update()
    #Fill the stubborn final snake2 blit
    start.blit(filler, (0,600))
    
    #Same as above, except y coordinate is moved up and the snake is now traveling from left ot right.
    pygame.time.wait(40)
    x3 = 0
    x4 = 750
    loop2 = 0
    while True:
        if x3 >= x4+101:
            break
        else:
            
            start.blit(snake2, (x3,400))
            pygame.time.wait(30)
            x3 += 20
            loop2 += 1
            pygame.display.update()
            
            if loop2 >= 5:
                start.blit(filler, (x3-120, 400))
                pygame.time.wait(30)
                pygame.display.update()
            elif loop2 >= 10:
                start.blit(filler, (x3-120, 400))
                pygame.time.wait(30)
                pygame.display.update()
    start.blit(filler, (750,460))
            


    while True:
        

        for event3 in pygame.event.get():
            #if they push the X, then quit
            if event3.type == QUIT:
                pygame.quit()
                sys.exit(0)
            #if they push down one of the following keys then do the task relate to that key
            elif event3.type == KEYDOWN:
                #if q is pressed start the game
                if event3.key == K_q:
                    pygame.mixer.music.fadeout(800)
                    pygame.time.wait(1000)
                    main_game()
                    pygame.display.update()
                #if w is pressed show game info (instructions/High score) screen
                elif event3.key == K_w:
                    file = open("high_score.txt", "r")
                    score = int(file.read())
                    file.close()
                    start.fill(silver)
                    info_font = pygame.font.SysFont('Times New Roman', 20)
                    info_title_font = pygame.font.SysFont('Times New Roman', 50)
                    info_title = info_title_font.render('I N S T R U C T I O N S', True, red)
                    info1 = info_font.render('- Use the arrow keys to move the snake.', True, red)
                    info2 = info_font.render('- Your goal is to eat food and grow without hitting yourself or a boundary.', True, red)
                    info3 = info_font.render('- Press Q to start a game, E to exit, or M to return to the main menu.', True, red)
                    HS_info = info_font.render('Current High Score: '+str(score), True, red)
                    start.blit(info_title, (10,10))
                    start.blit(info1, (10,100))
                    start.blit(info2, (10,170))
                    start.blit(info3, (10,240))
                    start.blit(HS_info, (280,680))
                    pygame.display.update()
                #if e is pressed, quit pygame and exit game
                elif event3.key == K_e:
                    start.fill(silver)
                    bye_font = pygame.font.SysFont('Times New Roman', 80)
                    bye = bye_font.render('G O O D B Y E!', True, red)
                    start.blit(bye, (100,280))
                    pygame.display.update()
                    pygame.mixer.music.fadeout(2800)
                    pygame.time.wait(3000)
                    pygame.quit()
                    sys.exit()
                elif event3.key == K_m:
                    start_screen()
            
            
        pygame.display.update()



start_screen()
