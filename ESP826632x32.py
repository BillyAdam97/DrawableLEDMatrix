import pygame
import httplib2


http = httplib2.Http()
url = "<RouterIP>/setColor?"
urlr = "<RouterIP>/clear"
width = 800
win = pygame.display.set_mode((width,width))
pygame.display.set_caption("32x32 LED Matrix")
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
colors = [RED,GREEN,BLUE,WHITE]


class Square:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = row*width
        self.y = col*width
        self.color = BLACK
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

def makeGrid(rows,width):
    grid = []
    gap = width//rows
    for i in range(rows):
        line = []
        for j in range(rows):
            square = Square(i, j, gap, rows)
            line.append(square)
        grid.append(line)

    return grid

def drawGrid(win, rows, width):
    gap = width//rows

    for i in range(rows):
        pygame.draw.line(win, WHITE, (0, i*gap), (width, i * gap))
        pygame.draw.line(win, WHITE, (i * gap, 0), (i * gap, width))


def drawMap(win, grid, rows, width):
    win.fill(BLACK)

    for row in grid:
        for square in row:
            square.draw(win)
    drawGrid(win,rows,width)

def getClicked(pos, rows, width):
    gap = width//rows
    y,x = pos
    row = y//gap
    col = x//gap
    return row,col

def main(win, width):
    ans=''
    answer = []
    rows = 32
    run = True
    grid = makeGrid(rows, width)
    pygame.mouse.set_visible(False)
    ind = 0


    while run:
        drawMap(win,grid,rows,width)
        mousepos = pygame.mouse.get_pos()
        pygame.draw.circle(win,colors[ind],mousepos,5)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col = getClicked(pos, rows, width)
                if (grid[row][col].getColor()!=colors[ind]):
                    grid[row][col].setColor(colors[ind])
                    http.request(url + f"X={row}&Y={col}&red={colors[ind][0]}&green={colors[ind][1]}&blue={colors[ind][2]}", "GET")

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row,col = getClicked(pos,rows,width)
                if (grid[row][col].getColor()!=BLACK):
                    grid[row][col].setColor(BLACK)


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if ind==len(colors)-1:
                        ind=0
                    else:
                        ind+=1
                elif event.key == pygame.K_LEFT:
                    if ind==0:
                        ind = len(colors)-1
                    else:
                        ind-=1
                elif event.key == pygame.K_r:
                    http.request(urlr, "GET");
                    for i in grid:
                        for j in i:
                            j.setColor(BLACK)


    pygame.quit()

main(win,width)