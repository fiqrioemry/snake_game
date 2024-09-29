import pygame, sys, time, random 

speed = 15

# windows sizing
frame_size_x = 720
frame_size_y = 480


# checking for error
check_errors = pygame.init()
if(check_errors[1] > 0) :
    print('Error' + check_errors[1])
else :
    print('Game Initialize Success')
    
    
# initialize game window
pygame.display.set_caption('snake game')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# game colors 
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
fps_controller = pygame.time.Clock()


# game effect 
eat_sound = pygame.mixer.Sound('./eating_sound.wav')

# snake square size 
square_size = 20

def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction
    direction = "RIGHT"
    head_pos = [720, 480]
    snake_body = [[720, 480]]
    food_pos = [random.randrange(1, (frame_size_x // square_size))* square_size,
                random.randrange(1,(frame_size_y // square_size)) * square_size]
    food_spawn = True
    
    score = 0
    
init_vars()

def show_score(choice, color, font, size) : 
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score :' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else :
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)

    game_window.blit(score_surface, score_rect)
    

def show_menu():
    while True:
        game_window.fill(black)
        font = pygame.font.SysFont('consolas', 50)

        title_surface = font.render('Snake Game', True, white)
        play_surface = font.render('Play', True, green)
        quit_surface = font.render('Quit', True, red)

        title_rect = title_surface.get_rect(center=(frame_size_x / 2, frame_size_y / 4))
        play_rect = play_surface.get_rect(center=(frame_size_x / 2, frame_size_y / 2))
        quit_rect = quit_surface.get_rect(center=(frame_size_x / 2, frame_size_y / 1.5))

        game_window.blit(title_surface, title_rect)
        game_window.blit(play_surface, play_rect)
        game_window.blit(quit_surface, quit_rect)

        pygame.display.update()

        # Event handling for menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  
                    return
                elif event.key == pygame.K_ESCAPE:  
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos): 
                    return
                elif quit_rect.collidepoint(event.pos):  
                    pygame.quit()
                    sys.exit()

show_menu()
    
# game loop
while True : 
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN :
            if (event.key == pygame.K_UP or event.key == ord('w') and direction != 'DOWN'):
                direction = 'UP'
            elif (event.key == pygame.K_DOWN or event.key == ord('s') and direction != 'UP') :
                direction = 'DOWN'
            elif (event.key == pygame.K_RIGHT or event.key == ord('d') and direction != 'LEFT') :
                direction = 'RIGHT'
            elif (event.key == pygame.K_LEFT or event.key == ord('a') and direction != 'RIGHT') :
                direction = 'LEFT'
                
    if direction == 'UP' :
        head_pos[1] -= square_size
    elif direction == 'DOWN' :
        head_pos[1] += square_size
    elif direction == 'LEFT' :
        head_pos[0] -= square_size
    else :
        head_pos[0] += square_size
        
    if head_pos[0] < 0 :
        head_pos[0] = frame_size_x - square_size
    elif head_pos[0] > frame_size_x - square_size :
        head_pos[0] = 0
    elif head_pos[1] < 0 :
        head_pos[1] = frame_size_y - square_size
    elif head_pos[1] > frame_size_y - square_size : 
        head_pos[1] = 0
        
    # eating apple
    snake_body.insert(0, list(head_pos))
    if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1] : 
        score += 1
        food_spawn = False
        eat_sound.play()
    else :
        snake_body.pop()
        
    # spawn food
    if not food_spawn : 
        food_pos = [random.randrange(1,(frame_size_x // square_size)) * square_size, random.randrange(1, (frame_size_y // square_size)) *square_size]
        food_spawn = True
        
    # GFX
    game_window.fill(black)
    for pos in snake_body : 
        pygame.draw.rect(game_window, green, pygame.Rect(
            pos[0] + 2, pos[1] + 2,
            square_size - 2, square_size))
    
    pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], square_size, square_size))
    
    # game over condition
    for block in snake_body[1:]  :
        if head_pos[0] == block[0] and head_pos[1] == block[1] :
            init_vars()
            
    show_score(1, white, 'consolas', 20)
    pygame.display.update()
    fps_controller.tick(speed)