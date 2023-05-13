import pygame
import sys
import random
from blessed import Terminal

def run_game():

    class Cube(object): #membuat objek cube pada game.
        rows = 20
        w = 500
        
        def __init__(self,start,dirnx=1,dirxny=0,color=(255,0,0), obstacle=False): #constructor 
            self.pos = start
            self.dirnx = 1
            self.dirny = 0
            self.color = color
            self.obstacle = obstacle

        def draw(self, surface, eyes=False):
            dis = self.w // self.rows
            i = self.pos[0]
            j = self.pos[1]

            if not self.obstacle:
                apple_image = pygame.image.load("assets/apple.png")
                apple_image = pygame.transform.scale(apple_image, (dis - 2, dis - 2))
                surface.blit(apple_image, (i * dis + 1, j * dis + 1))

                if eyes:
                    centre = dis // 2
                    radius = 3
                    circleMiddle = (i * dis + centre - radius, j * dis + 8)
                    circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
                    pygame.draw.circle(surface, (255, 255, 255), circleMiddle, radius)
                    pygame.draw.circle(surface, (255, 255, 255), circleMiddle2, radius)
            else:
                pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

    def drawGrid(surface, rows, width, obstacles):
        sizeBtwn = width // rows

        for obstacle in obstacles:
            if not obstacle.obstacle:
                obstacle.draw(surface)

        for obstacle in obstacles:
            if obstacle.obstacle:
                obstacle.draw(surface)

    def redrawWindow(surface, width, rows):
        surface.fill((0,0,0))
        drawGrid(width, rows, surface)

    def main():
        pygame.init()
        width = 500
        rows = 20
        surface = pygame.display.set_mode((width,width))
        clock = pygame.time.Clock()  # objek clock untuk mengontrol framerate
        
        obstacles = [
            Cube((0, i), color=(217, 217, 217), obstacle=True) for i in range(rows)
        ]  # Batas kiri
        obstacles.extend([Cube((i, 0), color=(217, 217, 217), obstacle=True) for i in range(rows)])  # Batas atas
        obstacles.extend([Cube((rows - 1, i), color=(217, 217, 217), obstacle=True) for i in range(rows)])  # Batas kanan
        obstacles.extend([Cube((i, rows - 1), color=(217, 217, 217), obstacle=True) for i in range(rows)])  # Batas bawah
        obstacles.extend([
            Cube((4, 6), color=(217, 217, 217), obstacle=True),
            Cube((5, 6), color=(217, 217, 217), obstacle=True),
            Cube((6, 6), color=(217, 217, 217), obstacle=True),
            Cube((7, 6), color=(217, 217, 217), obstacle=True),
            Cube((8, 6), color=(217, 217, 217), obstacle=True),
            Cube((9, 6), color=(217, 217, 217), obstacle=True),
            Cube((10, 6), color=(217, 217, 217), obstacle=True),
            Cube((10, 7), color=(217, 217, 217), obstacle=True),
            Cube((10, 8), color=(217, 217, 217), obstacle=True),
            Cube((10, 9), color=(217, 217, 217), obstacle=True),
            Cube((10, 10), color=(217, 217, 217), obstacle=True),
            Cube((11, 10), color=(217, 217, 217), obstacle=True),
            Cube((12, 10), color=(217, 217, 217), obstacle=True),
            Cube((13, 10), color=(217, 217, 217), obstacle=True),
            Cube((14, 10), color=(217, 217, 217), obstacle=True),
            Cube((5, 14), color=(217, 217, 217), obstacle=True),
            Cube((6, 14), color=(217, 217, 217), obstacle=True),
            Cube((7, 14), color=(217, 217, 217), obstacle=True),
            Cube((13, 14), color=(217, 217, 217), obstacle=True),
            Cube((11, 14), color=(217, 217, 217), obstacle=True),
            Cube((12, 14), color=(217, 217, 217), obstacle=True)
        ])  # Posisi obstacle pada batas-batas board
        
        def generate_apple(obstacles):
            available_positions = [(i, j) for i in range(rows) for j in range(rows) if (i, j) not in obstacles]
            apple_pos = random.choice(available_positions)
            return Cube(apple_pos, color=(255, 0, 0))

        def redrawWindow(surface, rows, width, obstacles, apple):
            surface.fill((0, 0, 0))
            drawGrid(surface, rows, width, obstacles)
            apple.draw(surface)
            pygame.display.update()
            
        apple = generate_apple(obstacles)
        apple.dirnx = 0
        apple.dirny = 0
        
        while True:  # gameloop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                apple.dirnx = 0
                apple.dirny = -1
            elif keys[pygame.K_a]:
                apple.dirnx = -1
                apple.dirny = 0
            elif keys[pygame.K_s]:
                apple.dirnx = 0
                apple.dirny = 1
            elif keys[pygame.K_d]:
                apple.dirnx = 1
                apple.dirny = 0
                    
            new_pos = (apple.pos[0] + apple.dirnx, apple.pos[1] + apple.dirny)

            if new_pos in [(obstacle.pos[0], obstacle.pos[1]) for obstacle in obstacles]:
                # Jika posisi baru terkena rintangan, tidak perlu mengubah posisi apel
                pass
            else:
                if new_pos[0] < 0:
                    apple.pos = (rows - 1, new_pos[1])
                elif new_pos[0] >= rows:
                    apple.pos = (0, new_pos[1])
                elif new_pos[1] < 0:
                    apple.pos = (new_pos[0], rows - 1)
                elif new_pos[1] >= rows:
                    apple.pos = (new_pos[0], 0)
                else:
                    apple.pos = new_pos
                    
            surface.fill((85, 67, 63))
            drawGrid(surface, rows, width, obstacles)
            apple.draw(surface)
            pygame.display.update()
            clock.tick(10)  # framerate maksimum = 10 fps

    main()

