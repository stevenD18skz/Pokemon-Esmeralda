import os


lista = [1,2,3,4]
lista.insert(0, 6)
print(lista)


if not (0):
    print("hola")    


def mensaje_game(mensaje, funcion=None, isInput=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    funcion() if funcion else 22222
    print(f"{mensaje}")
    input("-------------") if not isInput else 22222
    return ""
    #time.sleep(2)

def mensajes_exterior(mensajes):
    for mensaje in mensajes:
        mensaje_game(mensaje)
        #time.sleep(2)