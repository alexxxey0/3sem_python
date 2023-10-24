import pygame as pg
import numpy
from functions import *

WIDTH, HEIGHT = 1200, 700
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Epic Battleship")

pg.font.init()
def pixeloid(size):
    return pg.font.Font("fonts/pixeloid_sans.ttf", size)

BLACK = (0, 0, 0)
NEON_GREEN = (57, 255, 20)
RED = (255, 0, 0)

FPS = 30

clock = pg.time.Clock()
run = True
buttons = []

ships_placed = 0
ship_selected = False

# ships - 10x10 matrix that represents the placement of the ships (contains numbers 0 and 1)
# grid - 10x10 matrix that represents the visual state of the grid (contains grid square objects)

# Define a 10x10 matrix, that will represent placed ships (1 - ship, 0 - no ship)
ships = []
for i in range(10):
    ships.append([])
    for j in range(10):
        ships[i].append(0)

# Define the grid
grid = []
x, y = 350, 150
for i in range(10):
    grid.append([])
    for j in range(10):
        rect = pg.Rect(x, y, 50, 50)
        '''
            each square is represented by an object with the following properties:
            rect - the rect object associated with the square
            color - the color of the square
            width - outline thickness (0 to fill completely)
            i - i coordinate [0-9] (0,0 is the top left corner)
            j - j coordinate [0-9]
        '''
        grid[i].append({"rect": rect, "color": NEON_GREEN, "width": 2, "i": i, "j": j})
        x += 50
    y += 50
    x -= 500


p1_grid = []
p2_grid = []
grids = [p1_grid, p2_grid]
x, y = 50, 100
for player_grid in grids:
    for i in range(10):
        player_grid.append([])
        for j in range(10):
            rect = pg.Rect(x, y, 50, 50)
            '''
                each square is represented by an object with the following properties:
                rect - the rect object associated with the square
                color - the color of the square
                width - outline thickness (0 to fill completely)
                i - i coordinate [0-9] (0,0 is the top left corner)
                j - j coordinate [0-9]
            '''
            player_grid[i].append({"rect": rect, "color": NEON_GREEN, "width": 2, "i": i, "j": j})
            x += 50
        y += 50
        x -= 500

    x += 600
    y = 100



tab = "start" # starting tab
#tab = "player1_move"
while run:
    clock.tick(FPS)

    if tab == "start":
        # Drawing
        welcome_text = pixeloid(60).render("EPIC BATTLESHIP", True, NEON_GREEN)
        welcome_text_center = welcome_text.get_rect(center = (WIDTH / 2, 200))
        WIN.blit(welcome_text, welcome_text_center)

        start_text_border_outer = pg.Rect(0, 0, 200, 100)
        start_text_border_outer.center = (WIDTH / 2, 400)
        pg.draw.rect(WIN, NEON_GREEN, start_text_border_outer, 5)
        start_text = pixeloid(40).render("START", True, NEON_GREEN)
        start_text_center = start_text.get_rect(center = (WIDTH / 2, 400))
        WIN.blit(start_text, start_text_center)
        if start_text_border_outer not in buttons:
            buttons.append(start_text_border_outer)

        # Event handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("P1")
                print(numpy.matrix(p1_ships))
                print("P2")
                print(numpy.matrix(p2_ships))
                run = False
        
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if start_text_border_outer.collidepoint(event.pos):
                        tab = "player1_ships"
                        WIN.fill(BLACK)
                        buttons.remove(start_text_border_outer)

    
    elif tab == "player1_ships" or tab == "player2_ships":
        # Drawing
        place_ships_text = "Player 1, place your ships" if tab == "player1_ships" else "Player 2, place your ships"
        welcome_text = pixeloid(40).render(place_ships_text, True, NEON_GREEN)
        welcome_text_center = welcome_text.get_rect(center = (WIDTH / 2, 100))
        WIN.blit(welcome_text, welcome_text_center)

        reset_border = pg.Rect(0, 0, 150, 100)
        reset_border.center = (1025, 475)
        pg.draw.rect(WIN, RED, reset_border, 2)
        reset_text = pixeloid(26).render("RESET", True, RED)
        reset_text_center = reset_text.get_rect(center = (1025, 475))
        WIN.blit(reset_text, reset_text_center)
        if reset_border not in buttons:
            buttons.append(reset_border)

        for row in grid:
            for square in row:
                pg.draw.rect(WIN, square["color"], square["rect"], square["width"])

        # Event handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("P1")
                print(numpy.matrix(p1_ships))
                print("P2")
                print(numpy.matrix(p2_ships))
                run = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not ship_selected and ships_placed < 6:
                        '''
                            if the player clicks a square, and a ship is not currently selected,
                            fill the square with green and mark possible choices for ship placement with red
                            (for 1x1 ships, the player selects only 1 square, so we skip this step)
                        '''
                        for row in grid:
                            for square in row:
                                if square["rect"].collidepoint(event.pos) and valid_square(square, ships):
                                    square_selected = {"i": square["i"], "j": square["j"]}
                                    square["width"] = 0
                                    ship_selected = True

                                    if ships_placed < 1:
                                        offset = 3
                                    elif ships_placed < 3:
                                        offset = 2
                                    elif ships_placed < 6: 
                                        offset = 1

                                    if square["i"] >= offset and valid_square(grid[square["i"] - offset][square["j"]], ships):
                                        grid[square["i"] - offset][square["j"]]["color"] = RED
                                    if square["i"] <= 9 - offset and valid_square(grid[square["i"] + offset][square["j"]], ships):
                                        grid[square["i"] + offset][square["j"]]["color"] = RED
                                    if square["j"] >= offset and valid_square(grid[square["i"]][square["j"] - offset], ships):
                                        grid[square["i"]][square["j"] - offset]["color"] = RED
                                    if square["j"] <= 9 - offset and valid_square(grid[square["i"]][square["j"] +  offset], ships):
                                        grid[square["i"]][square["j"] +  offset]["color"] = RED


                    elif ships_placed < 10:
                        '''
                            if the player clicks a square, and a ship is currently selected,
                            fill the selected square, as well as all the squares in between with green (thus, drawing the whole ship)
                        '''
                        for row in grid:
                            for square in row:
                                if square["rect"].collidepoint(event.pos) and (square["color"] == RED or ships_placed >= 6) and valid_square(square, ships):
                                    square["color"] = NEON_GREEN
                                    square["width"] = 0
                                    ship_selected = False
                                    clear_red_squares(grid)

                                    if ships_placed >= 6:
                                        square_selected["i"] = square["i"]
                                        square_selected["j"] = square["j"]

                                    
                                    '''
                                        at this point the player has confirmed both the start and end points of the ship, so we do 2 things:
                                        1) fill the squares between the ones player has selected with green (thus, displaying the ship properly)
                                        2) add the ship to the 'ships' matrix
                                    '''
                                    if square["i"] != square_selected["i"]:
                                        for i in range(min(square["i"], square_selected["i"]), max(square["i"], square_selected["i"]) + 1):
                                            grid[i][square["j"]]["width"] = 0
                                            ships[i][square["j"]] = 1
                                    else:
                                        for j in range(min(square["j"], square_selected["j"]), max(square["j"], square_selected["j"]) + 1):
                                            grid[square["i"]][j]["width"] = 0
                                            ships[square["i"]][j] = 1

                                    ships_placed += 1
                                
                    # if the player has placed all 10 ships, display the confirm button
                    if ships_placed == 10:
                        confirm_border = pg.Rect(0, 0, 150, 100)
                        confirm_border.center = (1025, 600)
                        pg.draw.rect(WIN, NEON_GREEN, confirm_border, 2)
                        confirm_text = pixeloid(24).render("CONFIRM", True, NEON_GREEN)
                        confirm_text_center = confirm_text.get_rect(center = (1025, 600))
                        WIN.blit(confirm_text, confirm_text_center)
                        if confirm_border not in buttons:
                            buttons.append(confirm_border)
                    
                    # if player clicks reset, reset everything back to default
                    if reset_border.collidepoint(event.pos):
                        WIN.fill(BLACK)
                        ships_placed = 0
                        ship_selected = False
                        clear_board(grid)

                        if "confirm_border" in locals():
                            if confirm_border in buttons:
                                buttons.remove(confirm_border)

                        ships = clear_ships(ships)

                    # if player clicks confirm, save the ships matrix into a variable (p1_ships for player 1, p2_ships for player 2)
                    # as a result, we get 2 10x10 matrices, which represent the placement of players' ships
                    if "confirm_border" in locals():
                        if confirm_border.collidepoint(event.pos):
                            WIN.fill(BLACK)
                            if confirm_border in buttons:
                                buttons.remove(confirm_border)

                                if tab == "player1_ships":
                                    tab = "player2_ships"
                                    clear_board(grid)
                                    p1_ships = ships
                                elif tab == "player2_ships":
                                    tab = "player1_move"
                                    clear_board(grid)
                                    p2_ships = ships
                                    buttons.remove(reset_border)
                                    print(buttons)

                                ships_placed = 0
                                ship_selected = False
                                ships = clear_ships(ships)

    elif tab == "player1_move" or tab == "player2_move":
        WIN.fill(BLACK)
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        # Drawing
        place_ships_text = "Player 1, make your move ↓" if tab == "player1_move" else "↓ Player 2, make your move"
        welcome_text = pixeloid(40).render(place_ships_text, True, NEON_GREEN)
        welcome_text_center = welcome_text.get_rect(center = (WIDTH / 2, 50))
        WIN.blit(welcome_text, welcome_text_center)

        p1_text = pixeloid(40).render("Player 1", True, NEON_GREEN)
        p1_text_pos = p1_text.get_rect(center = (WIDTH / 4, 650))
        WIN.blit(p1_text, p1_text_pos)
        p2_text = pixeloid(40).render("Player 2", True, NEON_GREEN)
        p2_text_pos = p2_text.get_rect(center = (WIDTH * 3 / 4, 650))
        WIN.blit(p2_text, p2_text_pos)

        for player_grid in grids:
            for row in player_grid:
                for square in row:
                    pg.draw.rect(WIN, square["color"], square["rect"], square["width"])

        # Event handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("P1")
                print(numpy.matrix(p1_ships))
                print("P2")
                print(numpy.matrix(p2_ships))
                run = False

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and tab == "player1_move":
                for row in p2_grid:
                    for square in row:
                        if square["rect"].collidepoint(event.pos):
                            if p2_ships[square["i"]][square["j"]] == 1:
                                square["width"] = 0
                            else:
                                square["color"] = RED




    for button in buttons:
        if button.collidepoint(pg.mouse.get_pos()):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            break
        else:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    pg.display.update()

pg.quit()




