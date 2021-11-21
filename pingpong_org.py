# Оригінальна версія пінпонга

from tkinter import *
from random import randrange as rnd
import time

root = Tk()
root.geometry('600x800')
canv = Canvas(root, bg='#0044aa')
canv.pack(fill=BOTH, expand=1)


class ball():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.goal = 0
        self.id = canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill='white')

    def move(self):
        self.x += self.vx
        self.y += self.vy
        active_wall = list(set(canv.find_withtag('wall')) & set(
            canv.find_overlapping(self.x - self.r * 0.7, self.y - self.r * 0.7, self.x + self.r * 0.7,
                                  self.y + self.r * 0.7)))
        if active_wall:
            if 'x' in canv.gettags(active_wall[0]):
                self.vx = -self.vx
            if 'y' in canv.gettags(active_wall[0]):
                self.vy = -self.vy
                x1, y1, x2, y2 = canv.coords(active_wall[0])
                xc = (x1 + x2) / 2
                w = abs(x1 - x2)
                self.vx += (self.x - xc) / w * 10
        self.paint()
        lines = canv.find_overlapping(self.x - self.r * 0.7, self.y - self.r * 0.7, self.x + self.r * 0.7,
                                      self.y + self.r * 0.7)
        if len(lines) > 1:
            if "g1" in canv.gettags(lines[1]):
                self.goal = 1
                self.kill()
            if "g2" in canv.gettags(lines[1]):
                self.goal = 2
                self.kill()

    def kill(self):
        global game
        game = 0
        self.x = 300
        self.vx = 0
        if self.goal == 2:
            self.vy = -8
            self.y = 100
        if self.goal == 1:
            self.y = 700
            self.vy = 8
        self.paint()

    def paint(self):
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)


class gamer():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 60
        self.v = 3
        self.d = 4
        self.mode = ''
        self.score = 0
        self.xy_score = (0, 0)
        self.id = canv.create_rectangle(self.x - self.w, self.y - self.d, self.x + self.w, self.y + self.d,
                                        fill='white', tags=('wall', 'y'))
        self.id_score = canv.create_text(0, 0, text='', font='Tahoma 24', fill='white')

    def paint(self):
        canv.coords(self.id, self.x - self.w, self.y - self.d, self.x + self.w, self.y + self.d)
        canv.coords(self.id_score, self.xy_score[0], self.xy_score[1])
        canv.itemconfig(self.id_score, text=self.score)

    def move(self):
        if self.mode == 'left' and self.x > self.w // 2:
            self.x -= self.v
        elif self.mode == 'right' and self.x < (590 - self.w // 2):
            self.x += self.v
        self.paint()


b = ball()
b.x = 100
b.y = 100
b.vx = 4
b.vy = 4

canv.create_line(10, 10, 10, 790, width=10, fill='white', tags=('wall', 'x'))
canv.create_line(590, 10, 590, 790, width=10, fill='white', tags=('wall', 'x'))
canv.create_line(10, 790 / 2, 590, 790 / 2, width=2, fill='white')

canv.create_line(10, 11, 590, 11, width=2, fill='white', tag='g1')
canv.create_line(10, 789, 590, 789, width=2, fill='white', tag='g2')

g1 = gamer()
g1.x = 300
g1.y = 20
g1.paint()
g1.xy_score = (30, 50)

g2 = gamer()
g2.x = 300
g2.y = 780
g2.paint()
g2.xy_score = (30, 450)
game = 1


def key_press(event):
    global game
    if event.keycode == 37:
        g2.mode = 'left'
    elif event.keycode == 39:
        g2.mode = 'right'

    elif event.keycode == 65:
        g1.mode = 'left'
    elif event.keycode == 68:
        g1.mode = 'right'

    elif event.keycode == 32:
        game = 1


def key_release(event):
    if event.keycode == 37 or event.keycode == 39:
        g2.mode = ''

    elif event.keycode == 65 or event.keycode == 68:
        g1.mode = ''


root.bind('<Key>', key_press)
root.bind('<KeyRelease>', key_release)

while 1:
    if game:
        b.move()
    g2.move()
    g1.move()
    if b.goal == 1:
        g2.score += 1
        b.goal = 0
    elif b.goal == 2:
        g1.score += 1
        b.goal = 0
    time.sleep(0.02)
    canv.update()

mainloop()
