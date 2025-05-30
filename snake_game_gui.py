import tkinter as tk
import random

# Ukuran permainan
WIDTH = 600
HEIGHT = 400
SNAKE_SIZE = 20
DELAY = 100  # ms

# Variabel global
direction = 'Right'
snake_coords = []
food_coord = (0, 0)

def start_game():
    global direction, snake_coords
    direction = 'Right'
    snake_coords = [(100, 100), (80, 100), (60, 100)]
    canvas.delete("all")
    place_food()
    move_snake()

def move_snake():
    global direction, snake_coords, food_coord

    head_x, head_y = snake_coords[0]

    if direction == 'Up':
        new_head = (head_x, head_y - SNAKE_SIZE)
    elif direction == 'Down':
        new_head = (head_x, head_y + SNAKE_SIZE)
    elif direction == 'Left':
        new_head = (head_x - SNAKE_SIZE, head_y)
    else:  # 'Right'
        new_head = (head_x + SNAKE_SIZE, head_y)

    # Game over jika menabrak dinding atau diri sendiri
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake_coords):
        canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Game Over", fill="red", font=("Arial", 24))
        return  # Hentikan game, tidak memanggil move_snake lagi

    # Tambahkan kepala baru
    snake_coords = [new_head] + snake_coords

    # Cek apakah makan makanan
    if new_head == food_coord:
        place_food()
    else:
        snake_coords.pop()  # Hapus ekor jika tidak makan

    draw_snake()
    root.after(DELAY, move_snake)

def draw_snake():
    canvas.delete("snake")
    for x, y in snake_coords:
        canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill="green", tag="snake")

def place_food():
    global food_coord
    while True:
        x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        if (x, y) not in snake_coords:
            break
    food_coord = (x, y)
    canvas.delete("food")
    canvas.create_oval(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill="red", tag="food")

def change_direction(new_dir):
    global direction
    opposite = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
    if new_dir != opposite.get(direction):
        direction = new_dir

# Setup window
root = tk.Tk()
root.title("Snake Game - Tkinter")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Keyboard control
root.bind("<Up>", lambda e: change_direction("Up"))
root.bind("<Down>", lambda e: change_direction("Down"))
root.bind("<Left>", lambda e: change_direction("Left"))
root.bind("<Right>", lambda e: change_direction("Right"))

# Start game
start_game()
root.mainloop()

