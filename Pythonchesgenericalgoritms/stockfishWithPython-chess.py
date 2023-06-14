import chess
import chess.engine

# a chess position where white can win in one move
board = chess.Board("5Q2/5K1k/8/8/8/8/8/8 w - - 0 1")

# initialize Stockfish 
engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\teunt\Downloads\arena_3.5.1\Engines\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")

# board = chess.Board()
# while not board.is_game_over():
#     result = engine.play(board, chess.engine.Limit(time=0.1))
#     print(board.san(result.move))
#     board.push(result.move)

# engine.quit()

# you can control the engine's search by time or depth
info = engine.analyse(board, chess.engine.Limit(time=0.1))