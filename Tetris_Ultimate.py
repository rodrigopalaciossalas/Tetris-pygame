import pygame
import random
import sys
from button import Button
colors = [
    (1, 1, 128),            #Azul
    (150, 50, 255),          #Morado
    (255, 128, 1),          #Naranja
    (255, 255, 1),          #Amarillo
    (25, 255, 255),          #Celeste
    (1, 255, 1),            #Verde
    (255, 1, 1),            #Rojo
]
class Figure:
    figures = [
    [[1,5,9,13],[4,5,6,7]],                     #I
    [[1,4,5,6],[1,2,5,6],[4,5,6,10],[1,5,8,9]],     #J
    [[1,4,5,6],[1,5,6,9],[4,5,6,9],[1,4,5,9]],      #T
    [[2,4,5,6],[1,5,9,10],[4,5,6,8],[0,1,5,9]],     #L
    [[1,2,5,6]],                                 #O
    [[1,2,4,5],[0,4,5,9]],                          #S
    [[0,1,5,6],[1,4,5,8]],                          #Z
    ]
    def __init__(self, x, y):
        self.x =x                  #Posicion 3 de (0-9)
        self.y = y                  #Posicion 0 de (0-19)
        self.type=random.randint(0, len(self.figures) - 1) #Tipo figura
        self.rotation = 0           #Rotacion inicial
    def image(self):                #Forma de la figura
        return self.figures[self.type][self.rotation]
    def rotate(self):               #Rotacion de la figura
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])
class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.x = 100
        self.y = 50
        self.zoom = 20
        self.figure = None
        self.height = height
        self.width = width
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(-1)
            self.field.append(new_line)
    def new_figure(self):
        self.figure = Figure(3, 0)
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or j + self.figure.x > self.width - 1 or j + self.figure.x < 0 or self.field[i + self.figure.y][j + self.figure.x] >= 0:
                        intersection = True
        return intersection
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == -1:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.type
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"
    def go_side(self, mov_x):
        old_x = self.figure.x
        self.figure.x += mov_x
        if self.intersects():
            self.figure.x = old_x
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation
class Juego:
    def __init__(self):
        self.size=(400, 500)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tetris")
        self.fondo=pygame.image.load('fondo.jpg')
        self.fondo=pygame.transform.scale(self.fondo,self.size)
        pygame.mixer.music.load("music_base.mp3")
        self.done=False
        self.fps=5
        self.contador=0
        self.pressing_down=False
    def quit(self):
        pygame.quit()
        sys.exit()
    def play(self,mievento):
        clock=pygame.time.Clock()
        self.new_fondo=pygame.image.load('fondo_juego.jpg')
        self.new_fondo=pygame.transform.scale(self.new_fondo,self.size)
        game=Tetris(20,10)
        while True:
            self.screen.blit(self.new_fondo,(0,0))
            if game.figure is None:
                game.new_figure()
            self.contador=+1
            if self.contador>1000000:
                self.contador=0
            if self.contador % (self.fps // game.level // 2) == 0 or self.pressing_down:
                if game.state == "start":
                    game.go_down()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.rotate()
                    if event.key == pygame.K_DOWN:
                        self.pressing_down = True
                    if event.key == pygame.K_LEFT:
                        game.go_side(-1)
                    if event.key == pygame.K_RIGHT:
                        game.go_side(1)
                    if event.key == pygame.K_SPACE:
                        game.go_space()
                    if event.key == pygame.K_ESCAPE:
                        game.__init__(20, 10)
            if mievento.type == pygame.KEYUP:
                if mievento.key == pygame.K_DOWN:
                    self.pressing_down = False
            for i in range(game.height):#gradilla
                for j in range(game.width):
                    pygame.draw.rect(self.screen, (128,128,128), [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                    if game.field[i][j] >= 0:
                        pygame.draw.rect(self.screen, colors[game.field[i][j]],
                                        [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])
            if game.figure is not None:#pintar pantalla
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in game.figure.image():
                            pygame.draw.rect(self.screen, colors[game.figure.type],
                                            [game.x + game.zoom * (j + game.figure.x) + 1,
                                            game.y + game.zoom * (i + game.figure.y) + 1,
                                            game.zoom - 2, game.zoom - 2])
            font = pygame.font.SysFont('Arial', 25, True, False)
            font1 = pygame.font.SysFont('Arial', 65, True, False)
            text = font.render("Score: " + str(game.score), True, (1,1,250))
            text_game_over = font1.render("Game Over", True, (125, 125, 125))
            text_game_over1 = font1.render("Press ESC", True, (0, 0, 0))
            self.screen.blit(text, [5, 5])
            if game.state == "gameover":
                self.screen.blit(text_game_over, [20, 200])
                self.screen.blit(text_game_over1, [25, 265])
            pygame.display.update()
            clock.tick(self.fps)
    def menu(self):
        pygame.mixer.music.play(3)
        while not self.done:
            self.screen.blit(self.fondo,(0,0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            PLAY_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"),(200,75)), pos=(200, 300), 
                            text_input="PLAY", font=pygame.font.Font("assets/font.ttf", 30), base_color="Black", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/Quit Rect.png"),(200,75)), pos=(200, 450), 
                            text_input="QUIT", font=pygame.font.Font("assets/font.ttf", 30), base_color="Black", hovering_color="White")
            for button in [PLAY_BUTTON,QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play(event)
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.quit()   
            pygame.display.update()
def main():
    pygame.init()
    miJuego=Juego()
    miJuego.menu()
    pygame.quit()
main()



