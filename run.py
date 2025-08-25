import multiprocessing
import os
import subprocess
import time
import eel

# --- Main.py madhun import kelele functions ---
from engine.features import *
from engine.command import *
from engine.auth import recoganize
from engine.features import playAssistantSound
from engine.features import hotword

# Process 1: Ha Jarvis cha main UI aani logic sambhalto
def startJarvis():
    """Ha function Eel UI start karto aani saglya JS calls la handle karto."""
    print("Process 1 (Jarvis UI) is starting...")
    
    # Eel la sanga ki web files 'web' folder madhe ahet
    eel.init("web")

    # === Main.py madhil sarva @eel.expose functions ithe ahet ===
    @eel.expose
    def init():
        print("Frontend connected. Starting initialization sequence.")
        # Ha 'device.bat' file run karel
        subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for Face Authentication")
        
        # Face Authentication
        flag = recoganize.AuthenticateFace()

        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome Sir, How can I Help You?")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Failed")
           
    try:
        eel.start(
            'index.html',
            mode='edge',  # 'edge' kinva 'default' pan vapru shakta
            size=(1200, 700),  # Window chi size set kara
            port=8000
        )
    except (SystemExit, MemoryError, KeyboardInterrupt):
        # He errors app band zalyavar येतात, so ignore them.
        print("Jarvis UI process has been closed.")


# Process 2: Ha "Jarvis" hotword aiknyacha kaam karto
def listenHotword():
    """Ha function continuously hotword aikat rahto."""
    print("Process 2 (Hotword Detection) is starting...")
    hotword()


# === Main Program itun start hoto ===
if __name__ == '__main__':
    print("Starting Jarvis Application...")

    # Donhi process banva
    p1 = multiprocessing.Process(target=startJarvis)
    p2 = multiprocessing.Process(target=listenHotword)

    # Donhi process start kara
    p1.start()
    
    time.sleep(5)  # UI la load honyasathi thoda vel dya

    p2.start()

    # P1 (UI process) band honyachi vaat paha
    p1.join()

    # Jevha UI (P1) band hoil, tevha Hotword (P2) process la pan band kara
    if p2.is_alive():
        print("UI closed. Terminating hotword process.")
        p2.terminate()
        p2.join()
    
    print("Jarvis application has stopped.")
