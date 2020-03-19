import sys
from pieces_classes import *

pygame.init()

# CONSTANTS
COLOR_WHITE = (252, 215, 157)
COLOR_BLACK = (171, 101, 37)
COLOR_MARKER = (146, 187, 0)
DISPLAY_SIZE = 640
UNIT_WIDTH = DISPLAY_SIZE / 8
MINIMAX_DEPTH = 5  # difficulty?
INFINITY = 1000


# FUNCTIONS

def print_board():
    for x in range(8):
        for y in range(8):
            if (x + y) % 2 == 0:
                pygame.draw.rect(screen, COLOR_WHITE, (x * UNIT_WIDTH, y * UNIT_WIDTH, UNIT_WIDTH, UNIT_WIDTH))
            else:
                pygame.draw.rect(screen, COLOR_BLACK, (x * UNIT_WIDTH, y * UNIT_WIDTH, UNIT_WIDTH, UNIT_WIDTH))

            if board_state[x][y] is not None:
                screen.blit(board_state[x][y].image, (x * UNIT_WIDTH, y * UNIT_WIDTH))


def get_clicked_position():
    coordinates = pygame.mouse.get_pos()
    return int(coordinates[0] // UNIT_WIDTH), int(coordinates[1] // UNIT_WIDTH)


def print_markers(valid_moves):
    for move in valid_moves:
        centre = (int(move[0] * UNIT_WIDTH + UNIT_WIDTH / 2), int(move[1] * UNIT_WIDTH + UNIT_WIDTH / 2))
        pygame.draw.circle(screen, COLOR_MARKER, centre, 20)


def is_game_over(board):
    king_count = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] is not None:
                if board[x][y].__class__.__name__ is "King":
                    king_count += 1

    if king_count == 2:
        return False
    return True


def get_point_sum(board):
    point_sum = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] is not None:
                point_sum += board[x][y].points
    return point_sum


def get_copy(board):
    board_copy = []
    for column in board:
        board_copy.append(column.copy())
    return board_copy


def minimax(board, black, white, depth, alpha, beta, is_maximizing):
    if depth == 0 or is_game_over(board):
        return get_point_sum(board), 0, 0

    if is_maximizing:
        max_val = -INFINITY
        play = None
        player = None
        for piece_pos in black:
            for move in board[piece_pos[0]][piece_pos[1]].get_moves(piece_pos, board):
                board_temp = get_copy(board)
                board_temp[move[0]][move[1]] = board_temp[piece_pos[0]][piece_pos[1]]
                board_temp[piece_pos[0]][piece_pos[1]] = None
                black_temp = black.copy()
                black_temp[black.index(piece_pos)] = move
                white_temp = white
                if move in white:
                    white_temp = white.copy()
                    white_temp.remove(move)

                val = minimax(board_temp, black_temp, white_temp, depth - 1, alpha, beta, False)
                if val[0] > max_val:
                    max_val = val[0]
                    player = piece_pos
                    play = move
                alpha = max(alpha, val[0])
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return max_val, player, play

    else:
        min_val = INFINITY
        play = None
        player = None
        for piece_pos in white:
            for move in board[piece_pos[0]][piece_pos[1]].get_moves(piece_pos, board):
                board_temp = get_copy(board)
                board_temp[move[0]][move[1]] = board_temp[piece_pos[0]][piece_pos[1]]
                board_temp[piece_pos[0]][piece_pos[1]] = None
                white_temp = white.copy()
                white_temp[white.index(piece_pos)] = move
                black_temp = black
                if move in black:
                    black_temp = black.copy()
                    black_temp.remove(move)
                val = minimax(board_temp, black_temp, white_temp, depth - 1, alpha, beta, True)
                if val[0] < min_val:
                    min_val = val[0]
                    player = piece_pos
                    play = move
                beta = min(beta, val[0])
                if beta <= alpha:
                    break

            if beta <= alpha:
                break
        return min_val, player, play


pygame.display.set_caption("Say Chesse!")
screen = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))


board_state = [[Rook('b'), Pawn('b'), None, None, None, None, Pawn('w'), Rook('w')],
               [Knight('b'), Pawn('b'), None, None, None, None, Pawn('w'), Knight('w')],
               [Bishop('b'), Pawn('b'), None, None, None, None, Pawn('w'), Bishop('w')],
               [Queen('b'), Pawn('b'), None, None, None, None, Pawn('w'), Queen('w')],
               [King('b'), Pawn('b'), None, None, None, None, Pawn('w'), King('w')],
               [Bishop('b'), Pawn('b'), None, None, None, None, Pawn('w'), Bishop('w')],
               [Knight('b'), Pawn('b'), None, None, None, None, Pawn('w'), Knight('w')],
               [Rook('b'), Pawn('b'), None, None, None, None, Pawn('w'), Rook('w')]]
# user-white-bottom, comp-black-top

black_pieces = [(x, y) for y in [1, 0] for x in range(8)]  # first 8 members are pawns
white_pieces = [(x, y) for y in [6, 7] for x in range(8)]

print_board()
pygame.display.update()

active_piece_pos = None
open_slots = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = get_clicked_position()
            if active_piece_pos is None:
                if board_state[pos[0]][pos[1]] is not None and board_state[pos[0]][pos[1]].color is 'w':
                    active_piece_pos = pos
                    open_slots = board_state[active_piece_pos[0]][active_piece_pos[1]].get_moves(pos, board_state)
                    print_markers(open_slots)
                    pygame.display.update()

            else:
                if pos in open_slots:
                    board_state[pos[0]][pos[1]] = board_state[active_piece_pos[0]][active_piece_pos[1]]
                    board_state[active_piece_pos[0]][active_piece_pos[1]] = None
                    white_pieces[white_pieces.index(active_piece_pos)] = pos
                    if pos in black_pieces:
                        black_pieces.remove(pos)
                    active_piece_pos = None
                    open_slots = None
                    print_board()
                    pygame.display.update()

                    comp_move = minimax(board_state, black_pieces, white_pieces, MINIMAX_DEPTH, -INFINITY, INFINITY, True)
                    board_state[comp_move[2][0]][comp_move[2][1]] = board_state[comp_move[1][0]][comp_move[1][1]]
                    board_state[comp_move[1][0]][comp_move[1][1]] = None
                    black_pieces[black_pieces.index(comp_move[1])] = comp_move[2]
                    if comp_move[2] in white_pieces:
                        white_pieces.remove(comp_move[2])
                    print_board()
                    pygame.display.update()

                else:
                    active_piece_pos = None
                    open_slots = None
                    print_board()
                    pygame.display.update()