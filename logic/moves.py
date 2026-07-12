import atktbls
import board

#--------------------------------------------------------------------------------
# KNIGHT MOVES
#--------------------------------------------------------------------------------

def knight_moves(B, color):
    moves = []

    if color == board.white:
        knights = B[board.Wknight]
        friendly_pieces = B[board.white]
    else:
        knights = B[board.Bknight]
        friendly_pieces = B[board.black]

    b = knights
    while b:
        square = board.ctz(b)
        b = board.remove_bit(b, square)

        valid_squares = atktbls.KNIGHT_ATTACKS[square] & ~friendly_pieces

        destinations = valid_squares
        while destinations:
            dest = board.ctz(destinations)
            destinations = board.remove_bit(destinations, dest)
            moves.append((square, dest))

    return moves

#--------------------------------------------------------------------------------
# ROOK MOVES
#--------------------------------------------------------------------------------

def rook_moves(B, color):
    moves = []

    if color == board.white:
        rooks = B[board.Wrook]
        friendly_pieces = B[board.white]
    else:
        rooks = B[board.Brook]
        friendly_pieces = B[board.black]

    r = rooks
    while r:
        square = board.ctz(r)
        r = board.remove_bit(r, square)

        valid_squares = atktbls.get_rook_attacks(square, B[board.all_boards]) & ~friendly_pieces

        destinations = valid_squares
        while destinations:
            dest = board.ctz(destinations)
            destinations = board.remove_bit(destinations, dest)
            moves.append((square, dest))

    return moves

#--------------------------------------------------------------------------------
# BISHOP MOVES
#--------------------------------------------------------------------------------

def bishop_moves(B, color):
    moves = []

    if color == board.white:
        bishops = B[board.Wbishop]
        friendly_pieces = B[board.white]
    else:
        bishops = B[board.Bbishop]
        friendly_pieces = B[board.black]

    b = bishops
    while b:
        square = board.ctz(b)
        b = board.remove_bit(b, square)

        valid_squares = atktbls.get_bishop_attacks(square, B[board.all_boards]) & ~friendly_pieces

        destinations = valid_squares
        while destinations:
            dest = board.ctz(destinations)
            destinations = board.remove_bit(destinations, dest)
            moves.append((square, dest))

    return moves

#--------------------------------------------------------------------------------
# QUEEN MOVES
#--------------------------------------------------------------------------------

def queen_moves(B, color):
    moves = []

    if color == board.white:
        queens = B[board.Wqueen]
        friendly_pieces = B[board.white]
    else:
        queens = B[board.Bqueen]
        friendly_pieces = B[board.black]

    q = queens
    while q:
        square = board.ctz(q)
        q = board.remove_bit(q, square)

        valid_squares = atktbls.get_queen_attacks(square, B[board.all_boards]) & ~friendly_pieces

        destinations = valid_squares
        while destinations:
            dest = board.ctz(destinations)
            destinations = board.remove_bit(destinations, dest)
            moves.append((square, dest))

    return moves

#--------------------------------------------------------------------------------
# KING MOVES
#--------------------------------------------------------------------------------

def king_moves(B, color):
    moves = []

    if color == board.white:
        kings = B[board.Wking]
        friendly_pieces = B[board.white]
    else:
        kings = B[board.Bking]
        friendly_pieces = B[board.black]

    k = kings
    while k:
        square = board.ctz(k)
        k = board.remove_bit(k, square)

        valid_squares = atktbls.KING_ATTACKS[square] & ~friendly_pieces

        destinations = valid_squares
        while destinations:
            dest = board.ctz(destinations)
            destinations = board.remove_bit(destinations, dest)
            moves.append((square, dest))

    return moves

#--------------------------------------------------------------------------------
# PAWN MOVES
#--------------------------------------------------------------------------------

def pawn_moves(B, color):
    moves = []

    if color == board.white:
        pawns = B[board.Wpawn]
        p = pawns
        while p:
            square = board.ctz(p)
            p = board.remove_bit(p, square)

            one_forward = square - 8
            if not (B[board.all_boards] & (1 << one_forward)):
                moves.append((square, one_forward))

                two_forward = square - 16
                rank = square // 8
                if rank == 6 and not (B[board.all_boards] & (1 << two_forward)):
                    moves.append((square, two_forward))

            valid_squares = atktbls.WHITE_PAWN_ATTACKS[square] & B[board.black]

            destinations = valid_squares
            while destinations:
                dest = board.ctz(destinations)
                destinations = board.remove_bit(destinations, dest)
                moves.append((square, dest))

    else:
        pawns = B[board.Bpawn]
        p = pawns
        while p:
            square = board.ctz(p)
            p = board.remove_bit(p, square)

            one_forward = square + 8
            if not (B[board.all_boards] & (1 << one_forward)):
                moves.append((square, one_forward))

                two_forward = square + 16
                rank = square // 8
                if rank == 1 and not (B[board.all_boards] & (1 << two_forward)):
                    moves.append((square, two_forward))

            valid_squares = atktbls.BLACK_PAWN_ATTACKS[square] & B[board.white]

            destinations = valid_squares
            while destinations:
                dest = board.ctz(destinations)
                destinations = board.remove_bit(destinations, dest)
                moves.append((square, dest))

    return moves
