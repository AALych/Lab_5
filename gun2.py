import pygame as pg
import numpy as np
from random import randint, choice

SCREEN_SIZE = [800, 600]
# Константы цветов
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)  # цвет экрана
WHITE = (255, 255, 255)  # цвет счетчика
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]  # цвета мишеней
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


class Bomb:
    def __init__(self, coord, vel, rad=15):
        self.color = BLACK
        self.coord = coord
        self.vel = vel
        self.rad = rad
        self.is_alive = True

    def draw(self, screen):
        if self.rad <= 100:
            self.rad += 1
        pg.draw.circle(screen, self.color, self.coord, self.rad, 10)

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
        pg.draw.rect(screen, BLACK, (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]//5))
        counter = labelFont.render(('Ваш счёт: ' + str(self.count)),
                                   False, WHITE)
        bullets = labelFont.render(('Количество пуль: ' + str(self.bullet)),
                                   False, WHITE)
        screen.blit(counter, (0, 0))
        screen.blit(bullets, (0, SCREEN_SIZE[1] // 13))


class Gun:
    def __init__(self, coord=[30, 3 * SCREEN_SIZE[1] // 5],
                 min_pow=20, max_pow=50):
        self.coord = coord
        self.angle = 0
        self.min_pow = min_pow
        self.max_pow = max_pow
        self.power = min_pow
        self.active = False
        self.width = 30
        self.height = 15

    def draw(self, screen):
        end_pos = [int(self.coord[0] + self.power * np.cos(self.angle)),
                   int(self.coord[1] + self.power * np.sin(self.angle))]
        pg.draw.line(screen, RED, self.coord, end_pos, 7)
        pg.draw.rect(screen, RED, [self.coord[0] - self.width, self.coord[1],


                                   self.width + 7, self.height])

    def strike(self):
        vel = [int(self.power * np.cos(self.angle)),
               int(self.power * np.sin(self.angle))]
        self.active = False
        self.power = self.min_pow
        return Ball(list(self.coord), vel)

    def attack(self):
        vel = [int(self.power * np.cos(self.angle)),
               int(self.power * np.sin(self.angle))]
        self.active = False
        self.power = self.min_pow
        return Bomb(list(self.coord), vel)

    def move(self):
        if self.active and self.power < self.max_pow:
            self.power += 1

    def set_angle(self, mouse_pos):
        self.angle = np.arctan2(mouse_pos[1] - self.coord[1],
                                mouse_pos[0] - self.coord[0])


class TargetA:
    # Класс целей первого вида
    def __init__(self, min_rad=20, max_rad=50):
        '''
        self.rad - радиус мишени
        self.x - координаты по горизонтали
        self.y - кородинаты по вертикали
        self.color - цвет мишени
        self.speed - скорость мишени
        '''
        self.rad = randint(min_rad, max_rad)
        self.x = randint(2 * SCREEN_SIZE[0] // 3, SCREEN_SIZE[0] - self.rad)
        self.y = randint(SCREEN_SIZE[1] // 5 + self.rad,
                         SCREEN_SIZE[1] - self.rad)
        self.color = RED
        self.speed = 20

    def draw(self, screen):
        # рисование мишени
        pg.draw.circle(screen, self.color, [self.x, self.y], self.rad)

    def move(self):
        # движение мишени
        if SCREEN_SIZE[1]/5 + self.rad < self.y < SCREEN_SIZE[1] - self.rad:
            self.y += self.speed
        else:
            self.speed = - self.speed
            self.y += self.speed

    def hit(self, obj, count: Table, min_rad=20, max_rad=50):
        # функция, определябщая попали или нет
        if (self.x - obj.coord[0]) ** 2 + (self.y - obj.coord[1]) ** 2 <= \
                (self.rad + obj.rad) ** 2:
            # добавление звука при столкновении
            Oof = 'Oof.ogg'
            pg.init()
            pg.mixer.init()
            pg.mixer.music.load(Oof)
            pg.mixer.music.play(1)
            count.increase(1)  # увеличение счета
            # рисование новой мишени
            self.rad = randint(min_rad, max_rad)
            self.x = randint(2 * SCREEN_SIZE[0] // 3, SCREEN_SIZE[0] - self.rad)
            self.y = randint(SCREEN_SIZE[1]//5 + self.rad,
                             SCREEN_SIZE[1] - self.rad)


class TargetB:
    # класс мишений второго вида
    def __init__(self, min_rad=30, max_rad=50):
        '''
        self.rad - радиус мишени
        self.x - координаты по горизонтали
        self.y - кородинаты по вертикали
        self.color - цвет мишени
        self.Vx - скорость мишени по горизонтали
        self.Vy - скорость мишени по вертикали
        '''
        self.rad = randint(min_rad, max_rad)
        self.x = randint(SCREEN_SIZE[0] // 3 + self.rad,
                         SCREEN_SIZE[0] - self.rad)
        self.y = randint(SCREEN_SIZE[1] // 5 + self.rad,
                         SCREEN_SIZE[1] - self.rad)
        self.color = choice(COLORS)
        self.Vy = randint(10, 20)
        self.Vx = randint(10, 20)

    def draw(self, screen):
        # рисование мишени
        self.color = choice(COLORS)
        pg.draw.circle(screen, self.color, [self.x, self.y], self.rad)

    def move(self):
        # движение мишени
        if SCREEN_SIZE[1]/5 + self.rad < self.y < SCREEN_SIZE[1] - self.rad:
            self.y += self.Vy
        else:
            self.Vy = - self.Vy
            self.y += self.Vy
        if SCREEN_SIZE[0]/3 + self.rad < self.x < SCREEN_SIZE[0] - self.rad:
            self.x += self.Vx
        else:
            self.Vx = - self.Vx
            self.x += self.Vx

    def hit(self, obj: Ball, count: Table, min_rad=20, max_rad=50):
        # проверяет, столкнулся или нет
        if (self.x - obj.coord[0]) ** 2 + (self.y - obj.coord[1]) ** 2 <= \
                (self.rad + obj.rad) ** 2:
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
        self.bombs = []
        self.targets = [TargetA() for i in range(2)]
        target = TargetB()
        self.targets.append(target)

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
        for bomb in self.bombs:
            bomb.draw(screen)
            for target in self.targets:
                target.hit(bomb, self.table)
        for target in self.targets:
            target.draw(screen)
        self.table.draw()
        self.gun.draw(screen)

    def move(self):
        for ball in self.balls:
            ball.move()
        for bomb in self.bombs:
            bomb.move()
        self.gun.move()
        for target in self.targets:
            target.move()

    def check_alive(self):
        dead_balls = []
        dead_bombs = []
        for i, ball in enumerate(self.balls):
            if not ball.is_alive:
                dead_balls.append(i)

        for i in reversed(dead_balls):
            self.balls.pop(i)

        for i, bomb in enumerate(self.bombs):
            if not bomb.is_alive:
                dead_bombs.append(i)

        for i in reversed(dead_balls):
            self.bombs.pop(i)

    def handle_events(self, events):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                # движение пушки
                if event.key == pg.K_UP:
                    self.gun.coord[1] -= 5
                elif event.key == pg.K_DOWN:
                    self.gun.coord[1] += 5
                elif event.key == pg.K_LEFT:
                    self.gun.coord[0] -= 5
                elif event.key == pg.K_RIGHT:
                    self.gun.coord[0] += 5
            elif event.type == pg.MOUSEBUTTONDOWN:
                # настройка мощности
                if event.button == 1 or event.button == 3:
                    self.gun.active = True
            elif event.type == pg.MOUSEBUTTONUP:
                # выстрел
                if event.button == 1:
                    self.balls.append(self.gun.strike())
                    self.table.shoot()
                if event.button == 3:
                    self.bombs.append(self.gun.attack())
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
labelFont = pg.font.SysFont('Comic Sans MS', SCREEN_SIZE[1]//15)
# задание шрифта счетчика

mgr = Manager()

done = False

while not done:
    clock.tick(15)

    done = mgr.process(pg.event.get(), screen)

    pg.display.flip()
