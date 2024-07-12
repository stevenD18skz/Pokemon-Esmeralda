import os


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


