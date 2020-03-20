from pieces_classes import *

pygame.init()

# CONSTANTS
COLOR_WHITE = (252, 215, 157)
COLOR_BLACK = (171, 101, 37)
COLOR_MARKER = (87, 187, 0)
DISPLAY_SIZE = 640
UNIT_WIDTH = DISPLAY_SIZE / 8
INFINITY = 1000


# FUNCTIONS
def get_difficulty_from_menu():
    screen.fill((0, 0, 0))
    title_font = pygame.font.SysFont("Georgia", 35, bold=True)
    title_text = title_font.render("CHOOSE YOUR DIFFICULTY", True, (255, 255, 255))
    option_font = pygame.font.SysFont("Segoe UI", 30, bold=False)
    easy_text = option_font.render("Way Too Easy", True, (128, 128, 128))
    medium_text = option_font.render("Surprisingly Medium", True, (128, 128, 128))
    hard_text = option_font.render("Harder Than Steel", True, (128, 128, 128))
    credit_font = pygame.font.SysFont("Segoe UI", 15, bold=False)
    credit_text = credit_font.render("github.com/clifordjoshy", True, (255, 255, 255))
    screen.blit(title_text, ((DISPLAY_SIZE - title_text.get_rect().width) / 2, DISPLAY_SIZE / 2 - 60 -
                             title_text.get_rect().height))
    menu_height_range = [DISPLAY_SIZE / 2, DISPLAY_SIZE / 2 + medium_text.get_rect().height,
                         DISPLAY_SIZE / 2 + 2 * medium_text.get_rect().height,
                         DISPLAY_SIZE / 2 + 3 * medium_text.get_rect().height]
    menu_width_range = [(DISPLAY_SIZE - medium_text.get_rect().width) / 2,
                        (DISPLAY_SIZE + medium_text.get_rect().width) / 2]
    screen.blit(easy_text, (menu_width_range[0], menu_height_range[0]))
    screen.blit(medium_text, (menu_width_range[0], menu_height_range[1]))
    screen.blit(hard_text, (menu_width_range[0], menu_height_range[2]))
    screen.blit(credit_text,
                (DISPLAY_SIZE - credit_text.get_rect().width - 5, DISPLAY_SIZE - credit_text.get_rect().height - 5))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                opt = pygame.mouse.get_pos()
                if menu_width_range[0] < opt[0] < menu_width_range[1]:
                    if menu_height_range[0] < opt[1] < menu_height_range[1]:
                        return 3        # easy
                    if menu_height_range[1] < opt[1] < menu_height_range[2]:
                        return 4        # medium
                    if menu_height_range[2] < opt[1] < menu_height_range[3]:
                        return 5        # hard


def print_board(highlight=None, warning=None):
    for x in range(8):
        for y in range(8):
            if (x + y) % 2 == 0:
                pygame.draw.rect(screen, COLOR_WHITE, (x * UNIT_WIDTH, y * UNIT_WIDTH, UNIT_WIDTH, UNIT_WIDTH))
            else:
                pygame.draw.rect(screen, COLOR_BLACK, (x * UNIT_WIDTH, y * UNIT_WIDTH, UNIT_WIDTH, UNIT_WIDTH))

            if board_state[x][y] is not None:
                screen.blit(board_state[x][y].image, (x * UNIT_WIDTH, y * UNIT_WIDTH))

    if highlight is not None:
        pygame.draw.rect(screen, (180, 187, 0),
                         (highlight[0] * UNIT_WIDTH, highlight[1] * UNIT_WIDTH, UNIT_WIDTH, UNIT_WIDTH))
        # no need to check if there is a piece since it just moved there
        screen.blit(board_state[highlight[0]][highlight[1]].image,
                    (highlight[0] * UNIT_WIDTH, highlight[1] * UNIT_WIDTH))

    if warning is not None:
        pygame.draw.rect(screen, (180, 0, 0),
                         (warning[0] * UNIT_WIDTH, warning[1] * UNIT_WIDTH, UNIT_WIDTH, UNIT_WIDTH))
        # no need to check if there is a piece since it just moved there
        screen.blit(board_state[warning[0]][warning[1]].image,
                    (warning[0] * UNIT_WIDTH, warning[1] * UNIT_WIDTH))


def get_clicked_position():
    coordinates = pygame.mouse.get_pos()
    return int(coordinates[0] // UNIT_WIDTH), int(coordinates[1] // UNIT_WIDTH)


def print_markers(valid_moves):
    for move in valid_moves:
        centre = (int(move[0] * UNIT_WIDTH + UNIT_WIDTH / 2), int(move[1] * UNIT_WIDTH + UNIT_WIDTH / 2))
        pygame.draw.circle(screen, COLOR_MARKER, centre, 20)


def is_game_over(board, black, white, check):
    if check is 'b':
        king_ok = False
        for pos in black:
            if board[pos[0]][pos[1]].__class__.__name__ is "King":
                king_ok = True
                break
        if not king_ok:
            return 'w'

    elif check is 'w':
        king_ok = False
        for pos in white:
            if board[pos[0]][pos[1]].__class__.__name__ is "King":
                king_ok = True
                break
        if not king_ok:
            return 'b'

    return False


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


def handle_castling(board, piece_pos, all_pieces):
    if board[piece_pos[0]][piece_pos[1]].__class__.__name__ is "King":
        if board[piece_pos[0]][piece_pos[1]].can_castle:
            if piece_pos[0] == 6:
                board[5][7] = board[7][7]  # rook movement
                board[7][7] = None
                all_pieces[all_pieces.index((7, piece_pos[1]))] = (5, piece_pos[1])

            elif piece_pos[0] == 2:
                board[3][7] = board[0][7]  # rook movement
                board[0][7] = None
                all_pieces[all_pieces.index((0, piece_pos[1]))] = (3, piece_pos[1])
        board[piece_pos[0]][piece_pos[1]].can_castle = False

    if board[piece_pos[0]][piece_pos[1]].__class__.__name__ is "Rook" and board[piece_pos[0]][piece_pos[1]].can_castle:
        board[piece_pos[0]][piece_pos[1]].can_castle = False


def minimax(board, black, white, depth, alpha, beta, is_maximizing):
    if depth == 0 or is_game_over(board, black, white, 'w' if is_maximizing else 'b'):
        return get_point_sum(board), None

    for event in pygame.event.get():  # handle quitting during intervals
        if event.type == pygame.QUIT:
            sys.exit()

    if is_maximizing:
        max_val = -INFINITY
        play = None
        player = None
        for piece_pos in black:
            for move in board[piece_pos[0]][piece_pos[1]].get_moves(piece_pos, board):
                board_temp = get_copy(board)
                black_temp = black.copy()

                if len(move) == 2:
                    board_temp[move[0]][move[1]] = board_temp[piece_pos[0]][piece_pos[1]]
                    board_temp[piece_pos[0]][piece_pos[1]] = None
                    black_temp[black.index(piece_pos)] = move
                else:  # pawn promotion
                    board_temp[move[0]][move[1]] = move[2]('b')
                    board_temp[piece_pos[0]][piece_pos[1]] = None
                    black_temp[black.index(piece_pos)] = (move[0], move[1])  # remove third mem

                # handles any castling if there
                handle_castling(board_temp, piece_pos, black_temp)

                white_temp = white
                if (move[0], move[1]) in white:
                    white_temp = white.copy()
                    white_temp.remove((move[0], move[1]))

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
                white_temp = white.copy()

                if len(move) == 2:
                    board_temp[move[0]][move[1]] = board_temp[piece_pos[0]][piece_pos[1]]
                    board_temp[piece_pos[0]][piece_pos[1]] = None
                    white_temp[white.index(piece_pos)] = move

                else:
                    board_temp[move[0]][move[1]] = move[2]('w')
                    board_temp[piece_pos[0]][piece_pos[1]] = None
                    white_temp[white.index(piece_pos)] = (move[0], move[1])

                handle_castling(board_temp, piece_pos, white_temp)

                black_temp = black
                if (move[0], move[1]) in black:
                    black_temp = black.copy()
                    black_temp.remove((move[0], move[1]))
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


def handle_promotion_menu(position):
    if position[1] == 0 and board_state[position[0]][position[1]].__class__.__name__ is "Pawn":
        pygame.draw.rect(screen, (128, 0, 128), (155, 275, 330, 90))
        pygame.draw.rect(screen, (255, 255, 0), (160, 280, 320, 80))
        screen.blit(pygame.image.load(os.path.join(Path, "resources/knight_w.png")), (160, 280))
        screen.blit(pygame.image.load(os.path.join(Path, "resources/bishop_w.png")), (240, 280))
        screen.blit(pygame.image.load(os.path.join(Path, "resources/rook_w.png")), (320, 280))
        screen.blit(pygame.image.load(os.path.join(Path, "resources/queen_w.png")), (400, 280))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 280 <= mouse_pos[1] <= 360:
                        if 160 <= mouse_pos[0] <= 240:
                            board_state[position[0]][position[1]] = Knight('w')
                            return
                        if 240 <= mouse_pos[0] <= 320:
                            board_state[position[0]][position[1]] = Bishop('w')
                            return
                        if 320 <= mouse_pos[0] <= 400:
                            board_state[position[0]][position[1]] = Rook('w')
                            return
                        if 400 <= mouse_pos[0] <= 480:
                            board_state[position[0]][position[1]] = Queen('w')
                            return


pygame.display.set_caption("Say Chess!")
pygame.display.set_icon(pygame.image.load(os.path.join(Path, "resources/chess_icon.png")))
screen = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))
MINIMAX_DEPTH = get_difficulty_from_menu()

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

is_running = True
winner = None
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = get_clicked_position()
            if active_piece_pos is None:
                if board_state[pos[0]][pos[1]] is not None and board_state[pos[0]][pos[1]].color is 'w':
                    active_piece_pos = pos
                    open_slots = board_state[active_piece_pos[0]][active_piece_pos[1]].get_moves(pos, board_state)

                    # validating moves
                    to_remove = []
                    for pos in open_slots:
                        board_checker = get_copy(board_state)
                        board_checker[pos[0]][pos[1]] = board_checker[active_piece_pos[0]][active_piece_pos[1]]
                        board_checker[active_piece_pos[0]][active_piece_pos[1]] = None
                        if get_if_checked('w', board_checker):
                            to_remove.append(pos)
                    for pos in to_remove:
                        open_slots.remove(pos)
                    if len(open_slots) == 0:
                        active_piece_pos = None
                        open_slots = None
                        break

                    for i in range(len(open_slots)):
                        if len(open_slots[i]) != 2:   # is promotion pawn(contains 3 promotion moves as third member)
                            open_slots[i] = (open_slots[i][0], open_slots[i][1])
                    print_markers(open_slots)
                    pygame.display.update()

            else:
                if pos in open_slots:
                    # user move
                    board_state[pos[0]][pos[1]] = board_state[active_piece_pos[0]][active_piece_pos[1]]
                    board_state[active_piece_pos[0]][active_piece_pos[1]] = None
                    white_pieces[white_pieces.index(active_piece_pos)] = pos
                    if pos in black_pieces:
                        black_pieces.remove(pos)
                    handle_promotion_menu(pos)
                    handle_castling(board_state, pos, white_pieces)
                    warn_pos = get_if_checked('b', board_state, black_pieces, white_pieces)
                    active_piece_pos = None
                    open_slots = None
                    if is_game_over(board_state, black_pieces, white_pieces, 'b') is 'w':
                        winner = 'w'
                        is_running = False
                        break
                    print_board(highlight=pos, warning=warn_pos)
                    pygame.display.update()

                    # computer move
                    comp_move = minimax(board_state, black_pieces, white_pieces, MINIMAX_DEPTH, -INFINITY, INFINITY,
                                        True)

                    if comp_move[2] is not None and len(comp_move[2]) == 2:
                        board_state[comp_move[2][0]][comp_move[2][1]] = board_state[comp_move[1][0]][comp_move[1][1]]
                        board_state[comp_move[1][0]][comp_move[1][1]] = None
                        black_pieces[black_pieces.index(comp_move[1])] = comp_move[2]

                    else:  # promotion
                        board_state[comp_move[2][0]][comp_move[2][1]] = comp_move[2][2]('b')
                        board_state[comp_move[1][0]][comp_move[1][1]] = None
                        black_pieces[black_pieces.index(comp_move[1])] = (comp_move[2][0], comp_move[2][1])

                    if (comp_move[2][0], comp_move[2][1]) in white_pieces:
                        white_pieces.remove((comp_move[2][0], comp_move[2][1]))

                    handle_castling(board_state, comp_move[2], black_pieces)
                    warn_pos = get_if_checked('w', board_state, black_pieces, white_pieces)
                    if is_game_over(board_state, black_pieces, white_pieces, 'w') is 'b':
                        winner = 'b'
                        is_running = False
                        break
                    print_board(highlight=comp_move[2], warning=warn_pos)
                    pygame.display.update()

                else:
                    active_piece_pos = None
                    open_slots = None
                    print_board()
                    pygame.display.update()

screen.fill((0, 0, 0))
end_font = pygame.font.SysFont("Calibri.ttf", 40)
end_card = end_font.render("YOU WIN!" if winner is 'w' else "COMPUTER WINS!", True, (255, 255, 255))
screen.blit(end_card, ((640 - end_card.get_rect().width) / 2, (640 - end_card.get_rect().height) / 2))
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
