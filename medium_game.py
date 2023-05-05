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
        obstacles = [(4,5), (4,6), (4,7), (10,15), (11,15), (12,15), (13,15), (14,15), (15,15), (15,14), (15,13), (15,12), (15,11), (15,10)]  # tambahkan obstacle baru di sini
        for l in range(rows):
            x = x + sizeBtwn
            y = y + sizeBtwn
            
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

