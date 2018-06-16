import pygame
import numpy as np

scrw = 300
scrh = 600

tilesz = 10

tilew = int(scrw/tilesz)
tileh = int(scrh/tilesz)

done = False

pieces = [
[ #L
[1,0],
[1,0],
[1,1]],

[ #J
[0,1],
[0,1],
[1,1]],

[ #I
[1],
[1],
[1],
[1]],

[ #sq
[1,1],
[1,1]],

[ #E
[1,0],
[1,1],
[1,0]],

[ #s
[1,0],
[1,1],
[0,1]],

[ #z
[0,1],
[1,1],
[1,0]]
];

pieces = [np.array(x) for x in pieces]

colors = [
(255,0,0),
(0,255,0),
(0,0,255),
(255,255,0),
(255,0,255),
(0,255,255),
(255,255,255)
]

#moving piece
level_speed = 20
cp_speed = 20 #ie 1 tile for every 20 ticks
cp_speed_counter = 0
cp_x = 0
cp_y = 0
cp_color = (255,0,0)
current_piece = pieces[0]

solid = [[(0,0,0) for i in range(tilew)] for j in range(tileh)]

def draw_segment(pos, color):
    assert len(pos) == 2
    assert len(color) == 3

    pygame.draw.rect(screen, color, pygame.Rect(pos[0], pos[1], tilesz, tilesz))
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(pos[0]+2, pos[1]+2, tilesz-4, tilesz-4))
    pygame.draw.rect(screen, color, pygame.Rect(pos[0]+4, pos[1]+4, tilesz-8, tilesz-8))

def draw_piece(piece, pos, col):
    """
    draw an entire piece from list with a given color and rotation
    NB! pos is in pixels
    """
    assert len(pos) == 2
    assert len(col) == 3

    for y in range(piece.shape[0]):
        for x in range(piece.shape[1]):
            if piece[y][x] == 1 :
                draw_segment((pos[0] + x*tilesz, pos[1] + y*tilesz), col)


def ck_pt_in_rect(pos1, pos2):
    assert len(pos1) == 2
    assert len(pos2) == 2

    if  pos1[0] >= pos2[0] and \
        pos1[0] <= pos2[0] + tilesz and \
        pos1[1] >= pos2[1] and \
        pos1[1] <= pos2[1] + tilesz:
        return True

    return False


def ck_tile_overlap(pos1, pos2):
    """
    check if two tiles overlap
    """
    assert len(pos1) == 2
    assert len(pos2) == 2

    if ck_pt_in_rect(pos1, pos2): return True
    if ck_pt_in_rect(np.array(pos1) + np.array([0,tilesz]), pos2): return True
    if ck_pt_in_rect(np.array(pos1) + np.array([tilesz,0]), pos2): return True
    if ck_pt_in_rect(np.array(pos1) + np.array([tilesz,tilesz]), pos2): return True

    return False


def ck_collision(piece, pos) :
    """
    check a piece for a collision at any given point
    NB! pos in pixels
    """
    assert len(pos) == 2

    for y in range(piece.shape[0]):
        for x in range(piece.shape[1]):
            if piece[y][x] == 1 :
                for i in range(len(solid)):
                    for j in range(len(solid[i])):
                        if solid[i][j] != (0,0,0):
                            ck_tile_overlap((pos[0] + x*tilesz, pos[1] + y*tilesz), \
                            (j*tilesz, i*tilesz))

def gen_new_piece():
    #set all cp_ params
    return True

def handle_input():
    global current_piece
    global cp_speed
    global cp_x
    global cp_y
    global done

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP]:
        current_piece = np.rot90(current_piece)

    if pressed[pygame.K_DOWN]:
        cp_speed = level_speed / 2
    else:
        cp_speed = level_speed

    if pressed[pygame.K_LEFT]: cp_x -= tilesz
    if pressed[pygame.K_RIGHT]: cp_x += tilesz
    if pressed[pygame.K_ESCAPE]: done = True

def render():
    screen.fill((0, 0, 0))

    # draw current piece
    draw_piece(current_piece, (cp_x, cp_y), cp_color)
    pygame.display.flip()

def logic():
    global cp_speed_counter
    global cp_x
    global cp_y

    #ck_collision(0,(0,0),0)

    cp_speed_counter+=1

    if cp_speed_counter >= cp_speed:
        cp_speed_counter = 0
        cp_y+=tilesz


## init
pygame.init()
screen = pygame.display.set_mode((scrw, scrh))

## main loop
clock = pygame.time.Clock()

while not done:
    handle_input()
    render()
    logic()
    clock.tick(60)
