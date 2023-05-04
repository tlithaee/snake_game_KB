import pygame
import sys

def run_game():

    class cube(object):
        rows = 20
        w = 500
        def __init__(self,start,dirnx=1,dirxny=0,color=(255,0,0), obstacle=False):
            self.pos = start
            self.dirnx = 1
            self.dirny = 0
            self.color = color
            self.obstacle = obstacle

        def draw(self, surface, eyes=False):
            dis = self.w // self.rows
            i = self.pos[0]
            j = self.pos[1]

            if self.obstacle:
                pygame.draw.rect(surface, (217, 217, 217), (i*dis+1, j*dis+1,dis+2,dis-2))
            else:
                pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1,dis+2,dis-2))
        
            if eyes:
                centre = dis//2
                radius = 3
                circleMiddle = (i*dis + centre-radius,j*dis+8)
                circleMiddle2 = (i*dis + dis -radius*2, j*dis + 8)
                pygame.draw.circle(surface,(255,255,255), circleMiddle, radius)
                pygame.draw.circle(surface,(255,255,255), circleMiddle2, radius)

    def drawGrid(w, rows, surface):
        sizeBtwn = w // rows
        x = 0
        y = 0
        obstacles = [(0,i) for i in range(rows)] + [(i,0) for i in range(rows)] + [(rows-1,i) for i in range(rows)] + [(i,rows-1) for i in range(rows)] + [(4,6), (5,6), (6,6), (7,6), (8,6), (9,6), (10,6), (10,6), (10,7), (10,8), (10,9), (10,10), (10,11), (10,12), (10,13), (10,14)]  # posisi obstacle pada batas-batas board
        for l in range(rows):
            x = x + sizeBtwn
            y = y + sizeBtwn
            # pygame.draw.line(surface, (255,255,255), (x,0),(x,w))  
            # pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
            
        for obstacle in obstacles:
            cube_obstacle = cube(obstacle, color=(0,0,255), obstacle=True)
            cube_obstacle.draw(surface)
            
    pygame.display.update()


    def redrawWindow(surface, width, rows):
        surface.fill((0,0,0))
        drawGrid(width, rows, surface)

    def main():
        pygame.init()
        width = 500
        rows = 20
        surface = pygame.display.set_mode((width,width))
        clock = pygame.time.Clock()  # objek clock untuk mengontrol framerate
        while True:  # gameloop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            surface.fill((85, 67, 63))
            drawGrid(width, rows, surface)
            pygame.display.update()
            clock.tick(60)  # framerate maksimum = 60 fps

    main()
