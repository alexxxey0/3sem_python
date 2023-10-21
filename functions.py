BLACK = (0, 0, 0)
NEON_GREEN = (57, 255, 20)
RED = (255, 0, 0)


'''
Accepts a square and current board state, returns True if the square is valid (not adjacent to any ship horizontally, vertically or diagonally)
Otherwise returns False
'''
def valid_square(square, ships):
    x = [[0, 0], [0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    out = [-1, 10]
    
    for i in x:
        if square["i"] + i[0] in out or square["j"] + i[1] in out:
            continue
        if ships[square["i"] + i[0]][square["j"] + i[1]] == 1:
            return False
    return True


# resets 10x10 matrix back to all 0's
def clear_ships(ships):
    ships = []
    for i in range(10):
        ships.append([])
        for j in range(10):
            ships[i].append(0)
    
    return ships


# resets the board back to default
def clear_board(grid):
    for row in grid:
        for square in row:
            square["color"] = NEON_GREEN
            square["width"] = 2


# clears the board of any red squares
def clear_red_squares(grid):
    for row in grid:
        for square in row:
            if square["color"] == RED:
                square["color"] = NEON_GREEN


