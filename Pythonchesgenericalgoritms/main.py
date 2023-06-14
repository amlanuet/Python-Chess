import chess
import chess.engine
import numpy as np
from geneticalgorithm import geneticalgorithm as ga


varbound=np.array([[0,12]]*64)

algorithm_param = {'max_num_iteration': 5000,
                   'population_size': 15,
                   'mutation_probability': 0.06,
                   'elit_ratio': 0.01,
                   'crossover_probability': 0.9,
                   'parents_portion': 0.3,
                   'crossover_type': 'two_point',
                   'max_iteration_without_improv': 2000}


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
        penalty += 10

    return penalty

model=ga(function=f,dimension=64,variable_type='int',variable_boundaries=varbound, algorithm_parameters=algorithm_param)
model.run()

best_board = array_to_chess_board(list(model.best_variable))
print(best_board.fen())