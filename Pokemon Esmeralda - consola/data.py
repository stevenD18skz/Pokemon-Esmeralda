import os



def procesar_numeros(*numeros, multiplicador=1, incremento=0, **kwargs):
    """
    Procesa una lista de números con un multiplicador y un incremento opcional.
    
    :param numeros: Números a procesar (argumentos posicionales).
    :param multiplicador: Factor por el cual multiplicar cada número.
    :param incremento: Cantidad a añadir a cada número después de la multiplicación.
    :param kwargs: Argumentos adicionales con nombre.
    """
    imprimir = kwargs.get('imprimir', True)  # Obtener el valor de 'imprimir', por defecto es True
    formato = kwargs.get('formato', 'algoooo')  # Obtener el valor de 'formato', por defecto es 'lista'

    print(formato)
    
    resultados = []
    for numero in numeros:
        resultado = numero * multiplicador + incremento
        resultados.append(resultado)
    
    if imprimir:
        if formato == 'lista':
            print("Resultados:", resultados)
        elif formato == 'linea':
            print("Resultados:", ', '.join(map(str, resultados)))
        else:
            print("Formato no reconocido. Resultados en lista:", resultados)
    
    # Procesar cualquier otro argumento adicional pasado como kwargs
    for key, value in kwargs.items():
        if key not in ('imprimir', 'formato'):
            print(f"Argumento adicional - {key}: {value}")

# Llamada a la función con diferentes argumentos
#procesar_numeros(1, 2, 3, 4, 5, multiplicador=2, incremento=3, imprimir=True, extra1="valor1", extra2="valor2")



class Persona:
    def getNombre(self):
        print("si soy")

class Batalla:
    def getHorario(self):
        return 10


def mensaje(template, *args):
    args = [arg() if callable(arg) else arg for arg in args]
    print("11111111111111111111111111")
    print(template % tuple(args))

# Ejemplo de uso
persona = Persona()
batalla = Batalla()

#mensaje("holaaa %s como estas en %d", persona.getNombre, batalla.getHorario)




def mensaje_game(mensaje, funcion=None, isInput=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    funcion() if funcion else None
    if not isInput:
        print(f"{mensaje}")
        input("----------")
    else:
        return input(f"{mensaje}\n🔱⚜️ ==")
    return ""

def mensajes_exterior(mensajes, fun=None):
    for mensaje in mensajes:
        mensaje_game(mensaje, fun)