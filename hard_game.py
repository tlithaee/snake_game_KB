import math, random, pygame, sys, copy, time

def run_game():

    #menggambar objek
    class cube(object):
        #setup 20 rows dengan width 500
        rows = 20
        w = 500
        def __init__(self,start,dirnx=1,dirxny=0,color=(255,0,0), obstacle=False, food=False):
            self.pos = start
            self.dirnx = 1
            self.dirny = 0
            self.color = color
            self.obstacle = obstacle
            self.food = food

        #fungsi move untuk si apel
        def move(self, dirnx, dirny):
            self.dirnx = dirnx
            self.dirny = dirny
            #di mod 20 karena batasannya kan 20 rows
            self.pos = ((self.pos[0] + self.dirnx) % 20, (self.pos[1] + self.dirny) % 20)

        def draw(self, surface, eyes=False):
            dis = self.w // self.rows  # Menghitung jarak antar sel pada grid
            i = self.pos[0]  # Koordinat x posisi objek
            j = self.pos[1]  # Koordinat y posisi objek
            food = self.food  # Menentukan apakah objek adalah makanan atau bukan

            if self.obstacle:  # Jika objek adalah rintangan
                pygame.draw.rect(surface, (217, 217, 217), (i * dis + 1, j * dis + 1, dis + 2, dis - 2))
                # Menggambar persegi rintangan pada posisi yang benar

            else:
                if food:  # Jika objek adalah makanan
                    apple_image = pygame.image.load("assets/apple.png")
                    apple_image = pygame.transform.scale(apple_image, (dis - 2, dis - 2))
                    surface.blit(apple_image, (i * dis + 1, j * dis + 1))
                    # Menggambar gambar apel pada posisi yang benar

                else:
                    pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis + 2, dis - 2))
                    # Menggambar persegi biasa dengan warna yang ditentukan pada posisi yang benar

            if eyes:  # Jika mata ular diaktifkan
                centre = dis // 2
                radius = 3
                circleMiddle = (i * dis + centre - radius, j * dis + 8)
                circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
                pygame.draw.circle(surface, (255, 255, 255), circleMiddle, radius)
                pygame.draw.circle(surface, (255, 255, 255), circleMiddle2, radius)
                # Menggambar mata pada posisi yang benar


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
            #menambahkan 3 badan
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
                #ular move ke kiri
                if control == "left": 
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    self.curr_dir = "left"
                
                #ular move ke kanan
                elif control == "right":
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    self.curr_dir = "right" 

                #ular move ke atas
                elif control == "up":
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    self.curr_dir = "up"

                #ular move ke bawah
                elif control == "down":
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    self.curr_dir = "down"

            print(self.dirnx)
            print(self.dirny)
                        
            for i, c in enumerate(self.body):
                p = c.pos[:]

                # Memeriksa apakah posisi saat ini ada dalam daftar putaran (turns)
                if p in self.turns:
                    turn = self.turns[p]
                    c.move(turn[0], turn[1])

                    # Jika elemen saat ini adalah elemen terakhir dalam tubuh ular, hapus putaran yang terkait
                    if i == len(self.body) - 1:
                        self.turns.pop(p)
                else:
                    # Memeriksa apakah ular berada di luar batas area bermain
                    if c.dirnx == -1 and c.pos[0] <= 0:  # di luar batas kiri
                        c.pos = (19, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0] >= 19:  # di luar batas kanan
                        c.pos = (0, c.pos[1])
                    elif c.dirny == 1 and c.pos[1] >= 19:  # di luar batas bawah
                        c.pos = (c.pos[0], 0)
                    elif c.dirny == -1 and c.pos[1] <= 0:  # di luar batas atas
                        c.pos = (c.pos[0], 19)
                    else:
                        # Jika tidak ada putaran yang diperlukan, lanjutkan pergerakan ular sesuai arah saat ini
                        c.move(c.dirnx, c.dirny)

        #reset snake
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
            # Melakukan iterasi pada setiap bagian tubuh ular
            for i, c in enumerate(self.body):
                # Jika ini adalah kepala ular, gambar dengan mata (eyes) aktif
                if i == 0:
                    c.draw(surface, True)
                # Jika bukan kepala, gambar tanpa mata (eyes) aktif
                else:
                    c.draw(surface)


    def drawGrid(w, rows, surface, obstacles):
        # Menggambar grid pada permukaan (surface) dengan mengambil lebar (w) dan jumlah baris (rows) sebagai parameter
        # obstacles adalah daftar objek penghalang yang akan digambar

        # Melakukan iterasi pada setiap objek penghalang
        for obstacle in obstacles:
            # Jika objek penghalang tersebut ada, gambar objek penghalang pada permukaan (surface)
            if obstacle.obstacle:
                obstacle.draw(surface)

        # Memperbarui tampilan permukaan (surface) agar perubahan terlihat
        pygame.display.update()

    
    def drawScore(score):
        # Menggambar skor pada permukaan (surface) berdasarkan skor yang diberikan sebagai parameter

        # Membuat font untuk skor dengan menggunakan font "Raleway" dengan ukuran 20 dan cetak tebal (bold)
        score_font = pygame.font.SysFont('Raleway', 20, bold=True)

        # Membuat permukaan (surface) untuk skor dengan teks yang sesuai
        score_surface = score_font.render('Score : ' + str(score), True, pygame.Color(153, 255, 51))

        # Mendapatkan area persegi panjang (rect) dari permukaan skor
        score_rect = score_surface.get_rect()

        # Mengatur posisi kiri atas (topleft) dari area persegi panjang skor
        score_rect.topleft = (width-120, 10)

        # Menempatkan permukaan skor pada permukaan utama (surface)
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
    
    #parameter new_pos karena posisi tujuan yang ingin dicapai ular
    def best_first_search(new_pos):
        global s, visited
        #menyimpan posisi x dan y kepala ular saat ini
        curr_posx = s.body[0].pos[0]
        curr_posy = s.body[0].pos[1]

        nodes = [] # 0: left, 1: right, 2: up, 3: down
        #posisi baru kepala ular ke kiri
        p = ((curr_posx-1)%20,curr_posy)
        nodes.append(('left', manhattan_dis((curr_posx-1,curr_posy),new_pos,size=rows), p))
        #posisi baru kepala ular ke kanan
        p = ((curr_posx+1)%20,curr_posy)
        nodes.append(('right', manhattan_dis((curr_posx+1,curr_posy),new_pos,size=rows), p))
        #posisi baru kepala ular ke atas
        p = (curr_posx,(curr_posy-1)%20)
        nodes.append(('up', manhattan_dis((curr_posx,curr_posy-1),new_pos,size=rows), p))
        #posisi baru kepala ular ke bawah
        p = (curr_posx,(curr_posy+1)%20)
        nodes.append(('down', manhattan_dis((curr_posx,curr_posy+1),new_pos,size=rows), p))

        #misal nodes = [('left', 10, (1, 2)), ('right', 8, (3, 4)), ('up', 12, (5, 6))]
        #maka nodes[:][2] = [(1, 2), (3, 4), (5, 6)]

        #apakah posisi node ada di tubuh ular? jika iya maka akan tabrakan dg tubuh ular lalu s.move()
        if set(nodes[:][2])<= set(list(map(lambda z:z.pos,s.body))):
            s.move()
            return
        i = 0 
        print()

        #menyimpan elemen-elemen yang diurutkan berdasarkan prioritas pergerakan
        #format: (arah, manhattan_dis, new_pos, prioritas)
        best = []

        dist = []

        #looping elemen dalam nodes
        #misal nodes = [('left', 10, (1, 2)), ('right', 8, (3, 4)), ('up', 12, (5, 6))]
        #dilakukan forward checking.semakin  besar prio maka semakin buruk langkah yang dapat diselesaikan
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
                #menghitung jumlah langkah yang dibutuhkan untuk mencapai batas bawah
                if curr_posy > 16 and curr_posy < 19:
                    cy = 19 - curr_posy
                elif curr_posy < 17:
                    cy = 3
                
                #menghitung posisi yang berada di bagian bawah ular
                bottom = [q for q in list(map(lambda z:z.pos,s.body)) if q[0]==curr_posx and q[1]-curr_posy < cy and curr_posy<q[1]]

                #menambah posisi yang belum masuk ke bottom
                for i in range(3-cy):
                    if (curr_posx, i) in list(map(lambda z:z.pos,s.body)): bottom.append((curr_posx,i))
                print("bottom " + str(bottom))  

                #menghitung jumlah langkah yang dibutuhkan untuk mencapai batas atas
                cy = 0
                if curr_posy > 0 and curr_posy < 3:
                    cy = curr_posy
                elif curr_posy > 2:
                    cy = 3 #artinya berapapun langkahnya, ditetapkan 3 agar ga nabrak bagian atas 

                #menghitung posisi yang berada di bagian atas ular
                top = [q for q in list(map(lambda z:z.pos,s.body)) if q[0]==curr_posx and curr_posy-q[1] < cy and curr_posy>q[1]]

                #menambah posisi yang belum masuk ke top
                for i in range(19, 16 + cy, -1):
                    if (curr_posx,i) in list(map(lambda z:z.pos,s.body)): top.append((curr_posx,i))
                print("top " + str(top))

                #menghitung jumlah langkah yang dibutuhkan untuk mencapai batas kiri
                cx = 0
                if curr_posx > 0 and curr_posx < 3:
                    cx = curr_posx
                elif curr_posx > 2:
                    cx = 3

                #memasukkan posisi yang berada di bagian kiri ular
                left = [q for q in list(map(lambda z:z.pos,s.body)) if q[1]==curr_posy and curr_posx-q[0] < cx and curr_posx>q[0]]
                for i in range(19, 16 + cx, -1):
                    if (i,curr_posy) in list(map(lambda z:z.pos,s.body)): left.append((i,curr_posy))
                print("left " + str(left))

                #menghitung jumlah langkah yang diperlukan untuk mencapai batas kanan ular
                cx = 0
                if curr_posx > 16 and curr_posx < 19:
                    cx = 19 - curr_posx
                elif curr_posx < 17:
                    cx = 3
                
                #memasukkan posisi yang berada di bagian kanan ular
                right = [q for q in list(map(lambda z:z.pos,s.body)) if q[1]==curr_posy and q[0]-curr_posx < cx and curr_posx<q[0]]
                for i in range(3-cx):
                    if (i,curr_posy) in list(map(lambda z:z.pos,s.body)): right.append((i,curr_posy))
                print("right " + str(right))

                #menyimpan jarak manhattan
                temp = []


                if p[0] == "up":
                    if len(top) and s.curr_dir != "down":
                        #menambah value prionya untuk forward checking
                        prio += len(top)

                        #menghitung manhattan 
                        for q in top:
                            temp.append(manhattan_dis((curr_posx,curr_posy),q,size=rows))
                        
                        #memasukkan ke distance lalu nilai minimumnya
                        dist.append(("up", min(temp)))
                
                elif p[0] == "down":
                    if len(bottom) and s.curr_dir != "up":
                        #menambah value prio
                        prio += len(bottom)

                        #menghitung manhattan
                        for q in bottom:
                            temp.append(manhattan_dis((curr_posx,curr_posy),q,size=rows))
                        
                        #memasukkan ke distance dan nilai minimum dari tempnya
                        dist.append(("down",min(temp)))
            
                elif p[0] == "left":
                    if len(left) and s.curr_dir != "right":
                        prio += len(left)
                        for q in left:
                            temp.append(manhattan_dis((curr_posx,curr_posy),q,size=rows))
                        
                        #memasukkan ke distance dan nilai minimum dari tempnya
                        dist.append(("left",min(temp)))

                elif p[0] == "right":
                    if len(right) and s.curr_dir != "left":
                        prio += len(right)
                        for q in right:
                            temp.append(manhattan_dis((curr_posx,curr_posy),q,size=rows))

                        #memasukkan ke distance dan nilai minimum dari tempnya
                        dist.append(("right",min(temp)))
                
                #cek apakah akan nabrak ke tubuh ular
                if p[2] in list(map(lambda z:z.pos,s.body)):
                    prio += 1
            
            #memasukkan isi dari nodes dan prionya
            best.append((p[0],p[1],p[2],prio))
        

        if len(dist):
            print(dist)

            #mencari elemen terkecil di dist berdasarkan elemen ke dua dari tiap tupel
            mindist = min(dist, key=lambda t: t[1])
            print(mindist)

            #jika nilai mindist[1] sama dengan x[1] dari dist maka masukkan nilai x[0]
            #nilai dari x[0] adalah kalimat "up", "down", "left", "right"
            temp = [x[0] for x in dist if x[1]==mindist[1]]
            print(temp)


            for j in temp:
                print(j)
                for index, y in enumerate(best):
                    if y[0] == j:
                        near = best.pop(index)
                        break
                print(near)
                #dimasukkan lagi ke best dengan penambahan 1 di prior
                best.append((near[0], near[1], near[2], near[3] + 1))

        #mengurutkan elemen berdasarkan nilai pada indeks ke 3 dulu
        best = sorted(best, key=lambda t: (t[3],t[1]))

        print(best)

        #perubahan gerakan yang menyesuaikan gbfs
        for p in best:
            print(i)

            #akan ke kiri jika sekarang ular tidak sedang gerak ke kanan
            if p[0] == "left" and s.curr_dir != "right" and p not in visited:
                print("A")
                s.move(control="left")
                visited.add(p)
                return
            
            #akan ke kanan jika sekarang ular tidak sedang gerak ke kiri
            elif p[0] == "right" and s.curr_dir != "left" and p not in visited:
                print("B")
                s.move(control="right")
                visited.add(p)
                return
            
            #akan ke atas jika sekarang ular tidak sedang gerak ke bawah
            elif p[0] == "up" and s.curr_dir != "down" and p not in visited:
                print("C")
                s.move(control="up")
                visited.add(p)
                return
            
            #akan ke bawah jika sekarang ular tidak sedang gerak ke atas
            elif p[0] == "down" and s.curr_dir != "up" and p not in visited:
                print("D")
                s.move(control="down")
                visited.add(p)
                return
            i += 1
        
        #ular gerak
        s.move()

    def manhattan_dis(p, q, size=0):
        #mengambil nilai minimum untuk manhattannya
        dx = min( abs( q[0] - p[0] ), size - abs( q[0] - p[0] ) )
        dy = min( abs( q[1] - p[1] ), size - abs( q[1] - p[1] ) )
        return dx + dy

    def generate_apple(obstacles):
        # Membangkitkan posisi acak untuk apel yang tidak bertabrakan dengan rintangan

        # Membuat daftar posisi yang tersedia untuk penempatan apel
        available_positions = [(i, j) for i in range(rows) for j in range(rows) if (i, j) not in obstacles]

        # Memilih secara acak posisi untuk apel dari posisi-posisi yang tersedia
        apple_pos = random.choice(available_positions)

        # Membuat objek cube yang merepresentasikan apel dengan posisi, warna, dan atribut food yang sesuai
        return cube(apple_pos, color=(255, 0, 0), food=True)

    def checkForKeyPress():
        #check keypress  apakah menyentuh jendela permainan
        if len(pygame.event.get(pygame.QUIT)) > 0:
            pygame.quit()
            sys.exit()
        keyUpEvents = pygame.event.get(pygame.KEYUP)
        if len(keyUpEvents) == 0:
            return None
        
        #jika pencet escape, maka game berhenti
        if keyUpEvents[0].key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        return keyUpEvents[0].key
    
    def showGameOverScreen():
        #menggunakan font courier new dengan size font 150
        gameOverFont = pygame.font.SysFont("courier new", 150)
        gameSurf = gameOverFont.render('Game', True, pygame.Color(255, 255, 255))
        overSurf = gameOverFont.render('Over', True, pygame.Color(255, 255, 255))
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()

        #diatur di tengah bagian atas layar
        gameRect.midtop = (width / 2, 10)
        #diatur di bawah teks game dengan jarak 25 pixel
        overRect.midtop = (width / 2, gameRect.height + 10 + 25)


        surface.blit(gameSurf, gameRect)
        surface.blit(overSurf, overRect)

        #menggambar pesan "press a key to play"
        drawPressKeyMsg()
        pygame.display.update()
        pygame.time.wait(500)
        checkForKeyPress()

        while True:
            if checkForKeyPress():
                pygame.event.get() 
                return

    def main():
        global width, rows, s, surface, visited, apple, new_pos
        pygame.init()
        width = 500
        rows = 20
        surface = pygame.display.set_mode((width,width))
        pygame.display.set_caption('Snake Game Bot')

        #random posisi
        startx = random.randint(0, rows-1)
        starty = random.randint(0, rows-1)
        s = snake((255,255,51), (startx,starty))
        flag = True
        clock = pygame.time.Clock()
        #menyimpan langkah yang telah diambil ular
        visited = set({})

        #menetapkan posisi obstacle
        obstacles = [
            cube((4, 5), color=(217, 217, 217), obstacle=True),
            cube((4, 6), color=(217, 217, 217), obstacle=True),
            cube((4, 7), color=(217, 217, 217), obstacle=True),
            cube((15, 14), color=(217, 217, 217), obstacle=True),
            cube((15, 13), color=(217, 217, 217), obstacle=True),
            cube((10, 12), color=(217, 217, 217), obstacle=True),
            cube((10, 11), color=(217, 217, 217), obstacle=True),
            cube((10, 10), color=(217, 217, 217), obstacle=True)
        ]

        obs_pos = [(4, 5), (4, 6), (4, 7), (15, 14), (15, 13), (10, 12), (10, 11), (10, 10)]
        
        #generate apelnya
        apple = generate_apple(obstacles)
        apple.dirnx = 0
        apple.dirny = 0
        score = 0;
        while flag:
            pygame.time.delay(50)
            clock.tick(8)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #handle keyboard wasd
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

            #perubahan posisi dari pergerakan apel
            new_pos = (apple.pos[0] + apple.dirnx, apple.pos[1] + apple.dirny)

            if new_pos in [(obstacle.pos[0], obstacle.pos[1]) for obstacle in obstacles]:
                # Jika posisi baru terkena rintangan, tidak perlu mengubah posisi apel
                pass
            else:
                #jika melewati batas kiri maka akan melintasi batas kanan posisi apelnya
                if new_pos[0] < 0:
                    apple.pos = (rows - 1, new_pos[1])
                #jika melewati batas kanan maka akan melintasi batas kiri posisi apelnya
                elif new_pos[0] >= rows:
                    apple.pos = (0, new_pos[1])
                
                #jika melewati batas atas maka akan melintasi batas bawah posisi apelnya
                elif new_pos[1] < 0:
                    apple.pos = (new_pos[0], rows - 1)
                
                #jika melewati batas bawah maka akan melintasi batas atas posisi apelnya
                elif new_pos[1] >= rows:
                    apple.pos = (new_pos[0], 0)
                
                #posisi apel akan sama dengan pergerakan
                else:
                    apple.pos = new_pos

            #memanggil gbfs yang berisi posisi pergerakan apel
            best_first_search(new_pos)

            #handle posisi x dan y dari pergerakan snake baik dari head dan badan pertama
            x, y = s.body[0].pos
            xx, yy = s.body[1].pos
            
            #jika head bergerak ke kanan dan nabrak posisi apel maka akan gameover
            if (x + 1, y)  == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))
            #jika head bergerak ke kiri dan lokasi didepannya nabrak posisi apel maka akan gameover
            elif (x - 1, y) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))

            #jika head bergerak ke bawah dan lokasi didepannya nabrak posisi apel maka akan gameover
            elif (x, y + 1) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))
            
            #jika head bergerak ke atas dan lokasi didepannya nabrak posisi apel maka akan gameover
            elif (x, y - 1) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))

            #jika badan pertama bergerak ke kanan dan lokasi didepannya nabrak posisi apel maka akan gameover
            elif (xx + 1, yy) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))

            #jika badan pertama bergerak ke kiri dan lokasi didepannya nabrak posisi apel maka akan gameover
            elif (xx - 1, yy) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))

            #jika badan pertama bergerak ke bawah dan lokasi didepannya nabrak posisi apel maka akan gameover
            elif (xx, yy + 1) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))

            #jika badan pertama bergerak ke atas dan lokasi didepannya nabrak posisi apel maka akan gameover
            elif (xx, yy - 1) == new_pos:
                visited = set({})
                redrawWindow(score, obstacles, lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                score = 0
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))

            #jika posisi kepala bergerak ke kanan dan lokasi didepannya nabrak posisi obstacle maka nambah score
            if (x + 1, y) in obs_pos:
                score += 1;
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                redrawWindow(score, obstacles)
                
                #memastikan agar respawn dari snake tidak berada di obstacle
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

            #jika posisi kepala bergerak ke kiri dan lokasi didepannya nabrak posisi obstacle maka nambah score
            if (x - 1, y) in obs_pos:
                score += 1;
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                redrawWindow(score, obstacles)

                #memastikan agar respawn dari snake tidak berada di obstacle
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

            #jika posisi kepala bergerak ke bawah dan lokasi didepannya nabrak posisi obstacle maka nambah score
            if (x, y + 1) in obs_pos:
                score += 1;
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                redrawWindow(score, obstacles)

                #memastikan agar respawn dari snake tidak berada di obstacle
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
            
            #jika posisi kepala bergerak ke atas dan lokasi didepannya nabrak posisi obstacle maka nambah score
            if (x, y - 1) in obs_pos:
                score += 1;
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                redrawWindow(score, obstacles)

                #memastikan agar respawn dari snake tidak berada di obstacle
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
