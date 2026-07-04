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


def print_bitboard(bitboard):
    bitboard = bin(bitboard)[2:].zfill(64)

    print("\n      A B C D E F G H ")
    print("   ____________________")

    for i in range(8):
        temp = [' ', 8-i, "|"] + [*(bitboard[-8:])[::-1]]
        temp = [i if i!='0' else '.' for i in temp]

        print(*temp, sep=" ")

        bitboard = bitboard[:-8]
    print("\n")

#--------------------------------------------------------------------------------
# PIECE MOVEMENT LOGIC
#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
# KNIGHT ATTACK BOARDS
#--------------------------------------------------------------------------------

NOT_A_FILE = 0xFEFEFEFEFEFEFEFE
NOT_AB_FILE = 0xFCFCFCFCFCFCFCFC
NOT_H_FILE = 0x7F7F7F7F7F7F7F7F
NOT_GH_FILE = 0x3F3F3F3F3F3F3F3F

def generate_knight_attacks(square: int) -> int:
    attacks = 0
    bitboard = 1 << square

    if bitboard & NOT_A_FILE: attacks |= (bitboard << 15)
    if bitboard & NOT_H_FILE: attacks |= (bitboard << 17)

    if bitboard & NOT_AB_FILE: attacks |= (bitboard << 6)
    if bitboard & NOT_GH_FILE: attacks |= (bitboard << 10)

    if bitboard & NOT_A_FILE: attacks |= (bitboard >> 17)
    if bitboard & NOT_H_FILE: attacks |= (bitboard >> 15)

    if bitboard & NOT_AB_FILE: attacks |= (bitboard >> 10)
    if bitboard & NOT_GH_FILE: attacks |= (bitboard >> 6)

    return attacks & 0xFFFFFFFFFFFFFFFF

KNIGHT_ATTACKS = [generate_knight_attacks(sq) for sq in range(64)]

#--------------------------------------------------------------------------------
# KING ATTACK BOARDS
#--------------------------------------------------------------------------------

def generate_king_attacks(square: int) -> int:
    attacks = 0
    bitboard = 1 << square

    if bitboard & NOT_A_FILE: attacks |= (bitboard >> 1)
    if bitboard & NOT_A_FILE: attacks |= (bitboard << 7)
    if bitboard & NOT_A_FILE: attacks |= (bitboard >> 9)

    if bitboard & NOT_H_FILE: attacks |= (bitboard << 1)
    if bitboard & NOT_H_FILE: attacks |= (bitboard >> 7)
    if bitboard & NOT_H_FILE: attacks |= (bitboard << 9)

    if bitboard: attacks |= (bitboard >> 8)
    if bitboard: attacks |= (bitboard << 8)

    return attacks & 0xFFFFFFFFFFFFFFFF

KING_ATTACKS = [generate_king_attacks(sq) for sq in range(64)]

#--------------------------------------------------------------------------------
# ROOK ATTACK BOARDS
#--------------------------------------------------------------------------------

def rook_occupancy_mask(square: int) -> int:
    attacks = 0
    bitboard = 1 << square

    rank = square // 8
    file = square % 8

    rn = rank + 1
    while rn < 7:
        attacks |= (1 << (rn * 8 + file))
        rn += 1

    rs = rank - 1
    while rs > 0:
        attacks |= (1 << (rs * 8 + file))
        rs -= 1

    fe = file + 1
    while fe < 7:
        attacks |= (1 << (rank * 8 + fe))
        fe += 1

    fw = file - 1
    while fw > 0:
        attacks |= (1 << (rank * 8 + fw))
        fw -= 1

    return attacks & 0xFFFFFFFFFFFFFFFF

ROOK_ATTACKS = [rook_occupancy_mask(sq) for sq in range(64)]

