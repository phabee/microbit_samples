from microbit import *
import random

# Spielfeld 5x5
board = [[0 for _ in range(5)] for _ in range(5)]

# Tetris-Formen (vereinfacht für 5x5 Display)
shapes = [
    [[1, 1], [1, 1]],  # O-Block
    [[1, 1, 1]],        # I-Block (kurz)
    [[1, 1, 0], [0, 1, 1]],  # Z-Block
    [[0, 1, 1], [1, 1, 0]],  # S-Block
    [[1, 1, 1], [0, 1, 0]],  # T-Block
    [[1, 1, 1], [1, 0, 0]],  # L-Block
]

# Aktuelle Stein-Variablen
current_shape = []
current_x = 1
current_y = 0
score = 0
game_over = False
fall_counter = 0
fall_speed = 8

def new_shape():
    global current_shape, current_x, current_y
    current_shape = [row[:] for row in random.choice(shapes)]
    current_x = 1
    current_y = 0
    
    # Prüfen ob neuer Stein platziert werden kann
    if check_collision(current_x, current_y, current_shape):
        return False
    return True

def check_collision(x, y, shape):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                new_x = x + col_idx
                new_y = y + row_idx
                
                # Grenzen prüfen
                if new_x < 0 or new_x >= 5 or new_y >= 5:
                    return True
                
                # Kollision mit existierenden Blöcken
                if new_y >= 0 and board[new_y][new_x]:
                    return True
    return False

def rotate_shape():
    global current_shape, current_x
    
    # Transponieren und Zeilen umkehren für 90° Rotation
    rotated = [[current_shape[j][i] for j in range(len(current_shape))] 
               for i in range(len(current_shape[0]) - 1, -1, -1)]
    
    # Prüfen ob Rotation möglich ist
    if not check_collision(current_x, current_y, rotated):
        current_shape = rotated
    # Wenn nicht, versuche eine Position nach links
    elif current_x > 0 and not check_collision(current_x - 1, current_y, rotated):
        current_x -= 1
        current_shape = rotated

def place_shape():
    global board, current_shape, current_x, current_y
    
    for row_idx, row in enumerate(current_shape):
        for col_idx, cell in enumerate(row):
            if cell:
                board[current_y + row_idx][current_x + col_idx] = 1

def clear_lines():
    global board, score
    lines_cleared = 0
    
    for y in range(4, -1, -1):
        if all(board[y]):
            # Zeile entfernen
            del board[y]
            # Neue leere Zeile oben einfügen
            board.insert(0, [0 for _ in range(5)])
            lines_cleared += 1
            score += 10
    
    if lines_cleared > 0:
        # Animation für gelöschte Zeilen
        for _ in range(3):
            draw_game()
            sleep(100)

def draw_game():
    display.clear()
    
    # Board zeichnen
    for y in range(5):
        for x in range(5):
            if board[y][x]:
                display.set_pixel(x, y, 6)
    
    # Aktuellen Stein zeichnen
    for row_idx, row in enumerate(current_shape):
        for col_idx, cell in enumerate(row):
            if cell:
                px = current_x + col_idx
                py = current_y + row_idx
                if 0 <= px < 5 and 0 <= py < 5:
                    display.set_pixel(px, py, 9)

def move_left():
    global current_x
    if not check_collision(current_x - 1, current_y, current_shape):
        current_x -= 1

def move_right():
    global current_x
    if not check_collision(current_x + 1, current_y, current_shape):
        current_x += 1

def move_down():
    global current_y, game_over
    
    if not check_collision(current_x, current_y + 1, current_shape):
        current_y += 1
        return True
    else:
        # Stein kann nicht weiter fallen
        place_shape()
        clear_lines()
        if not new_shape():
            game_over = True
        return False

def hard_drop():
    while move_down():
        pass

# Spielstart
display.scroll("TETRIS")
sleep(1000)
new_shape()

# Hauptspielschleife
while not game_over:
    # Steuerung
    if button_a.was_pressed():
        move_left()
    
    if button_b.was_pressed():
        move_right()
    
    if pin_logo.is_touched():
        rotate_shape()
        sleep(200)  # Entprellen
    
    # Beschleunigtes Fallen mit A+B
    if button_a.is_pressed() and button_b.is_pressed():
        hard_drop()
        sleep(200)
    
    # Automatisches Fallen
    fall_counter += 1
    if fall_counter >= fall_speed:
        fall_counter = 0
        move_down()
    
    draw_game()
    sleep(100)

# Game Over
display.scroll("GAME OVER")
display.scroll("Score: " + str(score))
sleep(2000)

# Finales Board zeigen
for y in range(5):
    for x in range(5):
        if board[y][x]:
            display.set_pixel(x, y, 9)

sleep(3000)
display.scroll("Press RESET")
