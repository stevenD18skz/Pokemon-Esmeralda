import os

def mensaje_game(mensaje, funcion=None, isInput=False):
    os.system('cls' if os.name == 'nt' else 'clear')

    funcion() if funcion else None

    if not isInput:
        print(f"{mensaje}")
    else:
        print(f"{mensaje}\n🔱⚜️ ==", end="")
    return ""
    #time.sleep(2)

def mensajes_exterior(mensajes):
    for mensaje in mensajes:
        mensaje_game(mensaje)
        #time.sleep(2)