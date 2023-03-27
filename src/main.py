import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from board import *

class Main:

    def __init__(self):
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
                            board.calc_moves(piece, clicked_row, clicked_col)
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
                            captured = board.squares[released_row][released_col].has_piece()
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
main.mainloop()