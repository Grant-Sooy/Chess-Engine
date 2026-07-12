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

B = board.new_board()
moves = rook_moves(B, board.white)
print(moves)
