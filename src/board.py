from const import *
from square import Square
from piece import *
from move import Move
import copy

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        print(self.squares)
        self.last_move = None
        self._create()
        self._add_piece('white')
        self._add_piece('black')
        

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # Console Board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        print(self.squares[final.row][final.col].piece)


        if isinstance(piece, Pawn):
            # pawn en passant
            if self.en_pessant(initial, final):
                piece.en_passant = True
            else:
                # pawn promotion
                self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook # check wich side the king has castled
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        #clear valid moves to calculate valid moves for new position
        piece.clear_moves()

        # set last move
        self.last_move = move
        for row in range(ROWS):
            for col in range(COLS):
                print(row, col, self.squares[row][col].piece)

    def valid_move(self, piece, move):
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2
    
    def en_pessant(self, initial, final):
        return abs(initial.row - final.row) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)

        # move piece
        temp_board.move(temp_piece, move)
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece # p = piece that threatens check
                    temp_board.calc_moves(p, row, col, bool=False) # calculate moves for enemy piece
                    for m in p.moves:
                        if isinstance(m.final.piece, King): # here m = is moves that have a king at the end aka CHECK
                            return True
        return False
    
    def calc_moves(self, piece, row, col, bool=True):
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
                        #create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        #create new move
                        move = Move(initial, final)
                        #check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                #append new move
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    # blocked 
                    else: break
                # not in range
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
                        #check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                #append new move
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            # en passant moves
            r = 3 if piece.color == 'white' else 4 # row on wich en passant is allowed for both colors
            fr = 2 if piece.color == 'white' else 5 # final for for en passant
            #left en passant
            if Square.in_range(col - 1) and row == r:
                if self.squares[row][col - 1].has_enemy_piece(piece.color):
                    p = self.squares[row][col - 1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            final = Square(fr, col - 1, p)
                            # create a new move
                            move = Move(initial, final)
                            #check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    #append new move
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

            # right en passant
            if Square.in_range(col + 1) and row == r:
                if self.squares[row][col + 1].has_enemy_piece(piece.color):
                    p = self.squares[row][col + 1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            final = Square(fr, col + 1, p)
                            # create a new move
                            move = Move(initial, final)
                            #check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    #append new move
                                    piece.add_move(move)
                            else:
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
                        final_piece = self.squares[posible_move_row][posible_move_col].piece
                        final = Square(posible_move_row, posible_move_col, final_piece) 
                        # create a new move
                        move = Move(initial, final)
                        #check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                #append new move
                                piece.add_move(move)
                            else: break
                        else:
                            #append new move
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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)

                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            #check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    #append new move
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        # has enemy piece = add move = break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            #check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    #append new move
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break

                        # has team piece = BREAK
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
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
                        #check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                #append new move
                                piece.add_move(move)
                            else: break
                        else:
                            piece.add_move(move)


            # Castling moves
            if not piece.moved:
                #queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece(): # castling is not posible because there are piece in the way
                                break

                            if c == 3:
                                #adds left rook to king
                                piece.left_rook = left_rook
                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                #check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new rook move
                                        left_rook.add_move(moveR)
                                        #append new king move
                                        piece.add_move(moveK)
                                else:
                                    # append new rook move
                                    left_rook.add_move(moveR)
                                    #append new king move
                                    piece.add_move(moveK)
                                                
                                                
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece(): # castling is not posible because there are piece in the way
                                break
                            if c == 6:
                                #adds right rook to king
                                piece.right_rook = right_rook
                                
                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final) # move Rook

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final) # move King
                                #check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new rook move
                                        right_rook.add_move(moveR)
                                        #append new king move
                                        piece.add_move(moveK)
                                else:
                                    # append new rook move
                                    right_rook.add_move(moveR)
                                    #append new king move
                                    piece.add_move(moveK)


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
        # self.squares[5][4] = Square(5, 4, Queen(color))
        # self.squares[4][4] = Square(4, 4, Rook(color))
        # self.squares[3][4] = Square(3, 4, Bishop(color))
        # self.squares[4][3] = Square(4, 2, Bishop('white'))
        # self.squares[4][2] = Square(4, 2, Knight('white'))