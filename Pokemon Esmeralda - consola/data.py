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



#la entrada solo recive numeros
#la entrada recibe numeros y una letra que es para salir
#la entrada recibe string(contando numeros y caracteres)

def mensaje_game(
        mensaje, 
        display="", 
        is_input=False, 
        only_numbers=False,
        back_option="",
        validacion=None, 
        mensaje_raise="",
    ):
    while True:
        #os.system('cls' if os.name == 'nt' else 'clear')
        print(display)
        try:
            if not is_input:
                print(f"{mensaje}")
                input("----------")
                return None

            else:
                entrada = input(f"{mensaje}\n🔱⚜️ ==")
                
                #validar si la entrada esta dentro de las opciones validas = CASO VERDADERO = advertisement - continue
                if only_numbers and not (entrada.isdigit() or entrada.lower() in ["", back_option]) or entrada == "":
                    raise ValueError("La entrada no es valida, ingresa una de las opciones")
                
                #validar si la entradda es la opcion de exit = return True
                elif entrada.lower() == back_option:
                    return None
 
                #alguna validacion especial, tipo la de validar que una cantidad sea coherente =  advertisement - continue 
                elif validacion and not validacion(entrada):
                    mensaje_game(mensaje_raise, display=display)
                    continue

                #si todo esto pasa, se manda la entrada y listo
                else:
                    return int(entrada) if only_numbers else entrada
            
            
        except ValueError as ve:
            mensaje_game(f"Error: {ve}", display=display)
            continue
        except KeyboardInterrupt:
            mensaje_game("Operación cancelada.", display=display)
            return None
        except Exception as e:
            mensaje_game(f"Error inesperado: {e}", display=display)
            return None
        



def mensajes_exterior(mensajes, fun=None):
    for mensaje in mensajes:
        mensaje_game(mensaje, fun)


