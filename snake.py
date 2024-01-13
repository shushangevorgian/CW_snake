#!/usr/bin/python3

import pygame
import time
import random
from pygame.locals import *
from pygame import mixer

pygame.init()

white = (255 , 255 , 255)
black = (0 , 0 , 0)
red = (255, 0 ,0)
orange = (255 , 165 , 0)

widht = 1080
height = 720

mixer.init()
mixer.music.load('Listen_And_Move.mp3')
mixer.music.play()

game_display = pygame.display.set_mode((widht ,height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

snake_size = 10
snake_speed = 10

message_font = pygame.font.SysFont("ubuntu" , 30)
score_font = pygame.font.SysFont("ubuntu" , 25)

def menu():
    global widht, height
    pygame.init() 
      
    res = (widht,height) 
      
    screen = pygame.display.set_mode(res) 
      
    color = (255,255,255) 
      
    color_light = (170,170,170) 
      
    color_dark = (100,100,100) 
      
    width = screen.get_width() 
      
    height = screen.get_height() 
      
    smallfont = pygame.font.SysFont('Corbel',35) 
      
    q_text = smallfont.render('quit' , True , color)   
    s_text = smallfont.render('start' , True , color) 

    while True:       
        for ev in pygame.event.get(): 
              
            if ev.type == pygame.QUIT: 
                pygame.quit() 
                  
            if ev.type == pygame.MOUSEBUTTONDOWN: 
                  
                if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
                    pygame.quit() 
                      
                if width/2 <= mouse[0] <= width/2+140 and 100 <= mouse[1] <= 100+40: 
                    run_game()

        screen.fill((60,25,60)) 
          
        mouse = pygame.mouse.get_pos() 
          
        if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
            pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
        else: 
            pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40]) 
          
        if width/2 <= mouse[0] <= width/2+140 and 100 <= mouse[1] <=100+40: 
            pygame.draw.rect(screen,color_light,[width/2,100,140,40]) 
        else: 
            pygame.draw.rect(screen,color_dark,[width/2,100,140,40]) 

        screen.blit(q_text , (width/2+50,height/2))
        screen.blit(s_text, (width/2+50, 100))
        pygame.display.update() 

def print_score(score):
    text = score_font.render("Score: " + str(score) , True , orange)
    game_display.blit(text, [0,0])

def draw_snake(snake_size , snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(game_display , white , [pixel[0] , pixel[1] , snake_size , snake_size])

def run_game():
    game_over = False
    game_close = False

    x = widht / 2
    y = height / 2

    x_speed = 0
    y_speed = 0

    snake_pixels = []
    snake_lenght=1

    target_x = round(random.randrange(0 , widht - snake_size) / 10.0) * 10.0
    target_y = round(random.randrange(0 , height - snake_size) / 10.0) * 10.0

    while not game_over:

        while game_close:
            game_display.fill(black)
            game_over_message = message_font.render("Game over" , True , red)
            game_display.blit(game_over_message , [widht/3 , height/3 ])
            print_score(snake_lenght - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_2:
                        run_game()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_speed = -snake_size
                    y_speed = 0
                if event.key == pygame.K_RIGHT:
                    x_speed = snake_size
                    y_speed = 0
                if event.key == pygame.K_UP:
                    x_speed = 0
                    y_speed = -snake_size
                if event.key == pygame.K_DOWN:
                    x_speed = 0
                    y_speed = snake_size

        #if x >= widht or x < 0 or y >= height or y < 0 :
        #    game_close = True

        if x >= widht:
            x -= widht
        elif x < 0:
            x += widht
        if y > height:
            y -= height
        elif y < 0:
            y += height

        x += x_speed
        y += y_speed

        game_display.fill(black)
        pygame.draw.rect(game_display , orange , [target_x , target_y , snake_size , snake_size])
        snake_pixels.append([x , y])
        if len(snake_pixels) > snake_lenght:
            del snake_pixels[0]

        for pixel in snake_pixels[:-1] :
            if pygame.Rect.colliderect(pygame.Rect(*pixel, snake_size, snake_size), pygame.Rect(x, y, snake_size, snake_size)):
            #if pixel == [x , y ]:
                game_close = True

        draw_snake(snake_size , snake_pixels)
        print_score(snake_lenght - 1 )
        pygame.display.update()

        if x == target_x and y == target_y :
            target_x = round(random.randrange(0 , widht - snake_size) / 10.0) * 10.0
            target_y = round(random.randrange(0 , height - snake_size) / 10.0) * 10.0
            snake_lenght += 1
        clock.tick(snake_speed)

    pygame.quit()
    quit()
#run_game()
menu()
