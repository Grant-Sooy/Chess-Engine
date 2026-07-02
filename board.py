a8, b8, c8, d8, e8, f8, g8, h8, \
a7, b7, c7, d7, e7, f7, g7, h7, \
a6, b6, c6, d6, e6, f6, g6, h6, \
a5, b5, c5, d5, e5, f5, g5, h5, \
a4, b4, c4, d4, e4, f4, g4, h4, \
a3, b3, c3, d3, e3, f3, g3, h3, \
a2, b2, c2, d2, e2, f2, g2, h2, \
a1, b1, c1, d1, e1, f1, g1, h1 = range(64)

def get_bit(bitboard, square):
    return 1 if (bitboard & (1<<square)) else 0

def set_bit(bitboard, square):
    return bitboard | (1<<square)

def remove_bit(bitboard, square):
    return bitboard ^ ( 1<<square if get_bit(bitboard, square) else 0)

def ctz(bitboard):
    return (bitboard & -bitboard).bit_length() - 1

def get_piece_at(B, square):
    for i in range(12):
        if get_bit(B[i], square):
            return i
    return None

def new_board():
    return [ 71776119061217280, 65280,     # pawns (white, black)
            9295429630892703744, 129,     # rooks
            4755801206503243776, 66,      # knights
            2594073385365405696, 36,      # bishops
            576460752303423488, 8,        # queens
            1152921504606846976, 16,      # kings
            18446462598732840960, 65535,  # white, black pieces
            18446462598732840960 | 65535, # all board pieces
        ]

Wpawn, Bpawn, Wrook, Brook, Wknight, Bknight, Wbishop, Bbishop, Wqueen, Bqueen, Wking, Bking, white, black, all_boards = range(15)

piece_names = ['P', 'p', 'R', 'r', 'N', 'n', 'B', 'b', 'Q', 'q', 'K', 'k']


def print_board(B):
    output = [' ' for i in range(64)] 

    # scan the first 12 bitboards for pieces
    for i in range(12): 
        b = B[i]

        # repeatedly find and remove least significant bit from bitboard 
        while b: 
            square = ctz(b)
            b = remove_bit(b, square)
            output[square] = piece_names[i] # add piece to output string


    print ("\n      A B C D E F G H ")
    print ("    __________________ ")

    for i in range(8):
        # need to print upside down and back to front to 
        # ensure correct formatting
        temp = [' ', 8-i, "|"] + output[:8]
        print(*temp, sep=" ") 
        output = output[8:] 

    print ("\n")

def update_bitboards(B):
    # union of other bitboards
    B[white] = B[Wpawn] | B[Wrook] | B[Wknight] | B[Wbishop] | B[Wking] | B[Wqueen]
    B[black] = B[Bpawn] | B[Brook] | B[Bknight] | B[Bbishop] | B[Bking] | B[Bqueen]
    B[all_boards] = B[white] | B[black]


B = new_board()
print(B[Wpawn])
print_board(B)
