import tkinter as tk
import time
import random
import sys
import math

# PARAMETRY GRY
snake_window = tk.Tk()
win_x, win_y = 800, 800
snake_window.geometry(f"{win_x}x{win_y}")
snake_window.resizable(0, 0)
snake_window.title("Snake")
snake_window.protocol("WM_DELETE_WINDOW", sys.exit)
snake_canvas = tk.Canvas(snake_window, width=win_x, height=win_y, bd=0, highlightthickness=0)
snake_canvas.pack()

snake_scale = 25
game_dimensions = [win_x // snake_scale, win_y // snake_scale]

snake_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]
snake_tail = [[snake_coords[0], snake_coords[1]]]
snake_move_dir = [1, 0]
snake_moved_in_this_frame = False
initial_wps = 10  # Sta³a pocz¹tkowa prêdkoœæ gry
wps = initial_wps  # Aktualna prêdkoœæ gry
loop_id = None  # ID pêtli gry dla anulowania

game_over_flag = False
apple_count = 0
lives = 0  # Start gry bez dodatkowych ¿yæ

def createGridItem(coords, hexcolor):
    if coords:
        snake_canvas.create_rectangle(coords[0] * snake_scale, coords[1] * snake_scale, 
                                      (coords[0] + 1) * snake_scale, (coords[1] + 1) * snake_scale, 
                                      fill=hexcolor, outline="#222222", width=3)

def generateAppleCoords():
    global snake_tail
    while True:
        apple_coords = [random.randint(0, game_dimensions[0] - 1), random.randint(0, game_dimensions[1] - 1)]
        if apple_coords not in snake_tail:
            return apple_coords

def update_score():
    snake_canvas.create_text(50, 20, text=f"Score: {apple_count}  Lives: {lives}", fill="white", font=("Arial", 16), anchor="w")

def game_over():
    global game_over_flag, lives, wps, loop_id
    if lives > 0:
        lives -= 1
        wps = initial_wps  # Resetowanie prêdkoœci na wartoœæ pocz¹tkow¹
        restart_game(False)
        return
    if game_over_flag:
        return
    game_over_flag = True
    if loop_id:
        snake_window.after_cancel(loop_id)  # Zatrzymanie pêtli gry
    end_window = tk.Toplevel(snake_window)
    end_window.title("Game Over")
    end_window.geometry("300x200")
    end_canvas = tk.Canvas(end_window, width=300, height=200, bg="#222222")
    end_canvas.pack()
    
    end_canvas.create_oval(100, 50, 200, 150, fill="white", outline="black")
    end_canvas.create_oval(120, 80, 140, 100, fill="black")
    end_canvas.create_oval(160, 80, 180, 100, fill="black")
    end_canvas.create_rectangle(140, 120, 160, 130, fill="black")
    
    tk.Label(end_window, text="Game Over!", font=("Arial", 14), bg="#222222", fg="white").place(x=100, y=10)
    tk.Label(end_window, text=f"Final Score: {apple_count}", font=("Arial", 12), bg="#222222", fg="white").place(x=100, y=40)
    tk.Button(end_window, text="Play Again", command=lambda: [end_window.destroy(), restart_game(True)]).place(x=90, y=180)
    tk.Button(end_window, text="Exit", command=sys.exit).place(x=180, y=180)

def restart_game(reset_score):
    global snake_coords, snake_tail, snake_move_dir, apple_coords, game_over_flag, snake_moved_in_this_frame, apple_count, lives, wps, loop_id
    if loop_id:
        snake_window.after_cancel(loop_id)  # Zatrzymanie poprzedniej pêtli gry
    snake_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]
    snake_tail = [[snake_coords[0], snake_coords[1]]]
    snake_move_dir = [1, 0]
    apple_coords = generateAppleCoords()
    game_over_flag = False
    snake_moved_in_this_frame = False
    wps = initial_wps  # Resetowanie prêdkoœci gry
    if reset_score:
        apple_count = 0
        lives = 0  # Resetowanie liczby ¿yæ do 0
    gameloop()

def gameloop():
    global snake_moved_in_this_frame, snake_tail, snake_coords, snake_move_dir, apple_coords, apple_count, lives, wps, loop_id
    if game_over_flag:
        return
    
    loop_id = snake_window.after(1000 // wps, gameloop)  # Zapewnienie sta³ej prêdkoœci
    snake_canvas.delete("all")
    snake_canvas.create_rectangle(0, 0, win_x, win_y, fill="#222222", outline="#222222")
    
    new_head = [snake_coords[0] + snake_move_dir[0], snake_coords[1] + snake_move_dir[1]]
    if new_head in snake_tail or new_head[0] >= game_dimensions[0] or new_head[0] < 0 or \
       new_head[1] >= game_dimensions[1] or new_head[1] < 0:
        game_over()
        return
    
    snake_tail.append(new_head)
    snake_coords = new_head
    
    if new_head == apple_coords:
        apple_coords = generateAppleCoords()
        apple_count += 1
        if apple_count % 10 == 0:
            lives += 1
    else:
        if len(snake_tail) > 1:
            snake_tail.pop(0)
    
    createGridItem(apple_coords, "#ff0000")
    for segment in snake_tail:
        createGridItem(segment, "#00ff00")
    
    update_score()
    snake_moved_in_this_frame = False

def key(e):
    global snake_move_dir, snake_moved_in_this_frame
    if not snake_moved_in_this_frame:
        snake_moved_in_this_frame = True
        moves = {"Left": [-1, 0], "Right": [1, 0], "Up": [0, -1], "Down": [0, 1]}
        if e.keysym in moves and [moves[e.keysym][0] * -1, moves[e.keysym][1] * -1] != snake_move_dir:
            snake_move_dir = moves[e.keysym]

game_over_flag = False
apple_coords = generateAppleCoords()
gameloop()
snake_window.bind("<KeyPress>", key)
snake_window.mainloop()