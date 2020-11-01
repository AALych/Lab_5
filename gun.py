import pygame as pg
import numpy as np
from random import randint

SCREEN_SIZE = [800, 600]
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (245, 245, 245)

pg.init()


class Ball:
    def __init__(self, coord, vel, rad=15, color=None):
        if color is None:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color
        self.coord = coord
        self.vel = vel
        self.rad = rad
        self.is_alive = True

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.rad)

    def move(self, t_step=1., g=2.):
        self.vel[1] += int(g * t_step)
        for i in range(2):
            self.coord[i] += int(self.vel[i] * t_step)
        self.check_walls()
        if self.vel[0] ** 2 + self.vel[1] ** 2 < 2 ** 2 and self.coord[1] > \
                SCREEN_SIZE[1] - 2 * self.rad:
            self.is_alive = False

    def check_walls(self):
        n = [[1, 0], [0, 1]]
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.flip_vel(n[i], 0.8, 0.9)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.flip_vel(n[i], 0.8, 0.9)

    def flip_vel(self, axis, coef_perp=1., coef_par=1.):
        vel = np.array(self.vel)
        n = np.array(axis)
        n = n / np.linalg.norm(n)
        vel_perp = vel.dot(n) * n
        vel_par = vel - vel_perp
        ans = -vel_perp * coef_perp + vel_par * coef_par
        self.vel = ans.astype(np.int).tolist()


class Table:
    """
    Класс счетчика очков
    """

    def __init__(self):
        # В начале счет равен 0
        self.count = 0
        self.bullet = 0

    def increase(self, points):
        """
        Функция, увеличивающая счет пи попадании
        points - количество очков, начисляемое за попадание
        """
        self.count += points

    def shoot(self):
        self.bullet += 1

    def draw(self):
        # Функция рисования самого счетчика
        pg.draw.rect(screen, BLACK, (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]/5))
        counter = labelFont.render((str(self.count) + str('  ') +
                                    str(self.bullet)), False, WHITE)
        screen.blit(counter, (0, 0))


class Gun:
    def __init__(self, coord=[30, 3 * SCREEN_SIZE[1] // 5],
                 min_pow=20, max_pow=50):
        self.coord = coord
        self.angle = 0
        self.min_pow = min_pow
        self.max_pow = max_pow
        self.power = min_pow
        self.active = False

    def draw(self, screen):
        end_pos = [int(self.coord[0] + self.power * np.cos(self.angle)),
                   int(self.coord[1] + self.power * np.sin(self.angle))]
        pg.draw.line(screen, RED, self.coord, end_pos, 5)

    def strike(self):
        vel = [int(self.power * np.cos(self.angle)),
               int(self.power * np.sin(self.angle))]
        self.active = False
        self.power = self.min_pow
        return Ball(list(self.coord), vel)

    def move(self):
        if self.active and self.power < self.max_pow:
            self.power += 1

    def set_angle(self, mouse_pos):
        self.angle = np.arctan2(mouse_pos[1] - self.coord[1],
                                mouse_pos[0] - self.coord[0])


class Target:
    def __init__(self, min_rad=20, max_rad=50):
        self.rad = randint(min_rad, max_rad)
        self.x = randint(2 * SCREEN_SIZE[0] // 3, SCREEN_SIZE[0] - self.rad)
        self.y = randint(SCREEN_SIZE[1] // 5 + self.rad,
                         SCREEN_SIZE[1] - self.rad)
        self.color = RED
        self.speed = 20

    def draw(self, screen):
        pg.draw.circle(screen, self.color, [self.x, self.y], self.rad)

    def move(self):
        if SCREEN_SIZE[1]/5 + self.rad < self.y < SCREEN_SIZE[1] - self.rad:
            self.y += self.speed
        else:
            self.speed = - self.speed
            self.y += self.speed

    def hit(self, obj: Ball, count: Table, min_rad=20, max_rad=50):
        if (self.x - obj.coord[0]) ** 2 + (self.y - obj.coord[1]) ** 2 <= \
                (self.rad + obj.rad) ** 2:
            Oof = 'Oof.mp3'
            pg.init()
            pg.mixer.init()
            pg.mixer.music.load(Oof)
            pg.mixer.music.play(1)
            count.increase(1)
            self.rad = randint(min_rad, max_rad)
            self.x = randint(2 * SCREEN_SIZE[0] // 3, SCREEN_SIZE[0] - self.rad)
            self.y = randint(SCREEN_SIZE[1]//5 + self.rad,
                             SCREEN_SIZE[1] - self.rad)


class Manager:
    def __init__(self):
        self.gun = Gun()
        self.table = Table()
        self.balls = []
        self.targets = [Target() for i in range(2)]

    def process(self, events, screen):
        done = self.handle_events(events)
        self.move()
        self.draw(screen)
        self.check_alive()
        return done

    def draw(self, screen):
        screen.fill(WHITE)
        for ball in self.balls:
            ball.draw(screen)
            for target in self.targets:
                target.hit(ball, self.table)
        for target in self.targets:
            target.draw(screen)
        self.table.draw()
        self.gun.draw(screen)

    def move(self):
        for ball in self.balls:
            ball.move()
        self.gun.move()
        for target in self.targets:
            target.move()

    def check_alive(self):
        dead_balls = []
        for i, ball in enumerate(self.balls):
            if not ball.is_alive:
                dead_balls.append(i)

        for i in reversed(dead_balls):
            self.balls.pop(i)

    def handle_events(self, events):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.gun.coord[1] -= 5
                elif event.key == pg.K_DOWN:
                    self.gun.coord[1] += 5
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gun.active = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.balls.append(self.gun.strike())
                    self.table.shoot()

        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)

        return done


screen = pg.display.set_mode(SCREEN_SIZE)
pg.draw.rect(screen, WHITE, (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))
pg.display.set_caption("The gun of Khiryanov")
clock = pg.time.Clock()
score = Table()  # создание экземпляра счетчика
labelFont = pg.font.SysFont('Comic Sans MS', 50)  # задание шрифта счетчика

mgr = Manager()

done = False

while not done:
    clock.tick(15)

    done = mgr.process(pg.event.get(), screen)

    pg.display.flip()
