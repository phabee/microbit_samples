from microbit import *

# Mandelbrot-Parameter
WIDTH = 50
HEIGHT = 50
MAX_ITER = 16

# Koordinaten für das Mandelbrot-Set
X_MIN = -2.5
X_MAX = 1.0
Y_MIN = -1.25
Y_MAX = 1.25

# Cache für das berechnete Bild
mandelbrot_cache = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Viewport (5x5 Fenster auf dem Cache)
viewport_x = 20  # Startposition (ungefähr in der Mitte)
viewport_y = 15

def mandelbrot(c_real, c_imag):
    """Berechnet die Mandelbrot-Iterationen für einen Punkt"""
    z_real = 0
    z_imag = 0
    
    for i in range(MAX_ITER):
        # z = z^2 + c
        z_real_temp = z_real * z_real - z_imag * z_imag + c_real
        z_imag = 2 * z_real * z_imag + c_imag
        z_real = z_real_temp
        
        # Prüfen ob der Punkt divergiert
        if z_real * z_real + z_imag * z_imag > 4:
            return i
    
    return MAX_ITER

def calculate_mandelbrot():
    """Berechnet das gesamte Mandelbrot-Set und cached es"""
    display.scroll("CALC...")
    
    for py in range(HEIGHT):
        for px in range(WIDTH):
            # Pixel zu komplexen Koordinaten konvertieren
            c_real = X_MIN + (px / WIDTH) * (X_MAX - X_MIN)
            c_imag = Y_MIN + (py / HEIGHT) * (Y_MAX - Y_MIN)
            
            # Mandelbrot-Wert berechnen
            iterations = mandelbrot(c_real, c_imag)
            
            # In Helligkeitswert umwandeln (0-9)
            if iterations == MAX_ITER:
                brightness = 0  # Im Set = schwarz
            else:
                brightness = min(9, (iterations * 9) // MAX_ITER + 1)
            
            mandelbrot_cache[py][px] = brightness
        
        # Fortschrittsanzeige (alle 10 Zeilen)
        if py % 10 == 0:
            display.show(Image.HEART)
            sleep(50)
    
    display.show(Image.YES)
    sleep(500)
    display.clear()

def draw_viewport():
    """Zeichnet den aktuellen 5x5 Ausschnitt des Mandelbrot-Sets"""
    display.clear()
    
    for y in range(5):
        for x in range(5):
            cache_x = viewport_x + x
            cache_y = viewport_y + y
            
            # Grenzen prüfen
            if 0 <= cache_x < WIDTH and 0 <= cache_y < HEIGHT:
                brightness = mandelbrot_cache[cache_y][cache_x]
                display.set_pixel(x, y, brightness)

def move_viewport():
    """Bewegt den Viewport basierend auf Tasten und Beschleunigungssensor"""
    global viewport_x, viewport_y
    
    # Tasten für Navigation
    if button_a.was_pressed():
        # A-Taste: Nach links
        if viewport_x > 0:
            viewport_x -= 1
    
    if button_b.was_pressed():
        # B-Taste: Nach rechts
        if viewport_x < WIDTH - 5:
            viewport_x += 1
    
    # Beschleunigungssensor für Auf/Ab
    acc_y = accelerometer.get_y()
    
    if acc_y < -200:  # Nach vorne kippen = nach oben
        if viewport_y > 0:
            viewport_y -= 1
            sleep(150)
    elif acc_y > 200:  # Nach hinten kippen = nach unten
        if viewport_y < HEIGHT - 5:
            viewport_y += 1
            sleep(150)
    
    # Alternative: Logo für Reset zur Startposition
    if pin_logo.is_touched():
        viewport_x = 20
        viewport_y = 15
        display.show(Image.ARROW_N)
        sleep(300)

def show_position():
    """Zeigt die aktuelle Position im Cache"""
    display.scroll("X:" + str(viewport_x) + " Y:" + str(viewport_y), wait=False, loop=False)

# Programmstart
display.scroll("MANDELBROT")
sleep(500)

# Mandelbrot-Set berechnen (dauert ca. 20-30 Sekunden)
calculate_mandelbrot()

display.scroll("USE A/B + TILT")
sleep(1500)

# Hauptschleife - Navigation im Cache
while True:
    move_viewport()
    draw_viewport()
    
    # A+B gleichzeitig: Position anzeigen
    if button_a.is_pressed() and button_b.is_pressed():
        show_position()
        sleep(500)
    
    sleep(100)
