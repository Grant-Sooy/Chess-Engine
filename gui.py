import pygame

pygame.init()

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Chess')

run = True
while run:
    pygame.time.delay(60)

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run = False

pygame.quit()
