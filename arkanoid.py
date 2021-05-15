from tkinter import*
from random import*
import time


class Paddle:
    def __init__(self, c, color):
        self.c = c
        self.id = self.c.create_rectangle(0, 0, 100, 10, fill=color)
        self.starting_point_x = randrange(40, 200)
        self.c.move(self.id, self.starting_point_x, 300)
        self.x = 0
        self.started = False
        self.c.bind_all("<KeyPress-Right>", self.turn_right)
        self.c.bind_all("<KeyPress-Left>", self.turn_left)
        self.c.bind_all("<KeyPress-Return>", self.start_game)

    def turn_left(self, event):
        self.x = -2

    def turn_right(self, event):
        self.x = 2

    def start_game(self, event):
        self.started = True

    def draw(self):
        self.c.move(self.id, self.x, 0)
        pos = self.c.coords(self.id)
        if pos[0] <= 0:
            self.x = 2
        if pos[2] >= 500:
            self.x = -2


class Ball:
    def __init__(self, c, paddle, score, color):
        self.c = c
        self.paddle = paddle
        self.score = score
        self.id = self.c.create_oval(10, 10, 25, 25, fill=color)
        self.c.move(self.id, 245, 100)
        starts = [-2, -1, 1, 2]
        self.x = choice(starts)
        self.y = -2
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.c.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.score.hit()
                return True
        else:
            return False


    def draw(self):
        self.c.move(self.id, self.x, self.y)
        pos = self.c.coords(self.id)
        if pos[0] <= 0 or pos[2] >= 500:
            self.x *= -1
        if pos[1] <= 0 or self.hit_paddle(pos):
            self.y *= -1
        if pos[3] >= 400:
            self.hit_bottom = True
            self.c.create_text(250,50,text="Вы проиграли!",font=('Georgia',20), fill='red')

class Score:
    def __init__(self, c, color):
        self.score = 0
        self.c = c
        self.id = self.c.create_text(450, 10, text=self.score, font=("Arial",10), fill=color)

    def hit(self):
        self.score+=1
        self.c.itemconfig(self.id, text=self.score)


a = Tk()
a.iconbitmap("images/icon.ico")
a.title('Arkanoid')
a.resizable(width=False, height=False)
a.wm_attributes('-topmost', 1)
c = Canvas(a, width=500, height=400)
c.pack()
a.update()

paddle = Paddle(c, "white")
score = Score(c, "green")
ball = Ball(c, paddle, score, "red2")

while not ball.hit_bottom:
    if paddle.started:
        paddle.draw()
        ball.draw()
    a.update()
    time.sleep(0.01)

time.sleep(3)
