import pygame 

def moving_ball():

    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    running = True
    x, y = 50, 50
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (255, 0, 0), (x, y), 25)

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and y - 20 >= 25 : y -= 20
        if pressed[pygame.K_DOWN] and y + 20 <= 775: y += 20
        if pressed[pygame.K_LEFT] and x - 20 >= 25: x -= 20
        if pressed[pygame.K_RIGHT] and x + 20 <= 775: x += 20
        
        
        pygame.display.flip()
        clock.tick(20)
