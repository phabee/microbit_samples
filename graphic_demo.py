from microbit import *
import random
import music
from math import sin

# Willkommen
display.scroll("DEMO")

def plasma_effekt():
    """Plasmaartige Animation mit Sinuswellen"""
    for frame in range(200):
        for y in range(5):
            for x in range(5):
                # Berechne Helligkeit basierend auf Position und Zeit
                val = int((sin((x + frame/10) * 0.5) + sin((y + frame/8) * 0.7) + 2) * 4)
                val = max(0, min(9, val))
                display.set_pixel(x, y, val)
        sleep(20)

def matrix_regen():
    """Matrix-Style fallende Zeichen"""
    spalten = [[random.randint(0, 9) for _ in range(5)] for _ in range(5)]
    geschwindigkeit = [random.randint(1, 3) for _ in range(5)]
    
    for frame in range(150):
        for x in range(5):
            if frame % geschwindigkeit[x] == 0:
                # Bewege Spalte nach unten
                spalten[x] = [random.randint(0, 9)] + spalten[x][:-1]
            
            for y in range(5):
                # Helligkeit nimmt nach unten ab
                helligkeit = spalten[x][y] - y * 2
                helligkeit = max(0, min(9, helligkeit))
                display.set_pixel(x, y, helligkeit)
        
        if frame % 20 == 0:
            music.pitch(random.randint(400, 800), 50, wait=False)
        sleep(50)

def feuer_simulation():
    """Realistische Feuer-Animation"""
    feuer = [[0 for _ in range(5)] for _ in range(6)]
    
    for frame in range(200):
        # Neue Flammen am Boden
        for x in range(5):
            feuer[5][x] = random.randint(7, 9)
        
        # Feuer steigt auf und verblasst
        for y in range(5):
            for x in range(5):
                # Nimm Durchschnitt von unten
                nachbarn = []
                if y < 5:
                    nachbarn.append(feuer[y+1][x])
                if x > 0 and y < 5:
                    nachbarn.append(feuer[y+1][x-1])
                if x < 4 and y < 5:
                    nachbarn.append(feuer[y+1][x+1])
                
                if nachbarn:
                    feuer[y][x] = max(0, sum(nachbarn)//len(nachbarn) - random.randint(0, 2))
                
                display.set_pixel(x, y, feuer[y][x])
        
        if frame % 30 == 0:
            music.pitch(random.randint(100, 200), 30, wait=False)
        sleep(30)

def tunnel_effekt():
    """3D Tunnel-Effekt"""
    for frame in range(150):
        for y in range(5):
            for x in range(5):
                # Distanz vom Zentrum
                dx = x - 2
                dy = y - 2
                distanz = (dx*dx + dy*dy) ** 0.5
                
                # Winkel
                winkel = 0
                if dx != 0 or dy != 0:
                    import math
                    winkel = math.atan2(dy, dx)
                
                # Animierte Tunnel-Helligkeit
                val = int((sin(distanz - frame/10) + sin(winkel * 3 + frame/15)) * 4 + 5)
                val = max(0, min(9, val))
                display.set_pixel(x, y, val)
        
        sleep(30)

def starfield():
    """3D Sternfeld-Effekt"""
    sterne = []
    # Initialisiere Sterne
    for _ in range(15):
        sterne.append({
            'x': random.randint(-50, 50),
            'y': random.randint(-50, 50),
            'z': random.randint(1, 100)
        })
    
    for frame in range(200):
        display.clear()
        
        for stern in sterne:
            # Bewege Stern nach vorne
            stern['z'] -= 2
            
            # Wenn zu nah, respawn hinten
            if stern['z'] <= 1:
                stern['x'] = random.randint(-50, 50)
                stern['y'] = random.randint(-50, 50)
                stern['z'] = 100
            
            # 3D Projektion
            sx = int(stern['x'] * 10 / stern['z']) + 2
            sy = int(stern['y'] * 10 / stern['z']) + 2
            
            # Helligkeit basierend auf Distanz
            helligkeit = max(0, 9 - stern['z']//10)
            
            if 0 <= sx < 5 and 0 <= sy < 5:
                display.set_pixel(sx, sy, helligkeit)
        
        if frame % 15 == 0:
            music.pitch(200 + frame * 5, 20, wait=False)
        sleep(40)

def wellen_interferenz():
    """Zwei interferierende Wellen"""
    for frame in range(150):
        for y in range(5):
            for x in range(5):
                # Zwei Wellenzentren
                d1 = ((x-1)**2 + (y-1)**2)**0.5
                d2 = ((x-3)**2 + (y-3)**2)**0.5
                
                welle1 = sin(d1 - frame/8)
                welle2 = sin(d2 - frame/8)
                
                val = int((welle1 + welle2 + 2) * 2.5)
                val = max(0, min(9, val))
                display.set_pixel(x, y, val)
        sleep(30)

def game_of_life():
    """Conway's Game of Life"""
    # Zufällige Startposition
    welt = [[random.randint(0, 1) * 9 for _ in range(5)] for _ in range(5)]
    
    for generation in range(100):
        # Zeige aktuelle Generation
        for y in range(5):
            for x in range(5):
                display.set_pixel(x, y, welt[y][x])
        
        sleep(200)
        
        # Berechne nächste Generation
        neue_welt = [[0 for _ in range(5)] for _ in range(5)]
        
        for y in range(5):
            for x in range(5):
                # Zähle Nachbarn
                nachbarn = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = (x + dx) % 5, (y + dy) % 5
                        if welt[ny][nx] > 0:
                            nachbarn += 1
                
                # Game of Life Regeln
                if welt[y][x] > 0:  # Lebendig
                    if nachbarn in [2, 3]:
                        neue_welt[y][x] = 9
                else:  # Tot
                    if nachbarn == 3:
                        neue_welt[y][x] = 9
        
        welt = neue_welt
        
        # Sound-Effekt basierend auf Population
        population = sum(sum(1 for pixel in zeile if pixel > 0) for zeile in welt)
        if population > 0:
            music.pitch(300 + population * 50, 50, wait=False)

def spirale():
    """Rotierende Spirale"""
    for frame in range(150):
        for y in range(5):
            for x in range(5):
                dx = x - 2
                dy = y - 2
                
                import math
                winkel = math.atan2(dy, dx) if (dx != 0 or dy != 0) else 0
                distanz = (dx*dx + dy*dy)**0.5
                
                val = int((sin(winkel * 2 - frame/10 + distanz) + 1) * 4.5)
                val = max(0, min(9, val))
                display.set_pixel(x, y, val)
        sleep(30)

# Hauptmenü mit allen Demos
demos = [
    ("PLASMA", plasma_effekt),
    ("MATRIX", matrix_regen),
    ("FEUER", feuer_simulation),
    ("TUNNEL", tunnel_effekt),
    ("STERNE", starfield),
    ("WELLEN", wellen_interferenz),
    ("LIFE", game_of_life),
    ("SPIRAL", spirale)
]

demo_index = 0

# Zeige aktuelle Demo
display.scroll(demos[demo_index][0])
sleep(500)

while True:
    # Führe Demo aus
    demos[demo_index][1]()
    
    # Nächste Demo oder Steuerung
    if button_a.was_pressed():
        # Vorherige Demo
        demo_index = (demo_index - 1) % len(demos)
        display.scroll(demos[demo_index][0])
    elif button_b.was_pressed():
        # Nächste Demo
        demo_index = (demo_index + 1) % len(demos)
        display.scroll(demos[demo_index][0])
    else:
        # Auto-weiter zur nächsten Demo
        demo_index = (demo_index + 1) % len(demos)
        display.scroll(demos[demo_index][0])
        sleep(500)
