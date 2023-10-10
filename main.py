import pygame as pg
import numpy

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

def clear_red_squares(grid):
    for row in grid:
        for square in row:
            if square["color"] == RED:
                square["color"] = NEON_GREEN

def valid_square(square, ships):
    x = [[0, 0], [0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    out = [-1, 10]
    
    for i in x:
        if square["i"] + i[0] in out or square["j"] + i[1] in out:
            continue
        if ships[square["i"] + i[0]][square["j"] + i[1]] == 1:
            return False
    return True
    

def main():
    clock = pg.time.Clock()
    run = True
    state = "title" # initial state of the game (title screen)
    grid_created = False

    ships_placed = 0
    ship_selected = False

    ships = []
    for i in range(10):
        ships.append([])
        for j in range(10):
            ships[i].append(0)

    while run:
        clock.tick(FPS)

        WIN.fill(BLACK)
        
        if state == "title":
            # Welcome text and start button
            welcome_text = pixeloid(60).render("EPIC BATTLESHIP", True, NEON_GREEN)
            welcome_text_center = welcome_text.get_rect(center = (WIDTH / 2, 200))
            WIN.blit(welcome_text, welcome_text_center)

            start_text_border_outer = pg.Rect(0, 0, 200, 100)
            start_text_border_outer.center = (WIDTH / 2, 400)
            pg.draw.rect(WIN, NEON_GREEN, start_text_border_outer, 5)

            start_text = pixeloid(40).render("START", True, NEON_GREEN)
            start_text_center = start_text.get_rect(center = (WIDTH / 2, 400))
            WIN.blit(start_text, start_text_center)

        elif state == "player1_ships":
            welcome_text = pixeloid(40).render("Player 1, place your ships", True, NEON_GREEN)
            welcome_text_center = welcome_text.get_rect(center = (WIDTH / 2, 100))
            WIN.blit(welcome_text, welcome_text_center)

            if not grid_created:
                # Create the grid
                grid = []
                x, y = 350, 150

                for i in range(10):
                    grid.append([])
                    for j in range(10):
                        rect = pg.Rect(x, y, 50, 50)
                        grid[i].append({"rect": rect, "color": NEON_GREEN, "width": 2, "i": i, "j": j})
                        x += 50
                    y += 50
                    x -= 500

                grid_created = True

            # Draw the grid
            for row in grid:
                for square in row:
                    pg.draw.rect(WIN, square["color"], square["rect"], square["width"])



        for event in pg.event.get():
            if event.type == pg.QUIT:
                print(numpy.matrix(ships))
                run = False
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if start_text_border_outer.collidepoint(event.pos) and state == "title":
                        state = "player1_ships"
                        WIN.fill(BLACK)

                    elif state == "player1_ships" and ships_placed < 10:

                        if not ship_selected and ships_placed < 6:
                            for row in grid:
                                for square in row:
                                    if square["rect"].collidepoint(event.pos) and valid_square(square, ships):
                                        square_selected = {"i": square["i"], "j": square["j"]}
                                        square["width"] = 0
                                        ship_selected = True

                                        # Mark squares, where it is possible to place the ship with red
                                        if ships_placed < 1:
                                            offset = 3
                                        elif ships_placed < 3:
                                            offset = 2
                                        elif ships_placed < 6: 
                                            offset = 1
                                        else:
                                            offset = 0

                                        if square["i"] >= offset and valid_square(grid[square["i"] - offset][square["j"]], ships):
                                            grid[square["i"] - offset][square["j"]]["color"] = RED
                                        if square["i"] <= 9 - offset and valid_square(grid[square["i"] + offset][square["j"]], ships):
                                            grid[square["i"] + offset][square["j"]]["color"] = RED
                                        if square["j"] >= offset and valid_square(grid[square["i"]][square["j"] - offset], ships):
                                            grid[square["i"]][square["j"] - offset]["color"] = RED
                                        if square["j"] <= 9 - offset and valid_square(grid[square["i"]][square["j"] +  offset], ships):
                                            grid[square["i"]][square["j"] +  offset]["color"] = RED


                        else:
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

                                        if square["i"] != square_selected["i"]:
                                            for i in range(min(square["i"], square_selected["i"]), max(square["i"], square_selected["i"]) + 1):
                                                grid[i][square["j"]]["width"] = 0
                                                ships[i][square["j"]] = 1
                                        else:
                                            for j in range(min(square["j"], square_selected["j"]), max(square["j"], square_selected["j"]) + 1):
                                                grid[square["i"]][j]["width"] = 0
                                                ships[square["i"]][j] = 1

                                        ships_placed += 1
                                        
                                



            #if start_text_border_outer.collidepoint(pg.mouse.get_pos()):
            #    print("hover!")


        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()

