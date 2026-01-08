from microbit import *
import random
import music

display.scroll("DUELL!")
sleep(500)

# Highscore
highscore = 0
spieler_name = "???"

def zeige_countdown():
    """Zeigt einen visuellen 3-2-1 Countdown"""
    for i in range(3, 0, -1):
        display.show(str(i))
        music.pitch(400 + i*100, 200)
        sleep(1000)
    display.clear()

def zeige_blitz():
    """Zeigt einen coolen Blitz-Effekt"""
    blitz = Image("90009:09090:00900:09090:90009")
    display.show(blitz)
    music.pitch(1000, 100)

def feiere_sieg(reaktionszeit):
    """Feier-Animation mit Musik"""
    if reaktionszeit < 300:
        # Mega schnell!
        display.show(Image.SURPRISED)
        music.play(music.POWER_UP)
    elif reaktionszeit < 500:
        # Sehr gut
        display.show(Image.HAPPY)
        music.play(music.BA_DING)
    else:
        # Ok
        display.show(Image.SMILE)
        music.pitch(500, 300)

def spiele_runde():
    """Eine einzelne Spielrunde"""
    global highscore, spieler_name
    
    display.scroll("BEREIT?")
    sleep(500)
    
    # Countdown
    zeige_countdown()
    
    # Zufällige Wartezeit (1-5 Sekunden)
    wartezeit = random.randint(1000, 5000)
    sleep(wartezeit)
    
    # JETZT!
    zeige_blitz()
    startzeit = running_time()
    
    # Warte auf Button-Press
    while True:
        if button_a.was_pressed() or button_b.was_pressed():
            reaktionszeit = running_time() - startzeit
            break
        
        # Timeout nach 5 Sekunden
        if running_time() - startzeit > 5000:
            display.scroll("ZU LANGSAM!")
            music.play(music.WAWAWAWAA)
            return None
    
    # Zeige Reaktionszeit
    display.scroll(str(reaktionszeit) + "ms")
    feiere_sieg(reaktionszeit)
    sleep(1000)
    
    # Neuer Highscore?
    if reaktionszeit < highscore or highscore == 0:
        highscore = reaktionszeit
        display.scroll("RECORD!")
        music.play(music.POWER_UP)
        
        # Feuerwerk-Animation
        for _ in range(5):
            display.show(Image.ALL_CLOCKS, delay=100)
    
    return reaktionszeit

def multiplayer_duell():
    """Zwei-Spieler Duell-Modus"""
    display.scroll("DUELL!")
    sleep(500)
    
    display.scroll("A vs B")
    sleep(1000)
    
    zeige_countdown()
    
    # Zufällige Wartezeit
    wartezeit = random.randint(2000, 6000)
    sleep(wartezeit)
    
    # JETZT!
    zeige_blitz()
    startzeit = running_time()
    
    # Wer drückt zuerst?
    while True:
        if button_a.was_pressed():
            reaktionszeit = running_time() - startzeit
            display.scroll("A GEWINNT!")
            display.scroll(str(reaktionszeit) + "ms")
            music.play(music.POWER_UP)
            return
        
        if button_b.was_pressed():
            reaktionszeit = running_time() - startzeit
            display.scroll("B GEWINNT!")
            display.scroll(str(reaktionszeit) + "ms")
            music.play(music.POWER_UP)
            return
        
        if running_time() - startzeit > 5000:
            display.scroll("UNENTSCHIEDEN")
            return

def zeige_stats():
    """Zeigt Statistiken und Highscore"""
    display.scroll("RECORD:")
    if highscore > 0:
        display.scroll(str(highscore) + "ms")
    else:
        display.scroll("---")
    sleep(1000)

# Hauptmenü
while True:
    # Zeige Menü-Optionen
    display.show(Image.ARROW_W)  # A für Solo
    
    if button_a.was_pressed():
        # Solo-Modus
        spiele_runde()
    
    elif button_b.was_pressed():
        # Multiplayer-Modus
        multiplayer_duell()
    
    elif accelerometer.was_gesture("shake"):
        # Shake für Stats
        zeige_stats()
    
    sleep(100)
