import random

import logic.board as board

#--------------------------------------------------------------------------------
# PIECE MOVEMENT LOGIC
#--------------------------------------------------------------------------------

NOT_A_FILE = 0xFEFEFEFEFEFEFEFE
NOT_AB_FILE = 0xFCFCFCFCFCFCFCFC
NOT_H_FILE = 0x7F7F7F7F7F7F7F7F
NOT_GH_FILE = 0x3F3F3F3F3F3F3F3F

def generate_occupancy(index, mask):
    occupancy = 0
    bit_count = 0

    temp_mask = mask
    while temp_mask:
        square = board.ctz(temp_mask)
        temp_mask = board.remove_bit(temp_mask, square)

        if index & (1 << bit_count):
            occupancy = board.set_bit(occupancy, square)

        bit_count += 1

    return occupancy

def find_magic_number(square, mask, attacks_fn):
    N = bin(mask).count('1')
    num_variations = 1 << N

    occupancies = []
    attacks = []
    for index in range(num_variations):
        occ = generate_occupancy(index, mask)
        occupancies.append(occ)
        attacks.append(attacks_fn(square, occ))

    while True:
        magic = random.getrandbits(64) & random.getrandbits(64) & random.getrandbits(64)

        table = [None] * num_variations
        collision = False

        for i in range(num_variations):
            idx = ((occupancies[i] * magic) & 0xFFFFFFFFFFFFFFFF) >> (64 - N)

            if table[idx] is None:
                table[idx] = attacks[i]
            elif table[idx] != attacks[i]:
                collision = True
                break

        if not collision:
            return magic, table

#--------------------------------------------------------------------------------
# KNIGHT ATTACK BOARDS
#--------------------------------------------------------------------------------

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

ROOK_MASKS = [rook_occupancy_mask(sq) for sq in range(64)]

def rook_attacks_on_the_fly(square, occupancy):
    attacks = 0
    rank = square // 8
    file = square % 8

    # north
    rn = rank + 1
    while rn <= 7:
        attacks |= (1 << (rn * 8 + file))
        if occupancy & (1 << (rn * 8 + file)):  # hit a blocker
            break
        rn += 1

    rs = rank - 1
    while rs >= 0:
        attacks |= (1 << (rs * 8 + file))
        if occupancy & (1 << (rs * 8 + file)):
            break
        rs -= 1

    fe = file + 1
    while fe <= 7:
        attacks |= (1 << (rank * 8 + fe))
        if occupancy & (1 << (rank * 8 + fe)):
            break
        fe += 1

    fw = file - 1
    while fw >= 0:
        attacks |= (1 << (rank * 8 + fw))
        if occupancy & (1 << (rank * 8 + fw)):
            break
        fw -= 1

    return attacks & 0xFFFFFFFFFFFFFFFF

ROOK_TABLES = [None] * 64
ROOK_MAGICS = [
    0x48002102188c002,
    0x1400040a002500a,
    0x480100180200008,
    0x4800c8110000800,
    0x80040008008006,
    0x3200100200085104,
    0x100420021000084,
    0x20001088200204c,
    0x40800020884000,
    0x4440400043601001,
    0x201004051002000,
    0xa0100487000a100,
    0x6000800800240180,
    0xaa000806001084,
    0x224802100020080,
    0x102000840820104,
    0x10024800080c000,
    0x420c04004201000,
    0x880801000a000,
    0x92005200205a0040,
    0x1501110045000800,
    0x8001010012880400,
    0x140040002108849,
    0x20005c8810c,
    0x2020400080208000,
    0x408500040046008,
    0x200180100080,
    0x2188008180091000,
    0x8020710100051800,
    0x9414008080420004,
    0x8020400011048,
    0x8a000401c1,
    0x20018040008008a1,
    0x8200040401000,
    0x9002008412002440,
    0x490021001000,
    0x1400c0080800801,
    0x618200100a001408,
    0x304033102c00288a,
    0x9000408066000304,
    0x140004080208000,
    0x40201000414008,
    0x50200100110040,
    0xa408020100501000,
    0x408000805010010,
    0x8100040009000a,
    0x2000090002008080,
    0x40690140820004,
    0x404442312008600,
    0x94884c000200080,
    0x28200080b00a2080,
    0x1000e20500100,
    0x52800800440180,
    0x8804002200800480,
    0x401002442000100,
    0x40410084024200,
    0x1004820800011,
    0xc44208500104007,
    0x84700a000128843,
    0x8020051001002009,
    0x4001001084180007,
    0x2004110280422,
    0x2120008201100804,
    0x4800002400408106,
]

for square in range(64):
    mask = ROOK_MASKS[square]
    N = bin(mask).count('1')
    num_variations = 1 << N
    table = [None] * num_variations
    for index in range(num_variations):
        occ = generate_occupancy(index, mask)
        idx = ((occ * ROOK_MAGICS[square]) & 0xFFFFFFFFFFFFFFFF) >> (64 - N)
        table[idx] = rook_attacks_on_the_fly(square, occ)
    ROOK_TABLES[square] = table

def get_rook_attacks(square, occupancy):
    mask = ROOK_MASKS[square]
    N = bin(mask).count('1')
    index = ((occupancy & mask) * ROOK_MAGICS[square] & 0xFFFFFFFFFFFFFFFF) >> (64 - N)
    return ROOK_TABLES[square][index]

#--------------------------------------------------------------------------------
# BISHOP ATTACK BOARDS
#--------------------------------------------------------------------------------

def bishop_occupancy_squares(square: int) -> int:
    attacks = 0

    rank = square // 8
    file = square % 8

    rne = rank + 1
    fne = file + 1
    while rne < 7 and fne < 7:
        attacks |= (1 << (rne * 8 + fne))
        rne += 1
        fne += 1

    rnw = rank + 1
    fnw = file - 1
    while rnw < 7 and fnw > 0:
        attacks |= (1 << (rnw * 8 + fnw))
        rnw += 1
        fnw -= 1

    rse = rank - 1
    fse = file + 1
    while rse > 0 and fse < 7:
        attacks |= (1 << (rse * 8 + fse))
        rse -= 1
        fse += 1

    rsw = rank - 1
    fsw = file - 1
    while rsw > 0 and fsw > 0:
        attacks |= (1 << ( rsw * 8 + fsw))
        rsw -= 1
        fsw -= 1

    return attacks & 0xFFFFFFFFFFFFFFFF
