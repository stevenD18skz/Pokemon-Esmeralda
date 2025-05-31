import os
import readchar



#la entrada solo recive numeros
#la entrada recibe numeros y una letra que es para salir
#la entrada recibe string(contando numeros y caracteres)

def interfaz_usuario(
        *mensaje,
        display="",
        is_input=False, 
        validacion=None, 
        mensaje_raise="",
    ):
    """
    Maneja la interacción con el usuario, mostrando mensajes y validando entradas.

    Parámetros:
    -----------
    mensaje : str
        El mensaje principal que se mostrará al usuario.
    
    display : str, opcional
        Texto adicional que se muestra en pantalla antes del mensaje principal. 
        Puede ser utilizado para mostrar el estado actual del juego o información adicional.
    
    is_input : bool, opcional
        Indica si se espera una entrada del usuario. Si es False, la función solo muestra el mensaje 
        y espera una confirmación del usuario para continuar. Si es True, la función solicita una 
        entrada del usuario.
    
    validacion : function, opcional
        Una función que toma la entrada del usuario como argumento y devuelve True si la entrada es válida, 
        o False si no lo es. Si no se proporciona, cualquier entrada será considerada válida.
    
    mensaje_raise : str, opcional
        El mensaje que se mostrará si la validación de la entrada falla. Se utiliza para informar al 
        usuario sobre qué salió mal y solicitar una nueva entrada.
    
    Retorna:
    --------
    str o None
        Si is_input es True y la entrada es válida, retorna la entrada del usuario como cadena. 
        Si is_input es False, retorna None después de que el usuario confirme el mensaje.
    
    Manejo de Excepciones:
    ----------------------
    ValueError:
        Si ocurre un ValueError durante la ejecución, se muestra un mensaje de error y se solicita una nueva entrada.
    
    KeyboardInterrupt:
        Si el usuario interrumpe la ejecución con un comando especial (por ejemplo, Ctrl+C), se muestra un mensaje 
        de cancelación y se solicita una nueva entrada.
    
    Exception:
        Cualquier otra excepción se captura y se muestra un mensaje de error inesperado, retornando None.
    
    Ejemplos de Uso:
    ----------------
    1. Mostrar un mensaje sin esperar entrada:
        mensaje_game(mensaje="¡Bienvenido al juego!")
    
    2. Solicitar una entrada válida del usuario:
        entrada = mensaje_game(
            mensaje="Ingresa un número positivo:", 
            is_input=True, 
            validacion=lambda x: x.isdigit() and int(x) > 0, 
            mensaje_raise="Por favor, ingresa un número entero positivo."
        )
        if entrada:
            print(f"Entrada válida: {entrada}")
    """
    
    def funcion_interna(m):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(display)
            try:
                if not is_input:
                    print(f"{m}")
                    input("----------")
                    return None
    
                else:
                    print(f"{m}\n🔱⚜️ ==", end="")
                    entrada = readchar.readkey()
                    
                    if validacion and not validacion(entrada):
                        interfaz_usuario(mensaje_raise, display=display)
                        continue
                    
                    else:
                        return entrada
                
                
            except ValueError as ve:
                interfaz_usuario(f"Error: {ve}", display=display)
                continue
            except KeyboardInterrupt:
                interfaz_usuario("Operación cancelada, no ingreses comandos especiales", display=display)
                continue
            except Exception as e:
                interfaz_usuario(f"Error inesperado: {e}", display=display)
                return None
            

    e = None
    for m in mensaje:
        e = funcion_interna(m)
        
    return e
        
    


