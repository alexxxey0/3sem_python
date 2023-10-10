import pygame as pg
import classes

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

def main():
    clock = pg.time.Clock()
    run = True
    state = "title"
    grid_created = False

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

        if state == "player1_ships":
            welcome_text = pixeloid(40).render("Player 1, place your ships", True, NEON_GREEN)
            welcome_text_center = welcome_text.get_rect(center = (WIDTH / 2, 100))
            WIN.blit(welcome_text, welcome_text_center)



        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_text_border_outer.collidepoint(event.pos) and state == "title":
                        state = "player1_ships"
                        WIN.fill(BLACK)

            #if start_text_border_outer.collidepoint(pg.mouse.get_pos()):
            #    print("hover!")


        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()

