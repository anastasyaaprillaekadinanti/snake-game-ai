import tkinter as tk
import random
import heapq

# Konfigurasi dasar
WIDTH = 600
HEIGHT = 400
GRID = 20
DELAY = 100

# Game state
snake = []
food = (0, 0)
score = 0
direction = 'Right'
is_ai = True

# Fungsi heuristik Manhattan
def heuristik(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* pathfinding
def cari_jalur(start, goal, badan):
    bukaan = []
    heapq.heappush(bukaan, (heuristik(start, goal), 0, start))
    asal = {}
    skor_g = {start: 0}
    gerakan = [(GRID, 0), (-GRID, 0), (0, GRID), (0, -GRID)]

    while bukaan:
        _, g_sekarang, pos = heapq.heappop(bukaan)
        if pos == goal:
            jalur = []
            while pos in asal:
                jalur.append(pos)
                pos = asal[pos]
            return jalur[::-1]

        for dx, dy in gerakan:
            next_pos = (pos[0] + dx, pos[1] + dy)
            if 0 <= next_pos[0] < WIDTH and 0 <= next_pos[1] < HEIGHT and next_pos not in badan:
                g_baru = g_sekarang + 1
                if next_pos not in skor_g or g_baru < skor_g[next_pos]:
                    asal[next_pos] = pos
                    skor_g[next_pos] = g_baru
                    f = g_baru + heuristik(next_pos, goal)
                    heapq.heappush(bukaan, (f, g_baru, next_pos))
    return []

# Mulai ulang game
def mulai_game():
    global snake, direction, score
    play_again_btn.place_forget()
    direction = 'Right'
    snake = [(100, 100), (80, 100), (60, 100)]
    score = 0
    update_skor()
    canvas.delete("all")
    letakkan_makanan()
    gerak_ular()

# Gerakan ular
def gerak_ular():
    global snake, food, direction, score

    if is_ai:
        jalur = cari_jalur(snake[0], food, snake)
        if jalur:
            tujuan = jalur[0]
            dx = tujuan[0] - snake[0][0]
            dy = tujuan[1] - snake[0][1]
            if dx == GRID: direction = 'Right'
            elif dx == -GRID: direction = 'Left'
            elif dy == GRID: direction = 'Down'
            elif dy == -GRID: direction = 'Up'

    kepala = snake[0]
    if direction == 'Up':
        baru = (kepala[0], kepala[1] - GRID)
    elif direction == 'Down':
        baru = (kepala[0], kepala[1] + GRID)
    elif direction == 'Left':
        baru = (kepala[0] - GRID, kepala[1])
    else:
        baru = (kepala[0] + GRID, kepala[1])

    if baru in snake or not (0 <= baru[0] < WIDTH and 0 <= baru[1] < HEIGHT):
        game_over()
        return

    snake.insert(0, baru)
    if baru == food:
        score += 1
        update_skor()
        letakkan_makanan()
    else:
        snake.pop()

    gambar()
    root.after(DELAY, gerak_ular)

# Gambar ulang layar
def gambar():
    canvas.delete("snake", "food")
    for x, y in snake:
        canvas.create_rectangle(x, y, x+GRID, y+GRID, fill="green", tag="snake")
    fx, fy = food
    canvas.create_oval(fx, fy, fx+GRID, fy+GRID, fill="red", tag="food")

# Letakkan makanan acak
def letakkan_makanan():
    global food
    while True:
        x = random.randint(0, (WIDTH - GRID) // GRID) * GRID
        y = random.randint(0, (HEIGHT - GRID) // GRID) * GRID
        if (x, y) not in snake:
            food = (x, y)
            break

# Update skor
def update_skor():
    skor_label.config(text=f"Skor: {score}")

# Arah manual
def ubah_arah(baru):
    global direction
    if not is_ai:
        lawan = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        if baru != lawan.get(direction):
            direction = baru

# AI atau manual toggle
def ganti_mode():
    global is_ai
    is_ai = not is_ai
    mode_btn.config(text=f"Mode: {'AI' if is_ai else 'Manual'}")

# Game over handler
def game_over():
    canvas.create_text(WIDTH/2, HEIGHT/2 - 40, text="Game Over", fill="red", font=("Helvetica", 28, "bold"))
    play_again_btn.place(relx=0.5, rely=0.5, anchor="center")

# GUI setup
root = tk.Tk()
root.title("Ular AI - Snake Game")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

frame_ui = tk.Frame(root)
frame_ui.pack(pady=5)

skor_label = tk.Label(frame_ui, text="Skor: 0", font=("Arial", 14))
skor_label.pack(side="left", padx=10)

mode_btn = tk.Button(frame_ui, text="Mode: AI", command=ganti_mode)
mode_btn.pack(side="left", padx=10)

play_again_btn = tk.Button(root, text="Main Lagi", font=("Arial", 14, "bold"),
                           bg="#00cc66", fg="white", activebackground="#00aa55", command=mulai_game)

root.bind("<Up>", lambda e: ubah_arah("Up"))
root.bind("<Down>", lambda e: ubah_arah("Down"))
root.bind("<Left>", lambda e: ubah_arah("Left"))
root.bind("<Right>", lambda e: ubah_arah("Right"))

# Mulai game
mulai_game()
root.mainloop()
