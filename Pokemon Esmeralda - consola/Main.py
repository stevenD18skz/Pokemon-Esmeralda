from Algoritmo_De_Batalla import *
from Area import *
from Estrucutra import *


import os
import readchar

"""
#1.gengar
#2.rowlet
#3.bulbaur
#4.milotic
#5.garchomp
#6.sprigatito

el juego se basara en donde un entrenador llega a la liga pokemon con su pokemon inicial
el podra ir al bosque para poder capturar muchos mas pokemones o pelear contra alguos lideres de gimnasio
tambien contara con la parte de la tienda y de centro de pokemon
el objetivo principal del juego es combatir contra todos los campeones de la liga pokemon
el ganar contra los 9 al final se podra luchar contra el campeon mundial para ser el nuevo
~Bien, has escogido tu primer pokemon, ahora deberas de enfretarte los mejores entrenadores de cada region, aquello que vencioeron al alto mando correspondinete y se coronaron como los mejores de sus respectivas regiones, te enfrentaras contra los 7 campeones pokemon, pasando desde el campeon de Kanto, 
Azul hasta llegar ala Campeona de Teselia Iris, con una pequeña sospresa entre ellos, para al final llegar a la cima de todos ellos y asi enfrentarte contra Lionel, y tener la oportunidad de ser el nuevo campeon mundial.\n\nPara esta aventura tendras a tu dispocicion la tienda pokemon, donde podras comprar 
todo lo necesario para enfretarte a estos grandes adversarios, tambien podras ir a la zona del 'Bosque Verde', donde podras capturar al pokemon que desees, o combatir junto a tu equipo pokemon contra algunos miembro del alto mando para mejorar mutuamente con tus pokemons.\n\nEsa sera toda la introduccioon, 
te deseo suerte y espero te diviertas en esta pequeña eventura :3.~
....
TODO:   
- Implementar el sistema de batalla con entrenadores y pokemones salvajes.
"""






class Game:
    def __init__(self):
        # Definimos el área inicial:
        self.mapa_actual = self.load_area("bosque")
        self.matriz = [fila[:] for fila in self.mapa_actual.matriz]

        self.player_x, self.player_y = 5, 9
        self.tile_under_player = self.matriz[self.player_x][self.player_y]  # debería ser '9' o la ultima? 
        self.matriz[self.player_x][self.player_y] = 'P'
        
        # Instancias para el sistema de batalla, tienda, jugador, etc.
        self.steven = Entrenadores("Steven", 100000, 15, "entrenador pokemon", Mochila(),
                                   crear_pokemon_entrenador("Sobble"),
                                   crear_pokemon_entrenador("Ivysaur"),
                                   crear_pokemon_entrenador("Bulbasaur"),
                                   crear_pokemon_entrenador("Fennekin"),
                                   crear_pokemon_entrenador("Sobble"),
                                   crear_pokemon_entrenador("Oshawott")
                                   )
        
        self.debuggin = f""
        
    

    def load_area(self, area_name):
        # Instancias de las áreas
        self.pueblo = Pueblo()
        self.bosque = BosqueViejoPokemon()
        self.playa  = Playa()
        
        # Configuramos la relación de vecinos:
        # # Vinculamos los vecinos en “Pueblo”:
        self.pueblo.set_vecino_por_coord((5, 0),  self.bosque, coord_entrada=(5, 20))
        self.pueblo.set_vecino_por_coord((5, 20), self.playa, coord_entrada=(5, 0))

        # Vinculamos los vecinos en “Bosque”:
        self.bosque.set_vecino_por_coord((5, 20), self.pueblo, coord_entrada=(5, 0))
  
        # Vinculamos los vecinos en “Playa”:
        self.playa.set_vecino_por_coord((5, 0), self.pueblo, coord_entrada=(5, 20))

        # Devolvemos el área inicial:
        if area_name == "pueblo":
            return self.pueblo
        if area_name == "bosque":
            return self.bosque
        if area_name == "playa":
            return self.playa
        


    def cambiar_mapa(self, nueva_area, coord_entrada):
        """
        Cambia self.mapa_actual a nueva_area, y coloca al jugador en coord_entrada.
        coord_entrada es una tupla (fila, columna) donde aparecerá el jugador.
        """
        # 1. Restaurar el tile anterior: 
        #    Reemplazamos la posición donde estaba el jugador por el tile que había guardado.
        self.matriz[self.player_x][self.player_y] = self.tile_under_player

        # 2. Cambiamos el área actual y regeneramos la matriz desde la base:
        self.mapa_actual = nueva_area
        self.matriz = [fila[:] for fila in self.mapa_actual.matriz]

        # 3. Actualizar coordenadas del jugador y tile bajo él:
        self.player_x, self.player_y = coord_entrada
        self.tile_under_player = self.matriz[self.player_x][self.player_y]
        
        # 4. Colocar al jugador (tile '8') en la nueva posición de entrada:
        self.matriz[self.player_x][self.player_y] = 'P'



    def main_display(self):
        """
        Dibuja la pantalla actual basada en self.matriz.
        """
        assets = {
            '0': "🟩",  # Ground
            '1': "🌳",  # Tree (Wall)
            '2': "🌱",  # Bush (Walkable)
            '3': "🦚",  # Elder Bush
            '4': "🌼",  # Flower
            '5': "🪵",  # Log
            '6': "🌊",  # Flower
            '7': "🌴",  # Palm Tree
            '8': "🪨",  # Water
            '9': "🚪",   # Door
            'T': "🙎",   # Trainer
            "H": "🏠",  # House
            "S": "🏪",  # Store
            "F": "🏥",  # Hospital
            'P': "👤",  # Player
        }
        txt = []
        txt.append("──────────────────────────────────────────────")
        txt.append(f"👤 Jugador: {self.steven.getNombre()}   💰 Dinero: {self.steven.getDinero()}    ⏰ Hora: 12:00 PM  pos({self.player_x}, {self.player_y})")
        txt.append(f"dbg = {self.debuggin}")
        txt.append("──────────────────────────────────────────────")

        for fila in self.matriz:
            linea = "".join(assets.get(char, char) for char in fila)
            txt.append(linea)
        return "\n".join(txt)



    def mover_jugador(self, direccion):
        """
        - Se lee self.mapa_actual.matriz a través de self.matriz.
        - Si el jugador pisa '9', consultamos mapas_vecinos para cambiar de área.
        """
        direcciones = {
            "W": (-1, 0),  # Arriba
            "S": (1, 0),   # Abajo
            "A": (0, -1),  # Izquierda
            "D": (0, 1)    # Derecha
        }

        dx, dy = direcciones.get(direccion, (0,0))
        new_x = self.player_x + dx
        new_y = self.player_y + dy

        # Verificar límites:
        if not (0 <= new_x < len(self.matriz) and 0 <= new_y < len(self.matriz[0])) or self.matriz[new_x][new_y] == '1':
            return



        destino = self.matriz[new_x][new_y]

        if destino in ["H", 'S', 'F']:
            self.mapa_actual.store.recibir_jugador(self.steven)
        
        
        # 1) Restaurar tile anterior
        self.matriz[self.player_x][self.player_y] = self.tile_under_player

        # 2) Actualizar qué tile hay bajo el jugador
        self.tile_under_player = destino

        # 3) Mover el jugador
        self.player_x, self.player_y = new_x, new_y
        self.matriz[self.player_x][self.player_y] = 'P'

        # 4) Si pisa una puerta ('9'), ver si hay vecino:
        coord_actual = (self.player_x, self.player_y)
        
        if self.tile_under_player == '9':
            vecino_info = self.mapa_actual.obtener_vecino_por_coord(coord_actual)
            area_destino, coord_entrada = vecino_info
            self.cambiar_mapa(area_destino, coord_entrada)


        elif self.tile_under_player == '2': #0 255
            numero = random.randint(1, 1) 
            if not numero < self.mapa_actual.probabilidad_encuentro:
                return
    
            pokemon_salvaje = self.mapa_actual.crear_pokemon_salvaje()
            fitgh = AlgoritmoDeBatalla()
            fitgh.LUCHA_CONTRA_POKEMON(self.steven, pokemon_salvaje)
        
        elif self.tile_under_player == 'T':  # Si pisa un entrenador
            #entrenador = self.mapa_actual.obtener_entrenador_en_posicion(self.player_x, self.player_y)
            entrenador = crear_oponente("Lance")
            fitgh = AlgoritmoDeBatalla()
            fitgh.LUCHA_CONTRA_ENTRENADOR(self.steven, entrenador)
        


    def run(self):
        while True:
            eleccion = interfaz_usuario(
                f"""📋 Acciones:
                \nE. Menú          X. Salir del juego
                \nPresiona W/A/S/D para moverte, o elige una acción:""",
                display=self.main_display(),
                is_input=True,
                validacion=lambda x: x.upper() in ["W", "A", "S", "D", "E", "X"],
                mensaje_raise="Opción no válida. Intenta de nuevo."
            )

            if eleccion.upper() == "E": 
                while True:
                    eleccion_menu = interfaz_usuario(
                        f"""──────────────────────────────────────────────
                            \n📋 MENÚ:
                            \n1. POKEDEX
                            \n2. POKEMONS
                            \n3. MOCHILA
                            \n4. {self.steven.getNombre()}
                            \n5. GUARDAR
                            \n6. OPCIONES
                            \n7. VOLVER AL JUEGO
                            \n──────────────────────────────────────────────

                            \nPresiona la tecla correspondiente para seleccionar una acción.""",
                        display=self.main_display(),
                        is_input=True,
                        validacion=lambda x: x.lower() in ["1", "2", "3", "4", "5", "6", "7"],
                        mensaje_raise="Opción no válida. Intenta de nuevo."
                    )

                    if eleccion_menu == "1":
                        self.steven.pokedex.iniciar_interfaz()
                    elif eleccion_menu == "2":
                        interfaz_usuario(self.steven.imprimir_pokemons(), display=self.main_display(), is_input=False)
                        input("Presiona Enter para continuar...")
                    elif eleccion_menu == "3":
                        self.steven.usar_mochila()
                        input("Presiona Enter para continuar...")
                    elif eleccion_menu == "4":
                        interfaz_usuario(self.steven.mostrar_informacion(), display=self.main_display(), is_input=False)
                        input("Presiona Enter para continuar...")
                    elif eleccion_menu == "5":
                        print("Guardar partida: ¡Aún no disponible!")
                    elif eleccion_menu == "6":
                        print("Opciones: ¡Aún no disponible!")
                    elif eleccion_menu == "7":
                        break

            elif eleccion.upper() == "X":
                print("¡Gracias por jugar! Hasta luego.")
                break

            self.mover_jugador(eleccion)

  
        





# Para ejecutar el juego:
if __name__ == "__main__":
    game_instance = Game()
    game_instance.run()