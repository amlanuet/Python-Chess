import chess
import chess.engine
import numpy as np
from geneticalgorithm import geneticalgorithm as ga

import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from board import *

class Main:


    def start(self):
        varbound=np.array([[0,12]]*64)
        engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\teunt\Downloads\arena_3.5.1\Engines\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")

        # # DEFAULT PARAMS
        # algorithm_param = {'max_num_iteration': 50000,
        #                    'population_size': 20,
        #                    'mutation_probability': 0.05,
        #                    'elit_ratio': 0.01,
        #                    'crossover_probability': 0.9,
        #                    'parents_portion': 0.3,
        #                    'crossover_type': 'two_point',
        #                    'max_iteration_without_improv': 5000}

        # FAST BUT PROB NOT GOOD 
        # USED FOR TESTING ONLY!!
        algorithm_param = {'max_num_iteration': 15,
                        'population_size': 10,
                        'mutation_probability': 0.095,
                        'elit_ratio': 0.0105,
                        'crossover_probability': 0.1,
                        'parents_portion': 0.3,
                        'crossover_type': 'uniform',
                        'max_iteration_without_improv': 4200}

        def value_to_piece(value):
            if value == 0:
                return None
            elif value <= 6:
                # Pieces have values 1 through 6
                return chess.Piece(value, chess.WHITE)
            else:
                return chess.Piece(value - 6, chess.BLACK)

        def array_to_chess_board(arr):
            # construct an empty chess board
            board = chess.Board(fen='8/8/8/8/8/8/8/8 w - - 0 1')
            for i, value in enumerate(arr):
                piece = value_to_piece(value)
                if piece:
                    board.set_piece_at(i, piece)
            return board

        def f(X):
            board = array_to_chess_board(X)

            #We want as few pieces as possible so each piece adds t oour penalty
            penalty = len(board.piece_map()) * 0.1
            # Add a big penalty for invalid positions
            if not board.is_valid():
                return 10 + penalty
                
            # You can tune the depth for performance reasons
            info = engine.analyse(board, chess.engine.Limit(depth=10), multipv=2)

            # If there are no moves (meaning the game is over), return a high penalty
            if len(info) < 1:
                return 9 + penalty
            
            # Also heavily penalize having only 1 move, puzzles are only interesting
            #   if we have a choice to make
            if len(info) < 2:
                return 8 + penalty
            
            WhiteQueenCount = 0
            BlackQueenCount = 0

            WhiteRookCount = 0
            BlackRookCount = 0

            WhiteKnightCount = 0
            BlackKnightCount = 0

            WhiteBishopCount = 0
            BlackBishopCount = 0

            for value in board.fen():
                # print(value)
                if value == "Q":
                    WhiteQueenCount += 1
                    # print('white queen')
                    if WhiteQueenCount > 2:
                        # print('too many white queens')
                        return 7 + penalty
                if value == "q":
                    BlackQueenCount += 1
                    # print('black queen')
                    if BlackQueenCount > 2:
                        # print('too many black queens')
                        return 7 + penalty 
                if value == "R":
                    WhiteRookCount += 1
                    # print('white rook')
                    if WhiteRookCount > 2:
                        # print('too many white rooks')
                        return 7 + penalty
                if value == "r":
                    BlackRookCount += 1
                    # print('black rook')
                    if BlackRookCount > 2:
                        # print('too many black rooks')
                        return 7 + penalty       
                if value == 'N':
                    WhiteKnightCount += 1
                    # print('white knight')
                    if WhiteKnightCount > 2:
                        # print('too many white knights')
                        return 5.4 + penalty
                if value == "n":
                    BlackKnightCount += 1
                    # print('black knight')
                    if BlackKnightCount > 2:
                        # print('too many black knights')
                        return 5.4 + penalty
                if value == 'B':
                    WhiteBishopCount += 1
                    # print('white bishop')
                    if WhiteBishopCount > 2:
                        # print('too many white bishops')
                        return 5.5 + penalty
                if value == "b":
                    BlackBishopCount += 1
                    # print('black bishop')
                    if BlackBishopCount > 2:
                        # print('too many black bishops')
                        return 5.5 + penalty
            
                    
            # print(board.queens)
            # if board.queens > 2:
            #     print("more than 1 queen")
            #     return 3 + penalty
            
            # print(board.rooks)
            # if board.rooks > 4:
            #     print("more than 4 rooks")
            #     return 3 + penalty

            # print(board.knights)
            # if board.knights > 4:
            #     print("more than 4 knights")
            #     return 3 + penalty
            
            # print(board.bishops)
            # if board.queens > 4:
            #     print("more than 4 bishops")
            #     return 3 + penalty
            
            
            # We're specifically looking for puzzles where White can mate in 3 moves
            #   so we'll penalize cases where white does not have a forced mate
            score = info[0]["score"].white()
            if not score.is_mate() or score.mate() <= 0:
                return 6 + penalty
            
            # Add a penalty for the distance away from mate in 3
            penalty += min(3, abs(score.mate() - 3)) / 3

            # Finally, add a high penalty if the second best move in also good.
            # The defining characteristic of a puzzle is that thesecond best move is bad
            second_move_score = info[1]["score"].white().score(mate_score=1000)
            if second_move_score > 100:
                penalty += min(10.0, second_move_score / 100)

            return penalty
        model=ga(function=f,dimension=64,variable_type='int',variable_boundaries=varbound, algorithm_parameters=algorithm_param)
        model.run()

        def display_board(fen_string):
            board = chess.Board(fen_string)
            print(board)


        best_board = array_to_chess_board(list(model.best_variable))
        fen_string = best_board.fen()
        self.board.populate_puzzle(fen_string)
        display_board(fen_string)
        pygame.display.update()
        self.game.show_pieces(self.screen)

    def __init__(self):
        self.board = Board()
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()
    def mainloop(self):

        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # Click to drag
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    # position clicked on board
                    # print(event.pos)
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # if clicked sqr has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # Check valid piece color
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            # Save initial position so when an invalid move gets made the piece can return to the initial square 
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            #show methods
                            game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # Mouse motion
                elif event.type == pygame.MOUSEMOTION:

                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # Click release
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # create posibble move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        
                        # check valid
                        if board.valid_move(dragger.piece, move):
                            # print('valid move')
                            #normal capture (NOT en_passant)
                            captured = board.squares[released_row][released_col].has_piece()
                            board.set_false_en_passant()

                            board.move(dragger.piece, move)
                            # play sound 
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()
                        else: print('invalid move')
                    dragger.undrag_piece()

                # key press events
                elif event.type == pygame.KEYDOWN:
                    # T down
                    #changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()\
                    # R donw
                    #rest
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                
                # Quit Application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
main= Main()
main.start()
main.mainloop()