#import the required libraries

from tkinter import *
import random

window = Tk()
window.title("Snake Game Python")     #title
window.resizable(0,0)

Label(window, text='SUBSCRIBE', font='arial 20 bold').pack(side=BOTTOM) #footer

score = 0 
direction = 'down'

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 180
SPACE_SIZE = 50
BODY_PARTS = 2
SNAKE_COLOR = '#00FF00'
FOOD_COLOR = '#FF0000'
BACKGROUND_COLOR = '#000000'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])

            for x,y in self.coordinates:
                squares = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
                self
``