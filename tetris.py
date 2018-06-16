import pygame
import numpy as np
import random as rnd

scrw = 240
scrh = 600

tilesz = 20

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
cp_mv_left = False
cp_mv_right = False
cp_rotate = False
current_piece = pieces[0]

solid = [[(0,0,0) for i in range(tilew)] for j in range(tileh)]

score = 0

def draw_segment(pos, color):
    assert len(pos) == 2
    assert len(color) == 3

    pygame.draw.rect(screen, color, \
        pygame.Rect(pos[0]*tilesz, pos[1]*tilesz, tilesz, tilesz))
    pygame.draw.rect(screen, (0,0,0), \
        pygame.Rect(pos[0]*tilesz+2, pos[1]*tilesz+2, tilesz-4, tilesz-4))
    pygame.draw.rect(screen, color, \
        pygame.Rect(pos[0]*tilesz+4, pos[1]*tilesz+4, tilesz-8, tilesz-8))

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
                draw_segment((pos[0] + x, pos[1] + y), col)

def ck_collision(piece, pos):
    """
    check a piece for a collision at any given point
    returns:
    1 - collided
    0 - did not collide
    -1 - out of bounds x
    -2 - out of bounds y
    """
    assert len(pos) == 2

    for y in range(piece.shape[0]):
        for x in range(piece.shape[1]):
            if pos[0] + x < 0 or pos[0] + x > tilew - 1:
                return -1
            if pos[1] + y < 0 or pos[1] + y > tileh - 1:
                return -2
            if  piece[y][x] == 1 and \
                solid[pos[1] + y][pos[0] + x] != (0,0,0):
                return 1

    return 0

def gen_new_piece():
    global cp_x
    global cp_y
    global cp_color
    global current_piece
    global cp_speed

    cp_y = 0
    cp_x = int(tilew / 2)

    cp_speed = level_speed

    cp_color = colors[rnd.randint(0,len(colors)-1)]
    current_piece = np.rot90(pieces[rnd.randint(0,len(pieces)-1)], \
                    k=rnd.randint(0,3))


def solidify():
    global solid
    global score
    global level_speed

    for y in range(current_piece.shape[0]):
        for x in range(current_piece.shape[1]):
            if  current_piece[y][x] == 1:
                solid[cp_y + y][cp_x + x] = cp_color

    for y in range(len(solid)):
        full = True

        for x in range(len(solid[y])):
            if solid[y][x] == (0,0,0):
                full = False

        if full:
            score += 1
            level_speed -= 1
            del solid[y]
            solid.insert(0, [(0,0,0) for i in range(tilew)])

def handle_input():
    global cp_rotate
    global cp_speed
    global cp_mv_left
    global cp_mv_right
    global done

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]: done = True
    if pressed[pygame.K_UP]: cp_rotate = True

    if pressed[pygame.K_DOWN]:
        cp_speed = level_speed / 4
    else:
        cp_speed = level_speed

    if pressed[pygame.K_LEFT]:
        cp_mv_left = True
        cp_mv_right = False
    if pressed[pygame.K_RIGHT]:
        cp_mv_right = True
        cp_mv_left = False

def render():
    screen.fill((0, 0, 0))

    for y in range(len(solid)):
        for x in range(len(solid[y])):
            if solid[y][x] != (0,0,0):
                draw_segment((x,y), solid[y][x])

    draw_piece(current_piece, (cp_x, cp_y), cp_color)
    pygame.display.flip()

def logic():
    global cp_speed_counter
    global cp_x
    global cp_y
    global cp_mv_left
    global cp_mv_right
    global current_piece
    global cp_rotate

    cp_speed_counter+=1

    if cp_speed_counter >= cp_speed:
        cp_speed_counter = 0

        new_x = cp_x
        new_y = cp_y + 1
        collided = False

        if new_y + current_piece.shape[0] > tileh:
            new_y = cp_y
            collided = True

        new_piece = current_piece

        if cp_mv_left:
            if ck_collision(new_piece, (new_x-1, new_y)) == 0:
                new_x-=1
            cp_mv_left = False
        elif cp_mv_right:
            if ck_collision(new_piece, (new_x+1, new_y)) == 0:
                new_x+=1
            cp_mv_right = False

        if cp_rotate:
            if ck_collision(np.rot90(current_piece), (new_x, new_y)) == 0:
                new_piece = np.rot90(current_piece)
            cp_rotate = False

        if collided or ck_collision(new_piece, (new_x, new_y)):
            cp_x = new_x
            solidify()
            gen_new_piece()
        else:
            current_piece = new_piece
            cp_x=new_x
            cp_y=new_y

## init
rnd.seed()
pygame.init()
screen = pygame.display.set_mode((scrw, scrh))
pygame.display.set_caption("Tetris in Python")
gen_new_piece()

## main loop
clock = pygame.time.Clock()

while not done:
    handle_input()
    render()
    logic()
    clock.tick(60)
