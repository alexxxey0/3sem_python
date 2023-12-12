BLACK = (0, 0, 0)
NEON_GREEN = (57, 255, 20)
RED = (255, 0, 0)


'''
Accepts a square and current board state, returns True if the square is valid (not adjacent to any ship horizontally, vertically or diagonally)
Otherwise returns False
'''
def valid_square(square, ships):
    # adding these pairs of coordinaters to the square will give us all of the adjacent squares
    adjacent_squares = [[0, 0], [0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    out = [-1, 10]
    
    for i in adjacent_squares:
        if square["i"] + i[0] in out or square["j"] + i[1] in out:
            continue
        if ships[square["i"] + i[0]][square["j"] + i[1]] != 0:
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


'''
Function that takes a dictionary with player's hits and checks if any ship is fully destroyed.
If so, marks it as destroyed and returns the name of the ship. Otherwise, returns False.
'''
def check_if_destroyed(ship_hits):
    for key, value in ship_hits.items():
        if key == "ship4" and value == 4:
            ship_hits[key] = "destroyed"
            return key # return the ship which has been destroyed during this turn
        elif key in ("ship3_1", "ship3_2") and value == 3:
            ship_hits[key] = "destroyed"
            return key
        elif key in ("ship2_1", "ship2_2", "ship2_3") and value == 2:
            ship_hits[key] = "destroyed"
            return key
        elif key in ("ship1_1", "ship1_2", "ship1_3", "ship1_4") and value == 1:
            ship_hits[key] = "destroyed"
            return key
        
    return False