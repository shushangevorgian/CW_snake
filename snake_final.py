import pygame
import random
from pygame.locals import *
from pygame import mixer
import cv2

pygame.init()

###Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)

###Display sizes and caption
width = 1080
height = 720
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

###Music
mixer.init()
mixer.music.load("Listen_And_Move.mp3")
mixer.music.play()

##Image background
snake_bg = pygame.image.load("snake_over.png")
snake_bg = pygame.transform.scale(snake_bg, (width, height))

###Clock
clock = pygame.time.Clock()

###Snake sizes= and default speed
snake_size = 10
snake_speed = 25

###Texts fonts
message_font = pygame.font.SysFont("ubuntu", 25)
score_font = pygame.font.SysFont("ubuntu", 25)

###Video
video_frames = []
video_file = "snake_d.mp4"
video = cv2.VideoCapture(video_file)

while True:
    ret, frame = video.read()
    if not ret:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB
    frame = cv2.resize(frame, (width, height))  # Resize frame
    frame = pygame.image.frombuffer(frame.flatten(), (width, height), "RGB")
    video_frames.append(frame)
video.release()


def menu():
    # pygame.init()
    video_fps = 9  # How many frames per second should change
    video_timer = (
        0  # Stores the time that has passed before the last frame (in milliseconds)
    )
    milliseconds_per_frame = (
        1000 / video_fps
    )  # How many milliseconds does one frame last
    res = (width, height)
    screen = pygame.display.set_mode(res)
    frame_index = 0
    frame_count = len(video_frames)
    color = (255, 255, 255)
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)
    button_size = (150, 80)

    # Initializing buttons
    # "Surface" stores the button image (solid color in this case)
    # "Rect" stores the position and the size of the button
    # Start button
    button_start = pygame.Surface(button_size)
    button_start_rect = button_start.get_rect(
        center=(width // 2, height // 2 - button_size[1])
    )
    button_start.fill(color_dark)
    # Quit button
    button_quit = pygame.Surface(button_size)
    button_quit_rect = button_quit.get_rect(
        center=(width // 2, height // 2 + button_size[1])
    )
    button_quit.fill(color_dark)

    smallfont = pygame.font.SysFont("Corbel", 35)
    q_text = smallfont.render("Quit", True, color)
    s_text = smallfont.render("Start", True, color)
    while True:
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return
                ###Mouse event . Mouse positin and button position
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if button_quit_rect.collidepoint(mouse):
                    pygame.quit()
                    return
                if button_start_rect.collidepoint(mouse):
                    run_game()
                    return
        screen.blit(video_frames[frame_index], (0, 0))

        # Change button color when mouse hovers on it
        if button_start_rect.collidepoint(mouse):
            button_start.fill(color_light)
        else:
            button_start.fill(color_dark)

        if button_quit_rect.collidepoint(mouse):
            button_quit.fill(color_light)
        else:
            button_quit.fill(color_dark)

        # Draw the text on the button (centered)
        button_quit.blit(
            q_text,
            q_text.get_rect(center=(button_quit_rect.w // 2, button_quit_rect.h // 2)),
        )
        button_start.blit(
            s_text,
            s_text.get_rect(center=(button_quit_rect.w // 2, button_quit_rect.h // 2)),
        )
        # Draw buttons on the screen
        screen.blit(button_start, button_start_rect)
        screen.blit(button_quit, button_quit_rect)

        pygame.display.update()
        if video_timer >= milliseconds_per_frame:
            # How many frames have passed
            # (e.g. 1 frame time == 100 ms. If 1000ms passed after last update, 1000/100 = 10 frames will be skipped)
            frames_passed = (
                video_timer // milliseconds_per_frame * milliseconds_per_frame
            )
            # Next frame index
            frame_index = int((frame_index + frames_passed) % frame_count)
            # Update the timer
            video_timer %= milliseconds_per_frame

        # NOT Video speed (FPS=10 => this loop will work 10 times in a second.)
        # (clock.tick introduces delay if FPS is set)
        # clock.tick(10)  # Adjust as needed

        video_timer += clock.tick(60)


def print_score(score):
    text = score_font.render("Score: " + str(score), True, orange)
    game_display.blit(text, [0, 0])


def draw_snake(snake_size, snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(
            game_display, white, [pixel[0], pixel[1], snake_size, snake_size]
        )


def run_game():
    global snake_speed
    game_over = False
    game_close = False
    x = width / 2
    y = height / 2
    x_speed = 0
    y_speed = 0
    snake_pixels = []
    snake_lenght = 1
    ###Random positions for snake and food, start game time
    target_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
    target_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0
    while not game_over:
        while game_close:
            game_display.fill(black)
            game_display.blit(snake_bg, (0, 0))
            game_over_message = message_font.render("Game over", True, red)
            game_start_message = message_font.render(
                "Press 2 to restart the game",
                True,
                red,
            )
            game_quit_message = message_font.render(
                "Press 1 to quit the game", True, red
            )
            game_display.blit(game_over_message, [width / 1.5, height / 4])
            game_display.blit(game_start_message, [width / 1.5, height / 3.5])
            game_display.blit(game_quit_message, [width / 1.5, height / 3])

            print_score(snake_lenght - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_2:
                        snake_speed = 25
                        run_game()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
        ###Controlling snake
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                return
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
        if x >= width:
            x -= width
        elif x < 0:
            x += width
        if y > height:
            y -= height
        elif y < 0:
            y += height
        x += x_speed
        y += y_speed
        game_display.fill(black)
        pygame.draw.rect(
            game_display, orange, [target_x, target_y, snake_size, snake_size]
        )
        snake_pixels.append([x, y])
        if len(snake_pixels) > snake_lenght:
            del snake_pixels[0]
        for pixel in snake_pixels[:-1]:
            if pygame.Rect.colliderect(
                pygame.Rect(*pixel, snake_size, snake_size),
                pygame.Rect(x, y, snake_size, snake_size),
            ):
                game_close = True
        draw_snake(snake_size, snake_pixels)
        print_score(snake_lenght - 1)
        pygame.display.update()
        if x == target_x and y == target_y:
            target_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
            target_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0
            snake_lenght += 1
            ### Changing speed
            if (snake_lenght - 1) > 0 and (snake_lenght - 1) % 5 == 0:
                snake_speed += 5
        clock.tick(snake_speed)
    pygame.quit()
    quit()


menu()
