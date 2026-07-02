import pygame

from board import piece_names, new_board, ctz, remove_bit

pygame.init()

# Set the fixed logical game size
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 512, 512
virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

sq = VIRTUAL_WIDTH // 8

# Set inial window size and make it resizable
window_width, window_height = 800, 800
window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

clock = pygame.time.Clock()
pygame.display.set_caption('Chess')
dt = 0

piece_images = {}
for char in piece_names:
    if char.isupper():
        filename = 'w' + char + '.png'
    else:
        filename = 'b' + char + '.png'

    piece_images[char] = pygame.image.load(f'assets/{filename}')
    piece_images[char] = pygame.transform.scale(piece_images[char], (sq, sq))

B = new_board() # Defines the initial board state

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

    for i in range(12):
        b = B[i]
        char = piece_names[i]
        image = piece_images[char]

        while b:
            square = ctz(b)
            b = remove_bit(b, square)

            col = square % 8
            row = square // 8

            x = col * sq
            y = row * sq

            virtual_screen.blit(image, (x, y))

    scaled_surface = pygame.transform.scale(virtual_screen, (board_size, board_size))

    window.blit(scaled_surface, ((window_width - board_size) / 2, (window_height - board_size) / 2))

    pygame.display.flip()
    
    dt = clock.tick(60) / 1000

pygame.quit()
