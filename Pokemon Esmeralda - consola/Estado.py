import sqlite3
import random
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#OPCION 3


conexion = sqlite3.connect('data_base/pokemonRojoFuego.db')
cursor = conexion.cursor()

"""
tipos de estados
===>inmovilizacion:
-Paralizado - ✔✔✔
-Somnoliento - ✔✔✔
-Congelado - ✔✔✔
-enamorado - ✔✔✔
-Amedrentado - ✔✔✔


===>daño:
-Quemado - ✔✔✔
-Envenenado - ✔✔✔
-Gravemente Envenenado - ✔✔✔
-Helado - ✔✔✔
-Drenadoras - ✔✔✔


===>especiales:
-Confuso - 
-Atrapado - XX
-NORMAL - ✔✔✔
-DEBILITADO - ✔✔✔
-CENTRO DE ATENCION - 
"""


class Estado:
    def __init__(self, nombre, tipo, dañoAplicado, pctjeInmovilizacion, BonoEnCaptura, reduccionEstadistica):#✔✔✔
        self.nombre = nombre
        self.tipo = tipo
        self.dañoAplicado = dañoAplicado
        self.pctjeInmovilizacion = pctjeInmovilizacion
        self.BonoEnCaptura = BonoEnCaptura
        self.reduccionEstadistica = reduccionEstadistica.split(',')



    def mostrar_informacion(self):#✔✔✔
        # Imprimimos el menú con los datos del estado Normal
        print(f"◤────────────────────────────────────◥")
        print(f"🌀El estado {self.nombre} tiene las características:🌀")
        print("┌────────────────────────────────────┐")
        print(f"│   Tipo: {self.tipo}  |")
        print(f"│   Daño: {str(self.dañoAplicado)}  |")
        print(f"│   Probabilidad de moverse: {str(self.pctjeInmovilizacion)}  |")
        print(f"│   Bono en captura: {str(self.BonoEnCaptura)}  |")
        print(f"│   Reducción estadística: {", ".join(self.reduccionEstadistica)}  |")
        print("└────────────────────────────────────┘")
        print(f"◣────────────────────────────────────◢")



    def aplicar_segundo_efecto(self, pokemonAfectado):#✔✔✔
            mensajes = []
            if self.reduccionEstadistica[0] == "0":
                return mensajes

            # Obtén las funciones set y get correspondientes a la estadística que se va a reducir
            funcion_set = getattr(pokemonAfectado, 'set' + self.reduccionEstadistica[0][1:-1])
            funcion_get = getattr(pokemonAfectado, 'get' + self.reduccionEstadistica[0][1:-1])

            # Calcula la reducción
            reduccion = int(funcion_get() * int(self.reduccionEstadistica[1]) / 100)

            # Aplica la reducción
            funcion_set(reduccion)

            mensajes.append(f"🦽🦽🦽 A {pokemonAfectado.getNombre()} se le ha reducido en un {int(self.reduccionEstadistica[1])}% la estadística de {self.reduccionEstadistica[0]}, esta queda en {reduccion} 🦽🦽🦽")
            return mensajes



    def realizarDaño(self, pokemon_afectado, pokemon_contrario):#✔✔✔
        mensajes = []
        if pokemon_afectado.getEstado().getDañoAplicadoDeEstado() != 0:
            daño = int((pokemon_afectado.getMps() * pokemon_afectado.getEstado().getDañoAplicadoDeEstado()) / 100)
            pokemon_afectado.setPs(pokemon_afectado.getPs() - daño)
            mensajes.append(f"🧵🧵🧵La vida de {pokemon_afectado.getNombre()} ha bajado {daño} ps debido a {pokemon_afectado.getEstado().getNombre()}🧵🧵🧵")
            mensajes.append(f"\n💔💔💔La vida de {pokemon_afectado.getNombre()} ha quedado en {pokemon_afectado.getPs()}💔💔💔")
            
            
            self.dañoAplicado += 6.25 if self.nombre == "Gravemente envenenado⚛️" and daño < 100 else 0
            
            if self.nombre == "Drenadoras🫧":
                pokemon_contrario.setPs(pokemon_contrario.getPs() + daño)
                mensajes.append(f"⚕⚕⚕ {pokemon_contrario.getNombre()} ah recuperado un total de {daño} puntos de ps debido a Drenadoras🫧 ⚕⚕⚕")

        return mensajes



    def reset_estado(pokemon_afectado):#✔✔✔
        consulta_estado = """
        SELECT *
        FROM estado
        WHERE id_estado = 1
        """
        cursor.execute(consulta_estado)
        estado_consultado = cursor.fetchall()[0][1:]
        pokemon_afectado.setEstado(Estado(*estado_consultado))
    def ver_si_se_puede_mover(self, pokemon_afectado):#✔✔✔
        mensajes = []
        if random.randint(1,100) < (pokemon_afectado.getEstado().getPctjeInmovilizacion()):
            mensajes.append(f"\n\n      🧶🧶🧶Es el momento de atacar de {pokemon_afectado.getNombre()} 🧶🧶🧶")
            mensajes.append(f"\n🧊🧊🧊 {pokemon_afectado.getNombre()} no se puede mover debido a {pokemon_afectado.getEstado().getNombre()} 🧊🧊🧊")
            return True, mensajes

        if self.nombre == "Amedrentado💥":
            mensajes.append(f"💥💥💥{pokemon_afectado.getNombre()} no ah podido atacar debido a Amedrentado💥💥💥")
            self.reset_estado(pokemon_afectado)
            return True, mensajes    
        
        if self.nombre == "Congelado🧊" and random.randint(1,100) < 20:
            mensajes.append(f"🧊🧊🧊{pokemon_afectado.getNombre()} ya no se encuentra congelado 🧊🧊🧊")
            self.reset_estado(pokemon_afectado)
            return False, mensajes  

        return False, mensajes 




    def getNombre(self):
        return self.nombre

    def getTipo(self):
        return self.tipo

    def getDañoAplicadoDeEstado(self):
        return self.dañoAplicado

    def getPctjeInmovilizacion(self):
        return self.pctjeInmovilizacion

    def getBonoEnCaptura(self):
        return self.BonoEnCaptura

    def getreduccionEstadistica(self):
        return self.reduccionEstadistica