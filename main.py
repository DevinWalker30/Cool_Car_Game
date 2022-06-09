import pygame as pg
import sprites
from settings import *
import random


class Game():
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        self.bg = pg.image.load("images/road.svg")
        self.bg = pg.transform.scale(self.bg, (WIDTH*2, HEIGHT*2))

        self.vehicles = []
        for i in range(4, 6):
            path = f'images/car-truck{i}.png'
            vehicle = pg.image.load(path)
            vehicle = pg.transform.rotate(vehicle, 180)
            self.vehicles.append(vehicle)

        self.score = 0
        self.lives = None

    def display_score(self):
        score = MED_FONT.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score, (60, 7))

    def new(self):
        '''create all game objects, sprites, and sprite groups and call run()'''
        self.player_grp = pg.sprite.GroupSingle()
        self.enemy_grp = pg.sprite.Group()

        self.score = 0

        self.player = sprites.Player(WIDTH//2, HEIGHT-2*P_SIZE)
        for i in range(ENEMY_COUNT):
            vehicle = random.choice(self.vehicles)
            rand_x = random.randint(3*E_SIZE, WIDTH-2*E_SIZE)
            rand_y = random.randint(-250, -150)
            self.enemy = sprites.Enemy(rand_x, rand_y, vehicle)
            self.enemy_grp.add(self.enemy)

            self.lives = []
            for i in range(LIVES):
                dimensions = (10, 30)
                life = pg.Surface(dimensions)
                life.fill(YELLOW)
                self.lives.append(life)

        self.player_grp.add(self.player)


        self.run()


    def run(self):
        '''contains main game loop'''

        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def detect_collision(self):
        hit_list = pg.sprite.groupcollide(self.player_grp, self.enemy_grp, True, True)
        if hit_list:
            self.lives.pop()


    def update(self):
        # game loop - update
        self.player_grp.update()
        self.enemy_grp.update()
        self.detect_collision()

        if self.player.rect.y <= 50:
            self.score += 10

        if len(self.enemy_grp) < ENEMY_COUNT:
            vehicle = random.choice(self.vehicles)
            rand_x = random.randint(3*E_SIZE, WIDTH - 2*E_SIZE)
            rand_y = random.randint(-250, -150)
            self.enemy = sprites.Enemy(rand_x, rand_y, vehicle)
            self.enemy_grp.add(self.enemy)

        if len(self.player_grp) < 1:
            self.player = sprites.Player(WIDTH//2, HEIGHT - 2*P_SIZE)
            self.player_grp.add(self.player)

        if len(self.lives) == 0:
            self.playing = False

    def draw(self):
        '''fill screen, draw objects, sprites to the display, and flip'''
        self.screen.fill(RED)
        self.screen.blit(self.bg, (0, -10))
        self.display_score()
        for index, life in enumerate(self.lives):
            location = (400+index*20, 15)
            self.screen.blit(life, location)

        # anything to be drawn to screen goes here
        pg.draw.rect(SCREEN, BLACK, (0, 50, WIDTH, 10))
        self.player_grp.draw(SCREEN)
        self.enemy_grp.draw(SCREEN)


        pg.display.flip()


    def events(self):
        # game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    self.player.x_velo = +5
                elif event.key == pg.K_LEFT:
                    self.player.x_velo = -5
                elif event.key == pg.K_UP:
                    self.player.y_velo -= 5
                elif event.key == pg.K_DOWN:
                    self.player.y_velo += 5
            if event.type == pg.KEYUP:
                self.player.x_velo = 0
                self.player.y_velo = 0


    def show_start_screen(self):
        # screen to start game
        pg.init()
        pg.mixer.init()
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        clock = pg.time.Clock()
        running = True

        title = LRG_FONT.render('Press Space To Start', True, WHITE)

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        running = False

            screen.fill(BLACK)
            screen.blit(title, (60, 7))
            pg.display.flip()


    def show_go_screen(self):
        # screen when game over
        pg.init()
        pg.mixer.init()
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        clock = pg.time.Clock()
        running = True

        title = MED_FONT.render('Press Space To Start New Game', True, WHITE)
        title2 = MED_FONT.render('Press Q to Quit', True, WHITE)
        title3 = MED_FONT.render(f'Final score: {self.score}', True, WHITE)
        title4 = MED_FONT.render('UR Trash', True, WHITE)

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        running = False
                    elif event.key == pg.K_SPACE:
                        quit()

            screen.fill(BLACK)
            screen.blit(title, (60, 7))
            screen.blit(title2, (200, 57))
            screen.blit(title3, (210, 207))
            if self.score == 0:
                screen.blit(title4, (250, 257))
            pg.display.flip()


#################################################
###                 PLAY GAME                 ###
#################################################

game = Game()
game.show_start_screen()

while game.running:
    game.new()
    game.show_go_screen()

pg.quit()