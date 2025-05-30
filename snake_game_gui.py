import tkinter as tk
import random
import heapq

# Ukuran permainan
WIDTH = 600
HEIGHT = 400
SNAKE_SIZE = 20
DELAY = 100  # ms

# Variabel global
direction = 'Right'
snake_coords = []
food_coord = (0, 0)
score = 0
use_ai = True

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start, goal, snake_body):
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}
    directions = [(SNAKE_SIZE, 0), (-SNAKE_SIZE, 0), (0, SNAKE_SIZE), (0, -SNAKE_SIZE)]

    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < WIDTH and 0 <= neighbor[1] < HEIGHT and neighbor not in snake_body):
                tentative_g_score = current_g + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))

    return None

def start_game():
    global direction, snake_coords, score
    play_again_btn.pack_forget()  # Sembunyikan tombol saat mulai game baru
    direction = 'Right'
    snake_coords.clear()
    snake_coords.extend([(100, 100), (80, 100), (60, 100)])
    score = 0
    score_label.config(text="Score: 0")
    canvas.delete("all")
    place_food()
    move_snake()

def move_snake():
    global direction, snake_coords, food_coord, score

    if use_ai:
        path = astar(snake_coords[0], food_coord, snake_coords)
        if path and len(path) > 0:
            next_pos = path[0]
            dx = next_pos[0] - snake_coords[0][0]
            dy = next_pos[1] - snake_coords[0][1]
            if dx == SNAKE_SIZE: direction = 'Right'
            elif dx == -SNAKE_SIZE: direction = 'Left'
            elif dy == SNAKE_SIZE: direction = 'Down'
            elif dy == -SNAKE_SIZE: direction = 'Up'

    head_x, head_y = snake_coords[0]

    if direction == 'Up':
        new_head = (head_x, head_y - SNAKE_SIZE)
    elif direction == 'Down':
        new_head = (head_x, head_y + SNAKE_SIZE)
    elif direction == 'Left':
        new_head = (head_x - SNAKE_SIZE, head_y)
    else:
        new_head = (head_x + SNAKE_SIZE, head_y)

    # Game Over kondisi
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake_coords):
        canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Game Over", fill="red", font=("Arial", 24))
        play_again_btn.pack()  # Tampilkan tombol Play Again
        return

    snake_coords = [new_head] + snake_coords

    if new_head == food_coord:
        score += 1
        score_label.config(text=f"Score: {score}")
        place_food()
    else:
        snake_coords.pop()

    draw_snake()
    root.after(DELAY, move_snake)

def draw_snake():
    canvas.delete("snake")
    for x, y in snake_coords:
        canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill="green", tag="snake")
    canvas.delete("food")
    fx, fy = food_coord
    canvas.create_oval(fx, fy, fx + SNAKE_SIZE, fy + SNAKE_SIZE, fill="red", tag="food")

def place_food():
    global food_coord
    while True:
        x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        if (x, y) not in snake_coords:
            food_coord = (x, y)
            break

def change_direction(new_dir):
    global direction
    opposite = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
    if not use_ai and new_dir != opposite.get(direction):
        direction = new_dir

def toggle_mode():
    global use_ai
    use_ai = not use_ai
    mode_btn.config(text=f"Mode: {'AI' if use_ai else 'Manual'}")

# Setup window
root = tk.Tk()
root.title("Snake Game with AI and Score")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

score_label = tk.Label(root, text="Score: 0", font=("Arial", 14))
score_label.pack()

mode_btn = tk.Button(root, text="Mode: AI", command=toggle_mode)
mode_btn.pack()

play_again_btn = tk.Button(root, text="Play Again", command=start_game)
play_again_btn.pack()
play_again_btn.pack_forget()  # Sembunyikan dulu sampai game over

# Keyboard control
root.bind("<Up>", lambda e: change_direction("Up"))
root.bind("<Down>", lambda e: change_direction("Down"))
root.bind("<Left>", lambda e: change_direction("Left"))
root.bind("<Right>", lambda e: change_direction("Right"))

# Start game
start_game()
root.mainloop()
