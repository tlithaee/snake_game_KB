import math, random, pygame, sys, copy, time

def run_game():

    class cube(object):
        rows = 20
        w = 500
        def __init__(self,start,dirnx=1,dirxny=0,color=(255,0,0), obstacle=False, food=False):
            self.pos = start
            self.dirnx = 1
            self.dirny = 0
            self.color = color
            self.obstacle = obstacle
            self.food = food

        def move(self, dirnx, dirny):
            self.dirnx = dirnx
            self.dirny = dirny
            self.pos = ((self.pos[0] + self.dirnx)%20, (self.pos[1] + self.dirny)%20)

        def draw(self, surface, eyes=False):
            dis = self.w // self.rows
            i = self.pos[0]
            j = self.pos[1]
            food = self.food

            if self.obstacle:
                pygame.draw.rect(surface, (217, 217, 217), (i * dis + 1, j * dis + 1, dis + 2, dis - 2))

            else:
                if food:
                    apple_image = pygame.image.load("assets/apple.png")
                    apple_image = pygame.transform.scale(apple_image, (dis - 2, dis - 2))
                    surface.blit(apple_image, (i * dis + 1, j * dis + 1))
                else: 
                    pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis + 2, dis - 2))

            if eyes:
                centre = dis // 2
                radius = 3
                circleMiddle = (i * dis + centre - radius, j * dis + 8)
                circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
                pygame.draw.circle(surface, (255, 255, 255), circleMiddle, radius)
                pygame.draw.circle(surface, (255, 255, 255), circleMiddle2, radius)

    class snake(object):
        body = []
        turns = {}
        def __init__(self, color, pos):
            self.color = color
            self.head = cube(pos,color=(102,178,255))
            self.body.append(self.head)
            self.last_dir = ""
            self.curr_dir = "right"
            self.dirnx = 1
            self.dirny = 0
            tail = self.body[-1]
            self.body.append(cube((tail.pos[0]-1,tail.pos[1]),color=(255, 255, 255)))
            self.body.append(cube((tail.pos[0]-2,tail.pos[1]),color=(255, 255, 255)))
            self.body.append(cube((tail.pos[0]-3,tail.pos[1]),color=(255, 255, 255)))

        def move(self, control=""):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    break

            keys = pygame.key.get_pressed()
            if control != self.curr_dir:
                self.last_dir = self.curr_dir
                if control == "left": 
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    self.curr_dir = "left"

                elif control == "right":
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    self.curr_dir = "right" 

                elif control == "up":
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    self.curr_dir = "up"

                elif control == "down":
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    self.curr_dir = "down"

                else:
                    for key in keys:
                        if keys[pygame.K_LEFT] and self.curr_dir != "left":
                            self.dirnx = -1
                            self.dirny = 0
                            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                            self.curr_dir = "left"

                        elif keys[pygame.K_RIGHT] and self.curr_dir != "right":
                            self.dirnx = 1
                            self.dirny = 0
                            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                            self.curr_dir = "right"

                        elif keys[pygame.K_UP] and self.curr_dir != "up":
                            self.dirnx = 0
                            self.dirny = -1
                            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                            self.curr_dir = "up"

                        elif keys[pygame.K_DOWN] and self.curr_dir != "down":
                            self.dirnx = 0
                            self.dirny = 1
                            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                            self.curr_dir = "down"
            print(self.dirnx)
            print(self.dirny)
                        
            for i, c in enumerate(self.body):
                p = c.pos[:]
                if p in self.turns:
                    turn = self.turns[p]
                    c.move(turn[0],turn[1])
                    if i == len(self.body)-1:
                        self.turns.pop(p)
                else:
                    if c.dirnx == -1 and c.pos[0] <= 0: # out of left bound
                        c.pos = (19, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0] >= 19: # out of right bound
                        c.pos = (0,c.pos[1])
                    elif c.dirny == 1 and c.pos[1] >= 19: # out of bottom bound
                        c.pos = (c.pos[0], 0)
                    elif c.dirny == -1 and c.pos[1] <= 0: # out of top bound
                        c.pos = (c.pos[0],19)
                    else: c.move(c.dirnx,c.dirny)

        def reset(self, pos):
            self.head = cube(pos,color=(102,178,255))
            self.body = []
            self.body.append(self.head)
            self.turns = {}
            self.dirnx = 0
            self.dirny = 1
            tail = self.body[-1]
            self.body.append(cube((tail.pos[0]-1,tail.pos[1]),color=(255, 255, 255)))
            self.body.append(cube((tail.pos[0]-2,tail.pos[1]),color=(255, 255, 255)))
            self.body.append(cube((tail.pos[0]-3,tail.pos[1]),color=(255, 255, 255)))
            

        def draw(self, surface):
            for i, c in enumerate(self.body):
                if i == 0:
                    c.draw(surface, True)
                else:
                    c.draw(surface)


    def drawGrid(w, rows, surface, obstacles):

        for obstacle in obstacles:
            if obstacle.obstacle:
                obstacle.draw(surface)
            
        pygame.display.update()
    
    def drawScore(score):
        score_font = pygame.font.SysFont('Raleway', 20, bold=True)
        score_surface = score_font.render('Score : ' + str(score), True, pygame.Color(153, 255, 51))
        score_rect = score_surface.get_rect()
        score_rect.topleft = (width-120, 10)
        surface.blit(score_surface, score_rect)

    def drawPressKeyMsg():
        press_font = pygame.font.SysFont('Raleway', 25)
        pressKeySurf = press_font.render('Press a key to play.', True, (255, 255, 255))
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.midtop = (250, 350)
        surface.blit(pressKeySurf, pressKeyRect)

    def redrawWindow(score, obstacles, lose=False):
        surface.fill((85, 67, 63))
        s.draw(surface)
        apple.draw(surface)
        if not lose:
            drawGrid(width, rows, surface, obstacles)
        drawScore(score)
        pygame.display.update()
    
    def showGameOverScreen():
        gameOverFont = pygame.font.SysFont("courier new", 150)
        gameSurf = gameOverFont.render('Game', True, pygame.Color(255, 255, 255))
        overSurf = gameOverFont.render('Over', True, pygame.Color(255, 255, 255))
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        gameRect.midtop = (width / 2, 10)
        overRect.midtop = (width / 2, gameRect.height + 10 + 25)

        surface.blit(gameSurf, gameRect)
        surface.blit(overSurf, overRect)
        drawPressKeyMsg()
        pygame.display.update()
        pygame.time.wait(500)
        checkForKeyPress()

        while True:
            if checkForKeyPress():
                pygame.event.get() 
                return
    
    #cek tombol yang ditekan apakah escape atau quit
    def checkForKeyPress():
        if len(pygame.event.get(pygame.QUIT)) > 0:
            pygame.quit()
            sys.exit()
        keyUpEvents = pygame.event.get(pygame.KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        return keyUpEvents[0].key
    
    def best_first_search(new_pos):
        global s, snack, visited
        #menyimpan posisi x dan y kepala ular
        curr_posx = s.body[0].pos[0]
        curr_posy = s.body[0].pos[1]

        nodes = [] # 0: left, 1: right, 2: up, 3: down
        #menghitung bagian kiri
        p = ((curr_posx-1)%20,curr_posy)
        nodes.append(('left', manhattan_dis((curr_posx-1,curr_posy),new_pos,size=rows), p))
        #menghitung bagian kanan
        p = ((curr_posx+1)%20,curr_posy)
        nodes.append(('right', manhattan_dis((curr_posx+1,curr_posy),new_pos,size=rows), p))
        #menghitung bagian atas
        p = (curr_posx,(curr_posy-1)%20)
        nodes.append(('up', manhattan_dis((curr_posx,curr_posy-1),new_pos,size=rows), p))
        #menghitung bagian bawah
        p = (curr_posx,(curr_posy+1)%20)
        nodes.append(('down', manhattan_dis((curr_posx,curr_posy+1),new_pos,size=rows), p))

        #apakah posisi node ada di tubuh ular? jika iya maka akan tabrakan dg tubuh ular lalu s.move()
        if set(nodes[:][2])<= set(list(map(lambda z:z.pos,s.body))):
            s.move()
            return
        i = 0 
        print()
        best = []
        dist = []
        for p in nodes:
            #menghitung prioritas arah pergerakan
            prio = 0
            if (len(s.body)>2):
                #gerak ke kanan atas dan kanan bawah
                temp = [((curr_posx+1)%20,(curr_posy+1)%20),((curr_posx+1)%20,(curr_posy-1)%20)]
                #cek apakah setiap posisi dalam temp telah ada dalam list posisi tubuh snake menggunakan set
                if set(temp) <= set(list(map(lambda z:z.pos,s.body))):
                    if p[0]=="right":
                        prio += 1
                    elif (p[0]=="up" and s.curr_dir=="right" and s.last_dir=="up") or (p[0]=="down" and s.curr_dir=="right" and s.last_dir=="down"):
                        prio += 1
                #gerak ke kiri atas dan kiri bawah
                temp = [((curr_posx-1)%20,(curr_posy+1)%20),((curr_posx-1)%20,(curr_posy-1)%20)]
                if set(temp) <= set(list(map(lambda z:z.pos,s.body))):
                    if p[0]=="left":
                        prio += 1
                    elif (p[0]=="up" and s.curr_dir=="left" and s.last_dir=="up") or (p[0]=="down" and s.curr_dir=="left" and s.last_dir=="down"):
                        prio += 1
                #gerak ke kanan atas dan kiri atas
                temp = [((curr_posx+1)%20,(curr_posy+1)%20),((curr_posx-1)%20,(curr_posy+1)%20)]
                if set(temp) <= set(list(map(lambda z:z.pos,s.body))):
                    if p[0]=="down":
                        prio += 1
                    elif (p[0]=="left" and s.curr_dir=="down" and s.last_dir=="left") or (p[0]=="right" and s.curr_dir=="down" and s.last_dir=="right"):
                        prio += 1
                #gerak ke kanan bawah dan kiri bawah
                temp = [((curr_posx+1)%20,(curr_posy-1)%20),((curr_posx-1)%20,(curr_posy-1)%20)]
                if set(temp) <= set(list(map(lambda z:z.pos,s.body))):
                    if p[0]=="up":
                        prio += 1
                    elif (p[0]=="left" and s.curr_dir=="up" and s.last_dir=="left") or (p[0]=="right" and s.curr_dir=="up" and s.last_dir=="right"):
                        prio += 1

                #menyimpan jumlah langkah yang dibutuhkan agar snake mencapai batas atas atau batas bawah environment permainan
                cy = 0
                #menghitung jumlah langkah yang dibutuhkan untuk mencapai batas atas
                if curr_posy > 16 and curr_posy < 19:
                    cy = 19 - curr_posy
                elif curr_posy < 17:
                    cy = 3

                bottom = [q for q in list(map(lambda z:z.pos,s.body)) if q[0]==curr_posx and q[1]-curr_posy < cy and curr_posy<q[1]]
                for i in range(3-cy):
                    if (curr_posx,i) in list(map(lambda z:z.pos,s.body)): bottom.append((curr_posx,i))
                print("bottom " + str(bottom))    
                cy = 0
                if curr_posy > 0 and curr_posy < 3:
                    cy = curr_posy
                elif curr_posy > 2:
                    cy = 3
                top = [q for q in list(map(lambda z:z.pos,s.body)) if q[0]==curr_posx and curr_posy-q[1] < cy and curr_posy>q[1]]
                for i in range(19,16+cy,-1):
                    if (curr_posx,i) in list(map(lambda z:z.pos,s.body)): top.append((curr_posx,i))
                print("top " + str(top))
                cx = 0
                if curr_posx > 0 and curr_posx < 3:
                    cx = curr_posx
                elif curr_posx > 2:
                    cx = 3
                left = [q for q in list(map(lambda z:z.pos,s.body)) if q[1]==curr_posy and curr_posx-q[0] < cx and curr_posx>q[0]]
                for i in range(19,16+cx,-1):
                    if (i,curr_posy) in list(map(lambda z:z.pos,s.body)): left.append((i,curr_posy))
                print("left " + str(left))
                cx = 0
                if curr_posx > 16 and curr_posx < 19:
                    cx = 19 - curr_posx
                elif curr_posx < 17:
                    cx = 3
                right = [q for q in list(map(lambda z:z.pos,s.body)) if q[1]==curr_posy and q[0]-curr_posx < cx and curr_posx<q[0]]
                for i in range(3-cx):
                    if (i,curr_posy) in list(map(lambda z:z.pos,s.body)): right.append((i,curr_posy))
                print("right " + str(right))
                temp = []
                if p[0] == "up":
                    if len(top) and s.curr_dir != "down":
                        prio += len(top)            
                        for q in top:
                            temp.append(manhattan_dis((curr_posx,curr_posy),q,size=rows))
                        dist.append(("up",min(temp)))
                elif p[0] == "down":
                    if len(bottom) and s.curr_dir != "up":
                        prio += len(bottom)
                        for q in bottom:
                            temp.append(manhattan_dis((curr_posx,curr_posy),q,size=rows))
                        dist.append(("down",min(temp)))
                elif p[0] == "left":
                    if len(left) and s.curr_dir != "right":
                        prio += len(left)
                        for q in left:
                            temp.append(manhattan_dis((curr_posx,curr_posy),q,size=rows))
                        dist.append(("left",min(temp)))
                elif p[0] == "right":
                    if len(right) and s.curr_dir != "left":
                        prio += len(right)
                        for q in right:
                            temp.append(manhattan_dis((curr_posx,curr_posy),q,size=rows))
                        dist.append(("right",min(temp)))
                if p[2] in list(map(lambda z:z.pos,s.body)):
                    prio += 1
            best.append((p[0],p[1],p[2],prio))
        if len(dist):
            print(dist)
            mindist = min(dist, key=lambda t: t[1])
            print(mindist)
            temp = [x[0] for x in dist if x[1]==mindist[1]]
            print(temp)
            for j in temp:
                print(j)
                near = best.pop([y[0] for y in best].index(j))
                print(near)
                best.append((near[0],near[1],near[2],near[3]+1))
        best = sorted(best,key=lambda t: (t[3],t[1]))
        print(best)
        for p in best:
            print(i)
            if p[0] == "left" and s.curr_dir != "right" and p not in visited:
                print("A")
                s.move(control="left")
                visited.add(p)
                return
            elif p[0] == "right" and s.curr_dir != "left" and p not in visited:
                print("B")
                s.move(control="right")
                visited.add(p)
                return
            elif p[0] == "up" and s.curr_dir != "down" and p not in visited:
                print("C")
                s.move(control="up")
                visited.add(p)
                return
            elif p[0] == "down" and s.curr_dir != "up" and p not in visited:
                print("D")
                s.move(control="down")
                visited.add(p)
                return
            i+=1
        s.move()

    def manhattan_dis(p,q,size=0):
        dx = min( abs( q[0] - p[0] ), size - abs( q[0] - p[0] ) )
        dy = min( abs( q[1] - p[1] ), size - abs( q[1] - p[1] ) )
        return dx + dy

    def generate_apple(obstacles):
        available_positions = [(i, j) for i in range(rows) for j in range(rows) if (i, j) not in obstacles]
        apple_pos = random.choice(available_positions)
        return cube(apple_pos, color=(255, 0, 0), food=True)
    
    def checkForKeyPress():
        if len(pygame.event.get(pygame.QUIT)) > 0:
            pygame.quit()
            sys.exit()
        keyUpEvents = pygame.event.get(pygame.KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        return keyUpEvents[0].key
    
    def showGameOverScreen():
        gameOverFont = pygame.font.SysFont("courier new", 150)
        gameSurf = gameOverFont.render('Game', True, pygame.Color(255, 255, 255))
        overSurf = gameOverFont.render('Over', True, pygame.Color(255, 255, 255))
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        gameRect.midtop = (width / 2, 10)
        overRect.midtop = (width / 2, gameRect.height + 10 + 25)

        surface.blit(gameSurf, gameRect)
        surface.blit(overSurf, overRect)
        drawPressKeyMsg()
        pygame.display.update()
        pygame.time.wait(500)
        checkForKeyPress()

        while True:
            if checkForKeyPress():
                pygame.event.get() 
                return

    def main():
        global width, rows, s, snack, surface, visited, apple, new_pos
        pygame.init()
        width = 500
        rows = 20
        surface = pygame.display.set_mode((width,width))
        pygame.display.set_caption('Snake Game Bot')
        startx = random.randint(0, rows-1)
        starty = random.randint(0, rows-1)
        s = snake((255,255,51), (startx,starty))
        # food_pos = randomSnack(rows, s)
        # snack = cube(food_pos, color=(255, 51, 51))
        flag = True
        clock = pygame.time.Clock()
        visited = set({})

        obstacles = [cube((i, 0), color=(217, 217, 217), obstacle=True) for i in range(rows)] 
        obstacles.extend([cube((i, rows - 1), color=(217, 217, 217), obstacle=True) for i in range(rows)])  # Batas bawah
        obstacles.extend([
            cube((4, 6), color=(217, 217, 217), obstacle=True),
            cube((5, 6), color=(217, 217, 217), obstacle=True),
            cube((6, 6), color=(217, 217, 217), obstacle=True),
            cube((7, 6), color=(217, 217, 217), obstacle=True),
            cube((8, 6), color=(217, 217, 217), obstacle=True),
            cube((9, 6), color=(217, 217, 217), obstacle=True),
            cube((10, 6), color=(217, 217, 217), obstacle=True),
            cube((10, 7), color=(217, 217, 217), obstacle=True),
            cube((10, 8), color=(217, 217, 217), obstacle=True),
            cube((10, 9), color=(217, 217, 217), obstacle=True),
            cube((10, 10), color=(217, 217, 217), obstacle=True),
            cube((11, 10), color=(217, 217, 217), obstacle=True),
            cube((12, 10), color=(217, 217, 217), obstacle=True),
            cube((13, 10), color=(217, 217, 217), obstacle=True),
            cube((14, 10), color=(217, 217, 217), obstacle=True),
            cube((5, 14), color=(217, 217, 217), obstacle=True),
            cube((6, 14), color=(217, 217, 217), obstacle=True),
            cube((7, 14), color=(217, 217, 217), obstacle=True),
            cube((13, 14), color=(217, 217, 217), obstacle=True),
            cube((11, 14), color=(217, 217, 217), obstacle=True),
            cube((12, 14), color=(217, 217, 217), obstacle=True)
        ])  # Posisi obstacle pada batas-batas board

        obs_pos = [ (1, 0),(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), 
                   (16, 0), (17, 0), (18, 0), (19, 0), (0, 19), (1, 19), (2, 19),(3, 19), (4, 19), (5, 19), (6, 19), (7, 19), (8, 19), (9, 19), (10, 19),  (11, 19), (12, 19), (13, 19), (14, 19), (15, 19), 
                   (16, 19), (17, 19), (18, 19), (19, 19), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 6), (10, 7), (10, 8), (10, 9),    
                   (10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (5, 14), (6, 14), (7, 14), (13, 14), (11, 14), (12, 14)
                ]

        apple = generate_apple(obstacles)
        apple.dirnx = 0
        apple.dirny = 0
        score = 0;
        while flag:
            pygame.time.delay(50)
            clock.tick(10)

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

            best_first_search(new_pos)

            x, y = s.body[0].pos
            xx, yy = s.body[1].pos

            if (x + 1, y) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))

            elif (x - 1, y) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))

            elif (x, y + 1) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))
            
            elif (x, y - 1) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))

            elif (xx + 1, yy) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))

            elif (xx - 1, yy) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))

            elif (xx, yy + 1) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))

            elif (xx, yy - 1) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))

            if (x + 1, y) in obs_pos:
                score += 1;
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                redrawWindow(score, obstacles)

                for posisi in obs_pos:
                    x, y = posisi

                    if startx == x and starty == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)
                    if startx-1 == x and starty-1 == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)
                    if startx-2 == x and starty-2 == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)
                    if startx-3 == x and starty-3 == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)

                s.reset((startx,starty))
            
            if (x - 1, y) in obs_pos:
                score += 1;
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                redrawWindow(score, obstacles)

                for posisi in obs_pos:
                    x, y = posisi

                    if startx == x and starty == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)
                    if startx-1 == x and starty-1 == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)
                    if startx-2 == x and starty-2 == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)
                    if startx-3 == x and starty-3 == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)

                s.reset((startx,starty))
                
            if (x, y + 1) in obs_pos:
                score += 1;
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                redrawWindow(score, obstacles)

                for posisi in obs_pos:
                    x, y = posisi

                    if startx == x and starty == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)
                    if startx-1 == x and starty-1 == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)
                    if startx-2 == x and starty-2 == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)
                    if startx-3 == x and starty-3 == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)

                s.reset((startx,starty))
            
            if (x, y - 1) in obs_pos:
                score += 1;
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                redrawWindow(score, obstacles)

                for posisi in obs_pos:
                    x, y = posisi

                    if startx == x and starty == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)
                    if startx-1 == x and starty-1 == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)
                    if startx-2 == x and starty-2 == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)
                    if startx-3 == x and starty-3 == y:
                        startx = random.randint(0, rows-1)
                        starty = random.randint(0, rows-1)

                s.reset((startx,starty))
                
            redrawWindow(score, obstacles)

    main()
