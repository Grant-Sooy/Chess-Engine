import pygame

import board

#--------------------------------------------------------------------------------
# PYGAME INITIALIZATION AND TIME KEEPING
#--------------------------------------------------------------------------------

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Chess')
dt = 0

#--------------------------------------------------------------------------------
# DEFINING THE VIRTUAL WINDOW AND THE OS WINDOW
#--------------------------------------------------------------------------------

# Set the fixed logical game size
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 512, 512
virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

virtual_sq = VIRTUAL_WIDTH // 8

# Set inial window size and make it resizable
window_width, window_height = 800, 800
window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

#--------------------------------------------------------------------------------
# GATHERING THE PIECE IMAGES AND INITIAL BOARD STATE
#--------------------------------------------------------------------------------

piece_images = {}
for char in board.piece_names:
    if char.isupper():
        filename = 'w' + char + '.png'
    else:
        filename = 'b' + char + '.png'

    piece_images[char] = pygame.image.load(f'assets/{filename}')
    piece_images[char] = pygame.transform.scale(piece_images[char], (virtual_sq, virtual_sq))

B = board.new_board() # Defines the initial board state

selected_square = None
selected_piece = None

#--------------------------------------------------------------------------------
# BEGIN GAME LOOP
#--------------------------------------------------------------------------------

run = True
while run:

    window_width, window_height = window.get_size()
    board_size = min(window_width, window_height)
    window_sq = board_size / 8
    x_offset = (window_width - board_size) / 2
    y_offset = (window_height - board_size) / 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                col = int((mouse_x - x_offset) // window_sq)
                row = int((mouse_y - y_offset) // window_sq)
                print(row,col)
                square = row * 8 + col
                if selected_square is None:
                    if board.get_bit(B[board.all_boards], square) == 1:
                        selected_square = square
                        selected_piece = board.get_piece_at(B, square)
                else:
                    B[selected_piece] = board.set_bit(B[selected_piece], square)
                    B[selected_piece] = board.remove_bit(B[selected_piece], selected_square)
                    board.update_bitboards(B)
                    selected_square = None
                    selected_piece = None

    virtual_screen.fill((50, 50, 50))
    window.fill((30, 30, 30))

    for r in range(8):
        for c in range(8):
            if (r + c) % 2 == 0:
                pygame.draw.rect(virtual_screen, (238, 220, 151), (virtual_sq * c, virtual_sq * r, virtual_sq, virtual_sq), 0)
            else:
                pygame.draw.rect(virtual_screen, (150, 77, 34), (virtual_sq * c, virtual_sq * r, virtual_sq, virtual_sq), 0)

    for i in range(12):
        b = B[i]
        char = board.piece_names[i]
        image = piece_images[char]

        while b:
            square = board.ctz(b)
            b = board.remove_bit(b, square)

            col = square % 8
            row = square // 8

            x = col * virtual_sq
            y = row * virtual_sq

            virtual_screen.blit(image, (x, y))

    scaled_surface = pygame.transform.scale(virtual_screen, (board_size, board_size))

    window.blit(scaled_surface, (x_offset, y_offset))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
