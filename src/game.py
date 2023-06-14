import pygame
from const import *
from board import Board
from dragger import *
from config import Config
from theme import Theme               
from square import Square
from piece import Piece

class Game:
    def __init__(self, fen_string):
        self.next_player = 'white'
        self.hovered_square = None
        self.board = Board(fen_string)
        self.dragger = Dragger()
        self.config = Config()

    # Show methods

    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label for coordinates
                    label = self.config.font.render(str(ROWS-row), 1, color)
                    label_pos = (5, 5 + row * SQSIZE)
                    #blit
                    surface.blit(label, label_pos)

                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label for coordinates
                    label = self.config.font.render(Square.get_alphacol(col), 1, color)
                    label_pos = (col * SQSIZE + SQSIZE - 20 , HEIGHT - 20)
                    #blit
                    surface.blit(label, label_pos)
        
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                square = self.board.squares[row][col]
                if isinstance(square, Piece):
                    piece = square

                    # Render the piece on the screen
                    piece.set_texture(size=80)
                    img = pygame.image.load(piece.texture)
                    img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                    piece.texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, piece.texture_rect)
                    
    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece
            # Loop a valid moves
            for move in piece.moves:
                # color for vaid placements
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # rect for valid placements
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                #blit the valid placements
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if isinstance(self.hovered_square, Square):
            # Save color
            color = (180, 180, 180)
            # Rect
            rect = (
                self.hovered_square.col * SQSIZE,
                self.hovered_square.row * SQSIZE,
                SQSIZE,
                SQSIZE
            )
            # Blit update
            pygame.draw.rect(surface, color, rect, width=3)


    def show_hover(self, surface):
        if self.hovered_square:
            #save color
            color = (180, 180, 180)
            #rect
            rect = (self.hovered_square.col * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)
            #blit update
            pygame.draw.rect(surface, color, rect, width=3)

    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # Save color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # Rect
                rect = (
                    pos.col * SQSIZE,
                    pos.row * SQSIZE,
                    SQSIZE,
                    SQSIZE
                )
                # Blit update
                pygame.draw.rect(surface, color, rect)


    # Other methods
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_square = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self, fen_string):
        self.__init__(fen_string)