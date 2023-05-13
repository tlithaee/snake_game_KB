import pygame
import sys
import random
from blessed import Terminal

def run_game():

    # -------CONFIG--------
    APPLE = '🍎'

    class Cube(object):
        rows = 20
        width = 500

        def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0), obstacle=False):
            self.pos = start
            self.dirnx = dirnx
            self.dirny = dirny
            self.color = color
            self.obstacle = obstacle

        def draw(self, surface, eyes=False):
            dis = self.width // self.rows
            i = self.pos[0]
            j = self.pos[1]

            if self.obstacle:
                pygame.draw.rect(surface, (217, 217, 217), (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
            else:
                pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

            if not self.obstacle:
                apple_font = pygame.font.Font(None, dis)  # Menggunakan font default pygame
                apple_text = apple_font.render(APPLE, True, (255, 0, 0))  # Menggambar teks apel dengan warna merah
                surface.blit(apple_text, (i * dis + dis // 2 - apple_text.get_width() // 2, j * dis + dis // 2 - apple_text.get_height() // 2))  # Menampilkan teks apel di posisi yang tepat
                
                if eyes:
                    centre = dis // 2
                    radius = 3
                    circleMiddle = (i * dis + centre - radius, j * dis + 8)
                    circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
                    pygame.draw.circle(surface, (255, 255, 255), circleMiddle, radius)
                    pygame.draw.circle(surface, (255, 255, 255), circleMiddle2, radius)

    def drawGrid(surface, rows, width, obstacles):
        sizeBtwn = width // rows
        for l in range(rows):
            x = l * sizeBtwn
            y = l * sizeBtwn

        for obstacle in obstacles:
            obstacle.draw(surface)

    def main():
        pygame.init()
        width = 500
        rows = 20
        surface = pygame.display.set_mode((width, width))
        clock = pygame.time.Clock()  # objek clock untuk mengontrol framerate

        obstacles = [
            Cube((4, 5), color=(0, 0, 255), obstacle=True),
            Cube((4, 6), color=(0, 0, 255), obstacle=True),
            Cube((4, 7), color=(0, 0, 255), obstacle=True),
            Cube((10, 15), color=(0, 0, 255), obstacle=True),
            Cube((11, 15), color=(0, 0, 255), obstacle=True),
            Cube((12, 15), color=(0, 0, 255), obstacle=True),
            Cube((13, 15), color=(0, 0, 255), obstacle=True),
            Cube((14, 15), color=(0, 0, 255), obstacle=True),
            Cube((15, 15), color=(0, 0, 255), obstacle=True),
            Cube((15, 14), color=(0, 0, 255), obstacle=True),
            Cube((15, 13), color=(0, 0, 255), obstacle=True),
            Cube((15, 12), color=(0, 0, 255), obstacle=True),
            Cube((15, 11), color=(0, 0, 255), obstacle=True),
            Cube((15, 10), color=(0, 0, 255), obstacle=True)
        ]

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
