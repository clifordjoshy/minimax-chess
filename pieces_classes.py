import pygame

BOARD_DIMENSION = 8


def is_available(x, y, side, board_state):
    if 0 <= x < BOARD_DIMENSION and 0 <= y < BOARD_DIMENSION:
        if board_state[x][y] is None or board_state[x][y].dir_coeff != side:
            # either empty or opponents piece
            return True
    return False


class Pawn:
    def __init__(self, color):
        self.dir_coeff = 1 if color is 'b' else -1  # black playing down the board\
        self.color = color
        self.image = pygame.image.load("resources/pawn_" + color + ".png")
        self.points = 1 if color is 'b' else -1

    def get_moves(self, position, board_state):
        valid_moves = []
        if is_available(position[0], position[1] + self.dir_coeff, self.dir_coeff, board_state) and \
                board_state[position[0]][position[1] + self.dir_coeff] is None:
            valid_moves.append((position[0], position[1] + self.dir_coeff))

            # second one only if first is available
            if is_available(position[0], position[1] + 2 * self.dir_coeff, self.dir_coeff, board_state) and \
                    board_state[position[0]][position[1] + 2 * self.dir_coeff] is None:
                valid_moves.append((position[0], position[1] + 2 * self.dir_coeff))

        if is_available(position[0] - 1, position[1] + self.dir_coeff, self.dir_coeff, board_state) and \
                board_state[position[0] - 1][position[1] + self.dir_coeff] is not None:
            valid_moves.append((position[0] - 1, position[1] + self.dir_coeff))
        if is_available(position[0] + 1, position[1] + self.dir_coeff, self.dir_coeff, board_state) and \
                board_state[position[0] + 1][position[1] + self.dir_coeff] is not None:
            valid_moves.append((position[0] + 1, position[1] + self.dir_coeff))

        return valid_moves


class Rook:
    def __init__(self, color):
        self.dir_coeff = 1 if color is "b" else -1  # black playing down the board
        self.color = color
        self.image = pygame.image.load("resources/rook_" + color + ".png")
        self.points = 5 if color is 'b' else -5

    def get_moves(self, position, board_state):
        valid_moves = []

        # horizontal scanning
        for i in range(1, position[0] + 1):
            if is_available(position[0] - i, position[1], self.dir_coeff, board_state):
                valid_moves.append((position[0] - i, position[1]))
                if board_state[position[0] - i][position[1]] is not None:
                    break  # cant go through pieces
            else:
                break  # encountered own side pieces
        for i in range(position[0] + 1, BOARD_DIMENSION):
            if is_available(i, position[1], self.dir_coeff, board_state):
                valid_moves.append((i, position[1]))
                if board_state[i][position[1]] is not None:
                    break
            else:
                break

        # vertical scanning
        for i in range(1, position[1] + 1):
            if is_available(position[0], position[1] - i, self.dir_coeff, board_state):
                valid_moves.append((position[0], position[1] - i))
                if board_state[position[0]][position[1] - i] is not None:
                    break
            else:
                break
        for i in range(position[1] + 1, BOARD_DIMENSION):
            if is_available(position[0], i, self.dir_coeff, board_state):
                valid_moves.append((position[0], i))
                if board_state[position[0]][i] is not None:
                    break
            else:
                break

        return valid_moves


class Knight:
    def __init__(self, color):
        self.dir_coeff = 1 if color is "b" else -1  # black playing down the board
        self.color = color
        self.image = pygame.image.load("resources/knight_" + color + ".png")
        self.points = 3 if color is 'b' else -3

    def get_moves(self, position, board_state):
        valid_moves = []

        move_increments = [(-2, 1), (-2, -1), (2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for update in move_increments:
            if is_available(position[0] + update[0], position[1] + update[1], self.dir_coeff, board_state):
                valid_moves.append((position[0] + update[0], position[1] + update[1]))
        return valid_moves


class Bishop:
    def __init__(self, color):
        self.dir_coeff = 1 if color is "b" else -1  # black playing down the board
        self.color = color
        self.image = pygame.image.load("resources/bishop_" + color + ".png")
        self.points = 3 if color is 'b' else -3

    def get_moves(self, position, board_state):
        valid_moves = []
        pos_x = position[0] + 1
        pos_y = position[1] + 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x += 1
            pos_y += 1

        pos_x = position[0] - 1
        pos_y = position[1] - 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x -= 1
            pos_y -= 1

        pos_x = position[0] - 1
        pos_y = position[1] + 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x -= 1
            pos_y += 1

        pos_x = position[0] + 1
        pos_y = position[1] - 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x += 1
            pos_y -= 1

        return valid_moves


class Queen:
    def __init__(self, color):
        self.dir_coeff = 1 if color is "b" else -1  # black playing down the board
        self.color = color
        self.image = pygame.image.load("resources/queen_" + color + ".png")
        self.points = 10 if color is 'b' else -10

    def get_moves(self, position, board_state):  # rook + bishop
        valid_moves = []

        # horizontal scanning
        for i in range(1, position[0] + 1):
            if is_available(position[0] - i, position[1], self.dir_coeff, board_state):
                valid_moves.append((position[0] - i, position[1]))
                if board_state[position[0] - i][position[1]] is not None:
                    break  # cant go through pieces
            else:
                break  # encountered own side pieces
        for i in range(position[0] + 1, BOARD_DIMENSION):
            if is_available(i, position[1], self.dir_coeff, board_state):
                valid_moves.append((i, position[1]))
                if board_state[i][position[1]] is not None:
                    break
            else:
                break

        # vertical scanning
        for i in range(1, position[1] + 1):
            if is_available(position[0], position[1] - i, self.dir_coeff, board_state):
                valid_moves.append((position[0], position[1] - i))
                if board_state[position[0]][position[1] - i] is not None:
                    break
            else:
                break
        for i in range(position[1] + 1, BOARD_DIMENSION):
            if is_available(position[0], i, self.dir_coeff, board_state):
                valid_moves.append((position[0], i))
                if board_state[position[0]][i] is not None:
                    break
            else:
                break

        # diagonal scanning
        pos_x = position[0] + 1
        pos_y = position[1] + 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x += 1
            pos_y += 1

        pos_x = position[0] - 1
        pos_y = position[1] - 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x -= 1
            pos_y -= 1

        pos_x = position[0] - 1
        pos_y = position[1] + 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x -= 1
            pos_y += 1

        pos_x = position[0] + 1
        pos_y = position[1] - 1
        while is_available(pos_x, pos_y, self.dir_coeff, board_state):
            valid_moves.append((pos_x, pos_y))
            if board_state[pos_x][pos_y] is not None:
                break
            pos_x += 1
            pos_y -= 1

        return valid_moves


class King:
    def __init__(self, color):
        self.dir_coeff = 1 if color is "b" else -1  # black playing down the board
        self.color = color
        self.image = pygame.image.load("resources/king_" + color + ".png")
        self.points = 100 if color is 'b' else -100

    def get_moves(self, position, board_state):
        valid_moves = []
        move_increments = [(-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1)]

        for update in move_increments:
            if is_available(position[0] + update[0], position[1] + update[1], self.dir_coeff, board_state):
                valid_moves.append((position[0] + update[0], position[1] + update[1]))
        return valid_moves