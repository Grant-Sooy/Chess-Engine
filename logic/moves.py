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

#--------------------------------------------------------------------------------
# FURTHER LOGIC
#--------------------------------------------------------------------------------

def generate_all_moves(B, color):
    moves = []
    moves += pawn_moves(B, color)
    moves += knight_moves(B, color)
    moves += bishop_moves(B, color)
    moves += rook_moves(B, color)
    moves += queen_moves(B, color)
    moves += king_moves(B, color)
    return moves

def is_in_check(B, color):
    if color == board.white:
        king_square = board.ctz(B[board.Wking])

        enemy_pawns = B[board.Bpawn]
        enemy_knights = B[board.Bknight]
        enemy_bishops = B[board.Bbishop]
        enemy_rooks = B[board.Brook]
        enemy_queens = B[board.Bqueen]
        enemy_kings = B[board.Bking]
        pawn_attacks = atktbls.WHITE_PAWN_ATTACKS
    else:
        king_square = board.ctz(B[board.Bking])

        enemy_pawns = B[board.Wpawn]
        enemy_knights = B[board.Wknight]
        enemy_bishops = B[board.Wbishop]
        enemy_rooks = B[board.Wrook]
        enemy_queens = B[board.Wqueen]
        enemy_kings = B[board.Wking]
        pawn_attacks = atktbls.BLACK_PAWN_ATTACKS


    if atktbls.KNIGHT_ATTACKS[king_square] & enemy_knights:
        return True
    if pawn_attacks[king_square] & enemy_pawns:
        return True
    if atktbls.KING_ATTACKS[king_square] & enemy_kings:
        return True
    if atktbls.get_bishop_attacks(king_square, B[board.all_boards]) & (enemy_bishops | enemy_queens):
        return True
    if atktbls.get_rook_attacks(king_square, B[board.all_boards]) & (enemy_rooks | enemy_queens):
        return True

    return False

def make_move(B, move):
    src, dest = move
    piece = board.get_piece_at(B, src)
    captured = board.get_piece_at(B, dest)

    B[piece] = board.set_bit(B[piece], dest)
    B[piece] = board.remove_bit(B[piece], src)

    if captured is not None:
        B[captured] = board.remove_bit(B[captured], dest)

    board.update_bitboards(B)
    return captured

def unmake_move(B, move, captured):
    src, dest = move
    piece = board.get_piece_at(B, dest)

    B[piece] = board.set_bit(B[piece], src)
    B[piece] = board.remove_bit(B[piece], dest)

    if captured is not None:
        B[captured] = board.set_bit(B[captured], dest)

    board.update_bitboards(B)

def generate_legal_moves(B, color):
    pseudolegal = generate_all_moves(B, color)
    legal = []

    for move in pseudolegal:
        captured = make_move(B, move)
        if not is_in_check(B, color):
            legal.append(move)
        unmake_move(B, move, captured)

    return legal
