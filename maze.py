""" Drone Maze Game """
import turtle
import math
import time
import pygame
import json
import random
import sys
from numpy import array

STEP_COUNT = 24

class Pen(turtle.Turtle):
    """
    Draws the maze

    Args:
        turtle (_type_): turtle object
    """
    def  __init__(self):
        """_summary_
        """
        turtle.Turtle.__init__(self)
        screen = self.getscreen()
        screen.register_shape("./image/block.gif")
        self.shape("./image/block.gif")
        self.color("white")
        self.penup()
        self.speed(3)

class Drone(turtle.Turtle):
    """
    Moves the drone object

    Args:
        turtle (_type_): turtle object
    """
    def __init__(self):
        turtle.Turtle.__init__(self)
        screen = self.getscreen()
        screen.register_shape("./image/drone.gif")
        self.shape("./image/drone.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0

    def go_up(self, count=1):
        """_summary_

        Args:
            count (int, optional): _description_. Defaults to 1.
        """
        move_to_x = player.xcor()
        move_to_y = player.ycor() + (count * STEP_COUNT)

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self, count=1):
        move_to_x = player.xcor()
        move_to_y = player.ycor() - (count * STEP_COUNT)

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self, count=1):
        move_to_x = player.xcor() - (count * STEP_COUNT)
        move_to_y = player.ycor()

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self, count=1):
        move_to_x = player.xcor() + (count * STEP_COUNT)
        move_to_y = player.ycor()

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    # TODO - use collision
    def is_collision(self, other):
        pos_x = self.xcor()-other.xcor()
        pos_y = self.ycor()-other.ycor()
        distance = math.sqrt((pos_x**2)+(pos_y**2))
        return distance < 5

class Treasure(turtle.Turtle):
    """
    A treasure object

    Args:
        turtle (_type_): turtle object
    """
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        screen = self.getscreen()
        screen.register_shape("./image/treasure.gif")
        self.shape("./image/treasure.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x,y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

class Button:
    """
    A button object
    """
    def __init__(self, message: str, pos_x=-500, pos_y=100, pos_w=150, pos_h=50):
        self.message = message
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_w = pos_w
        self.pos_h = pos_h

    def render(self, pen: turtle.Turtle):
        pen.penup()
        pen.color("black", "green")
        pen.begin_fill()
        pen.goto(self.pos_x, self.pos_y)
        pen.goto(self.pos_x + self.pos_w, self.pos_y)
        pen.goto(self.pos_x + self.pos_w, self.pos_y + self.pos_h)
        pen.goto(self.pos_x, self.pos_y + self.pos_h)
        pen.goto(self.pos_x, self.pos_y)
        pen.end_fill()
        pen.goto(self.pos_x + 15, self.pos_y + 15)
        pen.write(self.message, font=("Courier", 18))

def load_maps():
    with open('./assets/mazes.json') as maze_file:
        return json.load(maze_file)

def setup_maze(level: array):
    for pos_y in range(len(level)):
        for pos_x in range(len(level[pos_y])):
            character = level[pos_y][pos_x]
            print(f"Parsing position {pos_x}, {pos_y}: {character}")
            maze_x = -288 + (pos_x * 24)
            maze_y = 288 - (pos_y * 24)

            if character == "X":
                pen.goto(maze_x, maze_y)
                pen.stamp()
                walls.append((maze_x, maze_y))
            elif character == "P":
                player.goto(maze_x, maze_y)
            elif character == "T":
                treasures.append(Treasure(maze_x, maze_y))
            elif character == "G":
                # TODO: Make this trigger the win
                print(f"Goal defined at {pos_x}, {pos_y}")
    wn.update()

    canvas = turtle.getcanvas()
    canvas.bind('<Motion>', on_click)


def on_click(event):
    pos_x, pos_y = event.x, event.y
    print('x={}, y={}'.format(pos_x, pos_y))
    # TODO capture start/reset button clicks
    # if (x >= 600 and x <= 800) and (  y >= 280 and y <= 300):
    #     turtle.onscreenclick(lambda x, y: turtle.bgcolor('red'))


def countdown_timer():
    turtle.speed(0)
    turtle.penup()
    turtle.clear()
    turtle.goto(-500, 150)
    turtle.write((str(int(time.time() - start))) + " seconds", font=("Courier", 18))

# TODO This needs a refactor!! Is it needed...
def start_time():
    treasure.destroy()
    treasures.remove(treasure)
    wn.update()

    pygame.mixer.music.load("./Music/Gameover.wav")
    pygame.mixer.music.play(4)

    start_timer = time()

    #struct = time.localtime(start_timer)

    turtle.speed(0)
    turtle.penup()
    turtle.goto(10, 300)
    turtle.color("red")
    turtle.write(" It's a fake gold!!! In to laggy mode!!!",align="left", font=(10))
    turtle.goto(-50,300)
    turtle.write("\nRespawn in 5 seconds",align="right", font=(0.0000001))
    turtle.goto(2000,2000)

    i = 5
    while i> -1:
        i-=1
        screen = turtle.Turtle()
        screen.pencolor = ("blue")
        screen.goto(0,0)
        screen.write(i+1, font=(0.0000001))
        screen.penup()
        screen.goto(2000, 2000)
        time.sleep(1)
        wn.update()
        screen.clear()
    pygame.mixer.music.load("./Music/SoundTest.wav")
    pygame.mixer.music.play(-1)
    turtle.clear()


if __name__ == "__main__":
    # Set up window
    wn = turtle.Screen()
    wn.bgcolor("black")
    wn.title("Drone commander")
    wn.setup(1700, 700)
    wn.tracer(0)
    wn.bgpic("./image/giphy.gif")

    # Play annoying music
    pygame.mixer.init()
    pygame.mixer.music.load("./Music/SoundTest.wav")
    pygame.mixer.music.play(-1)

    # Initialise buttons, timer, etc
    pen = Pen()
    start = time.time()
    start_button = Button("Start Game", -500, 100, 150, 50).render(pen)
    reset_button = Button("Reset Game", -500, 20, 150, 50).render(pen)

    walls = []
    treasures = []

    # Set up maze
    maps = load_maps()
    map_index = random.randrange(len(maps))
    print(f"Setting up map using map: {map_index}")
    player = Drone()
    setup_maze(maps[map_index])
    print("Map has been setup")

    # TODO turn off keypress and read commands from input
    turtle.listen()
    turtle.onkey(player.go_left,"Left")
    turtle.onkey(player.go_right,"Right")
    turtle.onkey(player.go_up,"Up")
    turtle.onkey(player.go_down,"Down")

    gold_left = 3

    while True:
        for treasure in treasures:
            if player.is_collision(treasure):
                player.gold += treasure.gold
                gold_left = gold_left-1
                print(gold_left)
                if player.gold == 100:
                    start_time()
                else:
                    turtle.clear()
                    turtle.goto(-50,300)
                    turtle.write(f"Player Gold:{player.gold}", font=(0.0000001))
                    turtle.goto(2000, 2000)
                    treasure.destroy()
                    wn.update()
        try:
            countdown_timer()
            wn.update()
        except:
            print("Exit game")
            sys.exit(0)
