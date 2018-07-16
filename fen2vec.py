import chess
import numpy as np

from string import digits as DIGITS

def fen2vec(fen_str):

    PIECES = "rnbqkp"
    square_vec_len = len(PIECES) + 2 #n_pieces + is white + is_black
    piece_dict = dict(zip(PIECES, range(square_vec_len)))
    
    def give_sqare_idx(square):
        return chess.SQUARE_NAMES.index(square)

    def square2vec(char):
        vec = np.zeros(square_vec_len)
        if char in DIGITS:
            return np.zeros(square_vec_len * int(char))
        vec[piece_dict[char.lower()]] = 1   
        if char.isupper():
            vec[len(PIECES)] = 1
        else:
            vec[len(PIECES) + 1] = 1
        return vec

    def parse_state_str(state_str):
        whos_turn, castle_str, en_passent, _, _ = state_str.split()
        whos_turn = np.array([1, 0]) if whos_turn == "w" else np.array([0, 1])
        
        def parse_castle_str(castle_str):
            cstl_vec = np.zeros(4)
            if "K" in state_str:
                cstl_vec[0] = 1
            if "Q" in state_str:
                cstl_vec[1] = 1
            if "k" in state_str:
                cstl_vec[2] = 1
            if "q" in state_str:
                cstl_vec[3] = 1
            return cstl_vec
        
        def parse_en_passent(en_pass_str):
            vec = np.zeros(64)
            if en_pass_str in chess.SQUARE_NAMES:
                vec[chess.SQUARE_NAMES.index(en_pass_str)] = 1
            return vec
        
        return np.concatenate([whos_turn,
                               parse_castle_str(castle_str),
                               parse_en_passent(en_passent)])

    pieces_str, state_str = fen_str.split(" ", 1)
    board_vecs = [square2vec(square_char) for square_char in pieces_str \
                    if square_char is not "/"]
    return np.concatenate(board_vecs + [parse_state_str(state_str)])

board = chess.Board()
# board.push(chess.Move.from_uci("e2e4"))
print(len(fen2vec(board.fen())))

# def tests():
#     board = chess.Board()
#     assert 