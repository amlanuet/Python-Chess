from const import *
from square import Square
from piece import *
from move import Move

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        self._create()
        self._add_piece('white')
        self._add_piece('black')


    def calc_moves(self, piece, row, col):
        '''
        Calculate all the possible (valid) moves of an specific piece on a specific position
        '''
        def pawn_moves():
            # steps for first pawn move
            steps = 1 if piece.moved else 2

            # Vertical move
            start = row + piece.dir
            end = row + (piece.dir * (1  + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        #createinitial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else: break
                else: break
            
            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a new move
                        move = Move(initial, final)
                        piece.add_move(move)

        def knight_moves():
            # 8 posible moves
            posible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1)
            ]

            for posible_move in posible_moves:
                posible_move_row, posible_move_col = posible_move

                if Square.in_range(posible_move_row, posible_move_col):
                    if self.squares[posible_move_row][posible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(posible_move_row, posible_move_col) # piece=piece still needs to be added
                        # create a new move
                        move = Move(initial, final)
                        #append new valid move
                        piece.add_move(move)
        
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                # start checcking possible moves untill we are obstructed
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                    
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            piece.add_move(move)

                        # has enemy piece
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break

                        # has team piece = BREAK
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    # NOT in range STOP
                    else: break

                    # if all requirements are met increment untill one doesnt and then stop completely with the incrementing
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row - 1, col + 0), # UP
                (row - 1, col + 1), # UP RIGHT
                (row + 0, col + 1), # RIGHT
                (row + 1, col + 1), # DONW RIGHT
                (row + 1, col + 0), # DOWN
                (row + 1, col - 1), # DONW LEFT
                (row + 0, col - 1), # LEFT
                (row - 1, col - 1)  # UP LEFT
            ]

            # Normal king moves
            for posible_move in adjs:
                posible_move_row, posible_move_col = posible_move
                if Square.in_range(posible_move_row, posible_move_col):
                    if self.squares[posible_move_row][posible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(posible_move_row, posible_move_col) # piece=piece still needs to be added
                        # create a new move
                        move = Move(initial, final)
                        #append new valid move
                        piece.add_move(move)

            # Castling moves

            #queen side

            #king side

        if isinstance(piece, Pawn): pawn_moves()
        elif isinstance(piece, Knight): knight_moves()
        elif isinstance(piece, Bishop): straightline_moves([
                (-1,  1), # UP RIGHT
                (-1, -1), # UP LEFT
                ( 1,  1), # DOWN RIGHT
                ( 1, -1), # DOWN LEFT
        ])
        elif isinstance(piece, Rook): straightline_moves([
                (-1, 0), # UP
                ( 1, 0), # DOWN
                (0, -1), # LEFT
                ( 0, 1)  # RIGHT
        ])
        elif isinstance(piece, Queen): straightline_moves([
                (-1,  0), # UP
                ( 1,  0), # DOWN
                ( 0, -1), # LEFT
                ( 0,  1), # RIGHT
                (-1,  1), # UP RIGHT
                (-1, -1), # UP LEFT
                ( 1,  1), # DOWN RIGHT
                ( 1, -1)  # DOWN LEFT
        ])
        elif isinstance(piece, King): king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_piece(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # -- Pawns --
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # -- Knights --
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))


        # -- Bishops --
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # -- Rooks --
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # -- Queen --
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # -- King --
        self.squares[row_other][4] = Square(row_other, 4, King(color))


        # Adding more pieces for testing of the movement
        self.squares[5][4] = Square(5, 4, Queen(color))
        self.squares[4][4] = Square(4, 4, Rook(color))
        self.squares[3][4] = Square(3, 4, Bishop(color))
        self.squares[4][3] = Square(4, 2, Bishop('white'))
        self.squares[4][2] = Square(4, 2, Knight('white'))