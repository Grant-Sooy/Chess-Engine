import pygame

pygame.init()

# Set the fixed logical game size
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 512, 512
virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

# Set inial window size and make it resizable
window_width, window_height = 800, 800
window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

clock = pygame.time.Clock()
pygame.display.set_caption('Chess')
dt = 0

# add board centering code here
sq = VIRTUAL_WIDTH / 8
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    virtual_screen.fill((50, 50, 50))
    window.fill((30, 30, 30))

    window_width, window_height = window.get_size()
    board_size = min(window_width, window_height)

    for r in range(8):
        for c in range(8):
            if (r + c) % 2 == 0:
                pygame.draw.rect(virtual_screen, (238, 220, 151), (sq * c, sq * r, sq, sq), 0)
            else:
                pygame.draw.rect(virtual_screen, (150, 77, 34), (sq * c, sq * r, sq, sq), 0)

    scaled_surface = pygame.transform.scale(virtual_screen, (board_size, board_size))

    window.blit(scaled_surface, ((window_width - board_size) / 2, (window_height - board_size) / 2))

    pygame.display.flip()
    
    dt = clock.tick(60) / 1000

pygame.quit()
