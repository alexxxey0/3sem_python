import pygame as pg
from functions import *

pg.mixer.pre_init(44100, -16, 2, 2048)
pg.mixer.init()
pg.init()

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

music_playing = True
music_icon = pg.image.load("background_music_icon.png")
MUSIC_ICON_SIZE = 50
music_icon = pg.transform.scale(music_icon, (MUSIC_ICON_SIZE, MUSIC_ICON_SIZE))
music_icon_rect = music_icon.get_rect(topleft = (10, 10))

sfx_playing = True
sfx_text = pixeloid(40).render("SFX", True, NEON_GREEN)
sfx_text_topleft = sfx_text.get_rect(topleft = (80, 10))
sfx_text_rect = pg.Rect(80, 10, 80 + sfx_text_topleft.width, 10 + sfx_text_topleft.height)
buttons = [music_icon_rect, sfx_text_topleft]

ships_placed = 0
ship_selected = False

# ships_matrix - 10x10 matrix that represents the placement of the ships
# grid - 10x10 matrix that represents the visual state of the grid (contains grid square objects)

# Define a 10x10 matrix, that will represent placed ships
ships_matrix = []
for i in range(10):
    ships_matrix.append([])
    for j in range(10):
        ships_matrix[i].append(0)

# for testing
'''p1_ships = [['ship4', 'ship4', 'ship4', 'ship4', 0, 0, 'ship3_1', 'ship3_1', 'ship3_1', 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        ['ship3_2', 0, 0, 'ship2_1', 0, 0, 'ship2_2', 0, 0, 'ship2_3'],
                        ['ship3_2', 0, 0, 'ship2_1', 0, 0, 'ship2_2', 0, 0, 'ship2_3'],
                        ['ship3_2', 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        ['ship1_1', 0, 'ship1_2', 0, 'ship1_3', 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 'ship1_4', 0]] 

p2_ships = [['ship4', 'ship4', 'ship4', 'ship4', 0, 0, 'ship3_1', 'ship3_1', 'ship3_1', 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        ['ship3_2', 0, 0, 'ship2_1', 0, 0, 'ship2_2', 0, 0, 'ship2_3'],
                        ['ship3_2', 0, 0, 'ship2_1', 0, 0, 'ship2_2', 0, 0, 'ship2_3'],
                        ['ship3_2', 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        ['ship1_1', 0, 'ship1_2', 0, 'ship1_3', 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 'ship1_4', 0]]'''

# Define the grid for players to place their ships
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
            i - i coordinate (horizontal) [0-9] (0,0 is the top left corner)
            j - j coordinate (vertical) [0-9]
        '''
        grid[i].append({"rect": rect, "color": NEON_GREEN, "width": 2, "i": i, "j": j})
        x += 50
    y += 50
    x -= 500


# Define the grids for players to attack
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
                i - i coordinate (horizontal) [0-9] (0,0 is the top left corner)
                j - j coordinate (vertical) [0-9]
            '''
            player_grid[i].append({"rect": rect, "color": NEON_GREEN, "width": 2, "i": i, "j": j})
            x += 50
        y += 50
        x -= 500

    x += 600
    y = 100

# Information about players' hits (necessary to tell if a ship is fully destroyed)
p1_ship_hits = {"ship4": 0, # ship name: how many times this ship was hit
           "ship3_1": 0,
           "ship3_2": 0,
           "ship2_1": 0,
           "ship2_2": 0,
           "ship2_3": 0,
           "ship1_1": 0,
           "ship1_2": 0,
           "ship1_3": 0,
           "ship1_4": 0
           }

p2_ship_hits = {"ship4": 0,
           "ship3_1": 0,
           "ship3_2": 0,
           "ship2_1": 0,
           "ship2_2": 0,
           "ship2_3": 0,
           "ship1_1": 0,
           "ship1_2": 0,
           "ship1_3": 0,
           "ship1_4": 0
           }

# Information about players' total hits (destroying all ships == 20 hits)
p1_hits = 0
p2_hits = 0

ship_names = {
    1: "ship4", # first ship that is placed
    2: "ship3_1", # second ship that is placed etc. (each of the 10 ships has a unique name)
    3: "ship3_2",
    4: "ship2_1",
    5: "ship2_2",
    6: "ship2_3",
    7: "ship1_1",
    8: "ship1_2",
    9: "ship1_3",
    10: "ship1_4"
}

pg.mixer.music.load("main_menu.mp3")
confirm_sound = pg.mixer.Sound("confirm.mp3")
reset_sound = pg.mixer.Sound("reset.mp3")
ship_placing_sound_1 = pg.mixer.Sound("ship_placing_1.mp3")
ship_placing_sound_2 = pg.mixer.Sound("ship_placing_2.mp3")
ship_hit_sound = pg.mixer.Sound("ship_hit.mp3")
ship_destroyed_sound = pg.mixer.Sound("ship_destroyed.mp3")
ship_missed_sound = pg.mixer.Sound("ship_missed.mp3")
victory_sound = pg.mixer.Sound("victory.mp3")
pg.mixer.music.play(loops=-1) # play music on repeat
pg.mixer.music.set_volume(0.3)

sounds = [confirm_sound, reset_sound, ship_placing_sound_1, ship_placing_sound_2, ship_hit_sound, ship_destroyed_sound, ship_missed_sound, victory_sound]

tab = "start" # starting tab
#tab = "player1_move"


# Main game loop
while run:
    clock.tick(FPS)

    pg_events = pg.event.get()

    if tab == "start":
        # Drawing
        WIN.fill(BLACK)
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

        created_by_text = pixeloid(32).render("Created by Alexey Gorlovich, 2023", True, NEON_GREEN)
        created_by_text_center = created_by_text.get_rect(center = (WIDTH / 2, 650))
        WIN.blit(created_by_text, created_by_text_center)

        # Event handler
        for event in pg_events:
            if event.type == pg.QUIT:
                run = False
        
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and start_text_border_outer.collidepoint(pg.mouse.get_pos()):
                pg.mixer.Sound.play(confirm_sound)
                tab = "player1_ships"
                WIN.fill(BLACK)
                buttons.remove(start_text_border_outer)

                # Changing background music
                music_playing = False if music_playing == False else True
                pg.mixer.music.stop()
                pg.mixer.music.unload()
                pg.mixer.music.load("placing_ships.mp3")
                pg.mixer.music.play(loops=-1)
                pg.mixer.music.set_volume(0.3)
                if not music_playing:
                    pg.mixer.music.pause()
    
    elif tab == "player1_ships" or tab == "player2_ships":
        # Drawing
        WIN.fill(BLACK)
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

        ship_count = {4: 0 if ships_placed == 0 else 1,
                      3: 2 if ships_placed >= 3 else ships_placed - 1,
                      2: 3 if ships_placed >= 6 else ships_placed - 3,
                      1: 4 if ships_placed == 10 else ships_placed - 6}
        for key in ship_count:
            if ship_count[key] < 0:
                ship_count[key] = 0

        ships_placed_texts = [[f"4x1 ships placed: {ship_count[4]} / 1", ship_count[4] == 1],
                              [f"3x1 ships placed: {ship_count[3]} / 2", ship_count[3] == 2],
                              [f"2x1 ships placed: {ship_count[2]} / 3", ship_count[2] == 3],
                              [f"1x1 ships placed: {ship_count[1]} / 4", ship_count[1] == 4]]
        
        y = 200
        for i in ships_placed_texts:
            text = pixeloid(18).render(i[0], True, NEON_GREEN if i[1] else RED)
            text_center = text.get_rect(center = (1025, y))
            WIN.blit(text, text_center)
            y += 50

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

        for row in grid:
            for square in row:
                pg.draw.rect(WIN, square["color"], square["rect"], square["width"])

        # Event handler
        for event in pg_events:
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if not ship_selected and ships_placed < 6:
                    '''
                        if the player clicks a square, and a ship is not currently selected,
                        fill the square with green and mark possible choices for ship placement with red
                        (for 1x1 ships, the player selects only 1 square, so we skip this step)
                    '''
                    for row in grid:
                        for square in row:
                            if square["rect"].collidepoint(pg.mouse.get_pos()) and valid_square(square, ships_matrix):
                                pg.mixer.Sound.play(ship_placing_sound_1)
                                valid_options = False

                                if ships_placed < 1:
                                    offset = 3
                                elif ships_placed < 3:
                                    offset = 2
                                elif ships_placed < 6: 
                                    offset = 1
                                    
                                if square["i"] >= offset and valid_square(grid[square["i"] - offset][square["j"]], ships_matrix):
                                    grid[square["i"] - offset][square["j"]]["color"] = RED
                                    valid_options = True
                                if square["i"] <= 9 - offset and valid_square(grid[square["i"] + offset][square["j"]], ships_matrix):
                                    grid[square["i"] + offset][square["j"]]["color"] = RED
                                    valid_options = True
                                if square["j"] >= offset and valid_square(grid[square["i"]][square["j"] - offset], ships_matrix):
                                    grid[square["i"]][square["j"] - offset]["color"] = RED
                                    valid_options = True
                                if square["j"] <= 9 - offset and valid_square(grid[square["i"]][square["j"] +  offset], ships_matrix):
                                    grid[square["i"]][square["j"] +  offset]["color"] = RED
                                    valid_options = True

                                if valid_options:
                                    square_selected = {"i": square["i"], "j": square["j"]}
                                    square["width"] = 0
                                    ship_selected = True

                elif ships_placed < 10:
                    '''
                        if the player clicks a square, and a ship is currently selected,
                        fill the selected square, as well as all the squares in between with green (thus, drawing the whole ship)
                    '''
                    for row in grid:
                        for square in row:
                            if square["rect"].collidepoint(pg.mouse.get_pos()) and (square["color"] == RED or ships_placed >= 6) and valid_square(square, ships_matrix):
                                pg.mixer.Sound.play(ship_placing_sound_2)
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
                                    2) add the ship to the 'ships_matrix' matrix
                                '''
                                if square["i"] != square_selected["i"]:
                                    for i in range(min(square["i"], square_selected["i"]), max(square["i"], square_selected["i"]) + 1):
                                        grid[i][square["j"]]["width"] = 0
                                        ships_matrix[i][square["j"]] = ship_names[ships_placed + 1]
                                else:
                                    for j in range(min(square["j"], square_selected["j"]), max(square["j"], square_selected["j"]) + 1):
                                        grid[square["i"]][j]["width"] = 0
                                        ships_matrix[square["i"]][j] = ship_names[ships_placed + 1]

                                ships_placed += 1
                
                # if player clicks reset, reset everything back to default
                if reset_border.collidepoint(pg.mouse.get_pos()):
                    pg.mixer.Sound.play(reset_sound)
                    WIN.fill(BLACK)
                    ships_placed = 0
                    ship_selected = False
                    clear_board(grid)

                    if ("confirm_border" in locals()) and (confirm_border in buttons):
                        buttons.remove(confirm_border)

                    ships_matrix = clear_ships(ships_matrix)

                # if player clicks confirm, save the ships_matrix matrix into a variable (p1_ships for player 1, p2_ships for player 2)
                # as a result, we get 2 10x10 matrices, which represent the placement of players' ships
                if ("confirm_border" in locals()) and (confirm_border in buttons) and confirm_border.collidepoint(pg.mouse.get_pos()) and ships_placed == 10:
                    pg.mixer.Sound.play(confirm_sound)
                    WIN.fill(BLACK)
                    buttons.remove(confirm_border)

                    if tab == "player1_ships":
                        tab = "player2_ships"
                        clear_board(grid)
                        p1_ships = ships_matrix
                    elif tab == "player2_ships":
                        # Changing background music
                        music_playing = False if music_playing == False else True
                        pg.mixer.music.stop()
                        pg.mixer.music.unload()
                        pg.mixer.music.load("battle_music.mp3")
                        pg.mixer.music.play(loops=-1)
                        pg.mixer.music.set_volume(0.3)
                        if not music_playing:
                            pg.mixer.music.pause()

                        tab = "player1_move"
                        clear_board(grid)
                        p2_ships = ships_matrix
                        buttons.remove(reset_border)

                    ships_placed = 0
                    ship_selected = False
                    ships_matrix = clear_ships(ships_matrix)

            # Highlighting the square that the user is hovering over
            for row in grid:
                for square in row:
                    if ship_selected:
                        if square_selected["i"] == square["i"] and square_selected["j"] == square["j"]:
                            square["width"] = 0
                        elif square["rect"].collidepoint(pg.mouse.get_pos()) and square["color"] == RED:
                            square["width"] = 5
                        elif square["color"] == RED:
                            square["width"] = 2

                    else:
                        if square["rect"].collidepoint(pg.mouse.get_pos()) and valid_square(square, ships_matrix) and ships_placed != 10:
                            square["width"] = 5
                        else:
                            if ships_matrix[square["i"]][square["j"]] != 0:
                                square["width"] = 0
                            else:
                                square["width"] = 2

    elif tab == "player1_move" or tab == "player2_move":
        # Drawing
        WIN.fill(BLACK)

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
        for event in pg_events:
            if event.type == pg.QUIT:
                run = False

            if p1_hits == 20 or p2_hits == 20:
                # Changing background music
                pg.mixer.music.stop()
                pg.mixer.music.unload()
                pg.mixer.Sound.play(victory_sound)
                tab = "win"

            # Player 1 attacking
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and tab == "player1_move":
                for row in p2_grid:
                    for square in row:
                        if square["rect"].collidepoint(pg.mouse.get_pos()) and square["color"] != RED and square["width"] != 0:

                            if p2_ships[square["i"]][square["j"]] != 0:
                                square["width"] = 0
                                p1_ship_hits[p2_ships[square["i"]][square["j"]]] += 1
                                p1_hits += 1
                                destroyed_ship = check_if_destroyed(p1_ship_hits)

                                if destroyed_ship: # if the player has fully destroyed a ship during this turn, marks all of the adjacent squares to this ship with red (since no ships can be there anyway)
                                    pg.mixer.Sound.play(ship_destroyed_sound)
                                    adjacent_squares = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
                                    out = [-1, 10]
                                    for row in p2_grid:
                                        for square in row:
                                            for i in adjacent_squares:
                                                if square["i"] + i[0] in out or square["j"] + i[1] in out:
                                                    continue
                                                if p2_ships[square["i"] + i[0]][square["j"] + i[1]] == destroyed_ship and p2_ships[square["i"]][square["j"]] == 0:
                                                    square["color"] = RED
                                                    break
                                else:
                                    pg.mixer.Sound.play(ship_hit_sound)

                            else:
                                pg.mixer.Sound.play(ship_missed_sound)
                                square["color"] = RED
                                tab = "player2_move"

            # Player 2 attacking
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and tab  == "player2_move":
                for row in p1_grid:
                    for square in row:
                        if square["rect"].collidepoint(pg.mouse.get_pos()) and square["color"] != RED and square["width"] != 0:

                            if p1_ships[square["i"]][square["j"]] != 0:
                                square["width"] = 0
                                p2_ship_hits[p1_ships[square["i"]][square["j"]]] += 1
                                p2_hits += 1
                                destroyed_ship = check_if_destroyed(p2_ship_hits)

                                if destroyed_ship: # if the player has fully destroyed a ship during this turn, marks all of the adjacent squares to this ship with red (since no ships can be there anyway)
                                    pg.mixer.Sound.play(ship_destroyed_sound)
                                    adjacent_squares = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
                                    out = [-1, 10]
                                    for row in p1_grid:
                                        for square in row:
                                            for i in adjacent_squares:
                                                if square["i"] + i[0] in out or square["j"] + i[1] in out:
                                                    continue
                                                if p1_ships[square["i"] + i[0]][square["j"] + i[1]] == destroyed_ship and p1_ships[square["i"]][square["j"]] == 0:
                                                    square["color"] = RED
                                                    break
                                else:
                                    pg.mixer.Sound.play(ship_hit_sound)

                            else:
                                pg.mixer.Sound.play(ship_missed_sound)
                                square["color"] = RED
                                tab = "player1_move"

    elif tab == "win":
        # Drawing
        WIN.fill(BLACK)

        win_rect_outer = pg.Rect(0, 0, 510, 370)
        win_rect_outer.center = (600, 300)
        pg.draw.rect(WIN, RED, win_rect_outer)
        win_rect = pg.Rect(0, 0, 490, 350)
        win_rect.center = (600, 300)
        pg.draw.rect(WIN, BLACK, win_rect)

        win_text = pixeloid(40).render("Player 1 won!" if p1_hits == 20 else "Player 2 won!", True, NEON_GREEN)
        win_text_center = win_text.get_rect(center = (WIDTH / 2, 250))
        WIN.blit(win_text, win_text_center)

        new_game_border_outer = pg.Rect(0, 0, 300, 100)
        new_game_border_outer.center = (WIDTH / 2, 400)
        pg.draw.rect(WIN, NEON_GREEN, new_game_border_outer, 5)
        new_game = pixeloid(40).render("NEW GAME", True, NEON_GREEN)
        new_game_center = new_game.get_rect(center = (WIDTH / 2, 400))
        WIN.blit(new_game, new_game_center)
        if new_game_border_outer not in buttons:
            buttons.append(new_game_border_outer)

        # Event handler
        for event in pg_events:
            if event.type == pg.QUIT:
                run = False

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if ("new_game_border_outer" in locals()) and (new_game_border_outer.collidepoint(pg.mouse.get_pos())):
                    # Resetting everything back to default

                    clear_board(grid)
                    clear_board(p1_grid)
                    clear_board(p2_grid)
                    buttons = [music_icon_rect]
                    p1_ship_hits = {"ship4": 0,
                            "ship3_1": 0,
                            "ship3_2": 0,
                            "ship2_1": 0,
                            "ship2_2": 0,
                            "ship2_3": 0,
                            "ship1_1": 0,
                            "ship1_2": 0,
                            "ship1_3": 0,
                            "ship1_4": 0
                            }

                    p2_ship_hits = {"ship4": 0,
                            "ship3_1": 0,
                            "ship3_2": 0,
                            "ship2_1": 0,
                            "ship2_2": 0,
                            "ship2_3": 0,
                            "ship1_1": 0,
                            "ship1_2": 0,
                            "ship1_3": 0,
                            "ship1_4": 0
                            }
                    p1_hits = 0
                    p2_hits = 0
                    tab = "start"

                    # Changing background music
                    music_playing = False if music_playing == False else True
                    pg.mixer.music.load("main_menu.mp3")
                    pg.mixer.music.play(loops=-1)
                    pg.mixer.music.set_volume(0.3)
                    if not music_playing:
                        pg.mixer.music.pause()
    
    # Handling background music
    if music_playing:
        WIN.blit(music_icon, (10, 10))
    else:
        WIN.blit(music_icon, (10, 10))
        pg.draw.line(WIN, NEON_GREEN, (10, 10), (10 + MUSIC_ICON_SIZE, 10 + MUSIC_ICON_SIZE), 4)

    for event in pg_events:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and music_icon_rect.collidepoint(pg.mouse.get_pos()):
            if music_playing:
                pg.mixer.music.pause()
                music_playing = False
            else:
                pg.mixer.music.unpause()
                music_playing = True

    # Handling sound effects (sfx)
    if sfx_playing:
        WIN.blit(sfx_text, sfx_text_topleft)
    else:
        WIN.blit(sfx_text, sfx_text_topleft)
        pg.draw.line(WIN, NEON_GREEN, (80, 10), (80 + sfx_text_topleft.width, 10 + sfx_text_topleft.height), 4)

    for event in pg_events:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and sfx_text_rect.collidepoint(pg.mouse.get_pos()):
            if sfx_playing:
                for sound in sounds:
                    pg.mixer.Sound.set_volume(sound, 0)
                sfx_playing = False
            else:
                for sound in sounds:
                    pg.mixer.Sound.set_volume(sound, 1)
                sfx_playing = True



    # Change the cursor when player hovers over a button
    for button in buttons:
        if button.collidepoint(pg.mouse.get_pos()):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            break
    else:
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    pg.display.update()

pg.quit()