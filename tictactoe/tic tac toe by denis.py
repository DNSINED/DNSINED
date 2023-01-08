import pygame as pg
from pygame.locals import *
import time
import sys

pg.init()
XO = 'x'
winner = None
draw = False
width = 600
height = 600
square = 200
line_color = 5

blue = (0, 255, 255)
pink = (255, 0, 188)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
purple = (51, 0, 51)
dark_purple = (51, 0, 102)

fps = 60
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height + 50), 0, 32)
pg.display.set_caption("TIC TAC TOE by Denis")

board = [[None]*3,[None]*3,[None]*3]

opening = pg.image.load('x_o_startup.png')
x_img = pg.image.load('X_neon.png')
o_img = pg.image.load('O_neon.png')

x_img = pg.transform.scale(x_img, (160, 160))
o_img = pg.transform.scale(o_img, (160, 160))
opening = pg.transform.scale(opening, (width, height ))

font = pg.font.Font(None, 30)
text = font.render("!DNSINED'S PROPERTY!", bool(1), pink)
text_rect = text.get_rect(center=(width / 2 , height + 25))
screen.blit(text, text_rect)

def game_opening():
    screen.blit(opening, (0, 0))
    pg.display.update()
    time.sleep(3/2)
    screen.fill(dark_purple)

    pg.draw.line(screen, blue, (0, square), (width, square), line_color)
    pg.draw.line(screen, blue, (0, 2 * square), (width, 2 * square), line_color)
    pg.draw.line(screen, blue, (square, 0), (square, width), line_color)
    pg.draw.line(screen, blue, (2 * square, 0), (2 * square, width), line_color)
    draw_status()


def draw_status():
    global draw

    if winner is  None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = 'Game Draw!'

    font = pg.font.Font(None, 30)
    text = font.render(message, bool(1), (255, 255, 255))

    screen.fill((0, 0, 0), (0, 600, 600, 50))
    text_rect = text.get_rect(center=(width / 2 , height + 25))
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():
    global board, winner, draw

    for row in range(0, 3):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            winner = board[row][0]
            pg.draw.line(screen, pink, (0, (row + 1) * height / 3 - height / 6),
                         (width, (row + 1) * height / 3 - height / 6), 20)

            break

    for col in range(0, 3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            winner = board[0][col]
            pg.draw.line(screen, pink, ((col + 1) * width / 3 - width / 6, 0),
                         ((col + 1) * width / 3 - width / 6, height), 20)
            break

    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        winner = board[0][0]
        pg.draw.line(screen, pink, (10, 10), (590, 590), 20)

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        winner = board[0][2]
        pg.draw.line(screen, pink, (590, 10), (10, 590), 20)

    if all([all(row) for row in board]) and winner is None:
        draw = True
    draw_status()


def drawXO(row, col):
    global board, XO
    if row == 1:
        posx = 30
    if row == 2:
        posx = width / 3 + 30
    if row == 3:
        posx = width / 3 * 2 + 30

    if col == 1:
        posy = 30
    if col == 2:
        posy = height / 3 + 30
    if col == 3:
        posy = height / 3 * 2 + 30
    board[row - 1][col - 1] = XO
    if (XO == 'x'):
        screen.blit(x_img, (posy, posx))
        XO = 'o'
    else:
        screen.blit(o_img, (posy, posx))
        XO = 'x'
    pg.display.update()


def mouse_click():
    x, y = pg.mouse.get_pos()

    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    if row and col is not None:
        if board[row-1][col-1] is None:
            global XO
            drawXO(row, col)
            check_win()


def reset_game():
    global board, winner, XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    game_opening()
    winner = None
    board = [[None]*3,[None]*3,[None]*3]


game_opening()

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_click()
            if winner or draw:
                reset_game()

    pg.display.update()
    CLOCK.tick(fps)
