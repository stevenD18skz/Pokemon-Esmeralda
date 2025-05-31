from Algoritmo_De_Batalla import *
from Bosque import *
from Tienda import *
from data import interfaz_usuario
"""
#1.gengar
#2.rowlet
3.bulbaur
4.milotic
5.garchomp
6.sprigatito

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
COSAS POR HACER
8-hacer la parte de huir ✔
9-acomodar la parte de posiones para cuando la posion no sirva
10-acomodar la logica de las los combates ✔
11-hacer que la parte de que los pokemones ataquen sea fiel al juego
12-hacer el archivo de guardar datos del jugador
13-crear funncion de cargar partida
14-crear un minibot para el oponente
19-empezar a acomodar algoritmo de batalla para los demas tipos de lucha
20-terminar de acomodar la parte de captura para no capturar de entrenadores
"""





class Game:
    def __init__(self):
        # Instancias de las áreas
        self.pueblo = Pueblo()
        self.bosque = BosqueViejoPokemon()
        
        # Configuramos la relación de vecinos:
        # Cuando en Pueblo piso '9', voy al Bosque, en la coordenada (5,0)
        self.pueblo.set_vecino_por_coord((5, 20), bosque, coord_entrada=(2, 2))
        # Cuando en Bosque piso '9', vuelvo al Pueblo, en la coordenada (5,0)
        self.bosque.set_vecino_por_coord((5, 5), pueblo, coord_entrada=(2, 2))

        # Definimos el área inicial:
        self.mapa_actual = self.pueblo
        # Matriz de caracteres actual (lista de listas)
        self.matriz = [fila[:] for fila in self.mapa_actual.matriz]

        # Suponemos que al iniciar, el jugador está en cierta posición del Pueblo:
        # Por ejemplo, (fila 5, col 0). Colocamos el jugador en esa posición:
        self.player_x, self.player_y = 5, 10
        self.tile_under_player = self.matriz[self.player_x][self.player_y]  # debería ser '9'? 
        self.matriz[self.player_x][self.player_y] = '8'  # Marcamos la posición del jugador en el mapa
        
        # Instancias para el sistema de batalla, tienda, jugador, etc.
        self.steven = Entrenadores("Steven", 100000, 15, "entrenador pokemon", Mochila(),
                                   crear_pokemon_entrenador("Sobble"),
                                   crear_pokemon_entrenador("Ivysaur"),
                                   crear_pokemon_entrenador("Bulbasaur"),
                                   crear_pokemon_entrenador("Fennekin"),
                                   crear_pokemon_entrenador("Sobble"),
                                   crear_pokemon_entrenador("Oshawott")
                                   )
    
    def main_display(self):
        """
        Dibuja la pantalla actual basada en self.matriz.
        """
        assets = {
            "8": "👤",  # Player
            '0': "🟩",  # Ground
            '1': "🌳",  # Tree (Wall)
            '2': "🌱",  # Bush (Walkable)
            '9': "🚪"   # Door
        }
        txt = []
        txt.append("──────────────────────────────────────────────")
        player_name = self.steven.getNombre() if hasattr(self.steven, 'getNombre') else "Ash"
        player_money = self.steven.dinero if hasattr(self.steven, 'dinero') else 100000
        txt.append(f"👤 Jugador: {player_name}   💰 Dinero: {player_money}    ⏰ Hora: 12:00 PM  pos({self.player_x}, {self.player_y})")
        txt.append("──────────────────────────────────────────────")
        txt.append("")
        for fila in self.matriz:
            linea = "".join(assets.get(char, char) for char in fila)
            txt.append(linea)
        return "\n".join(txt)

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
        self.matriz[self.player_x][self.player_y] = '8'

    def mover_jugador(self, direccion):
        """
        Igual que antes, pero adaptado a la nueva estructura:
        - Se lee self.mapa_actual.matriz a través de self.matriz.
        - Si el jugador pisa '9', consultamos mapas_vecinos para cambiar de área.
        """
        direcciones = {
            "w": (-1, 0),  # Arriba
            "s": (1, 0),   # Abajo
            "a": (0, -1),  # Izquierda
            "d": (0, 1)    # Derecha
        }

        dx, dy = direcciones.get(direccion, (0,0))
        new_x = self.player_x + dx
        new_y = self.player_y + dy

        # Verificar límites:
        if 0 <= new_x < len(self.matriz) and 0 <= new_y < len(self.matriz[0]):
            destino = self.matriz[new_x][new_y]

            # Si no es muro ('1'), permitimos el movimiento:
            if destino != '1':
                # 1) Restaurar tile anterior
                self.matriz[self.player_x][self.player_y] = self.tile_under_player

                # 2) Actualizar qué tile hay bajo el jugador
                self.tile_under_player = destino

                # 3) Mover el jugador
                self.player_x, self.player_y = new_x, new_y
                self.matriz[self.player_x][self.player_y] = '8'

                # 4) Si pisa una puerta ('9'), ver si hay vecino:
                coord_actual = (self.player_x, self.player_y)
                if self.tile_under_player == '9':
                    vecino_info = self.mapa_actual.obtener_vecino_por_coord(coord_actual)
                    if vecino_info is not None:
                        area_destino, coord_entrada = vecino_info
                        print(f"Cruzas la puerta hacia {area_destino.nombre}…")
                        self.cambiar_mapa(area_destino, coord_entrada)
                    else:
                        print("¡No hay salida configurada en esta puerta!")

                else:
                    # Opcional: Si pisa hierba ('2'), generar encuentro:
                    if self.tile_under_player == '2':
                        print("Lees el follaje y… ¡elige un combate con un Pokémon salvaje!")
                        # Aquí podrías llamar a iniciar_combate_pokemon, etc.
            # Si hay muro, no hacer nada (o reproducir un sonido “bump”)
        # Si está fuera de la matriz, tampoco hacemos nada.

    def run(self):
        input("Bienvenido al juego, presiona Enter para comenzar...")
        while True:
            eleccion = interfaz_usuario(
                f"""──────────────────────────────────────────────
📋 Acciones:
1. Ir al bosque   2. Luchar contra un entrenador   3. Ir a la tienda
E. Menú          X. Salir del juego
──────────────────────────────────────────────

Presiona W/A/S/D para moverte, o elige una acción:""",
                display=self.main_display(),
                is_input=True,
                validacion=lambda x: x.lower() in ["w", "a", "s", "d", "1", "2", "3", "e", "x"],
                mensaje_raise="Opción no válida. Intenta de nuevo."
            )

            tecla = eleccion.lower()
            if tecla in ["w", "a", "s", "d"]:
                self.mover_jugador(tecla)

            elif eleccion == "1":
                # Ya no necesitamos llamar explícitamente a BosqueViejoPokemon,
                # sino que el jugador usará las puertas para desplazarse entre áreas.
                print("Para ir al bosque, ¡acércate a la puerta y pisa '9'!")
                # (Opcional: podrías teletransportar al jugador aquí directamente:
                #  self.cambiar_mapa(self.bosque, (5,0)))
            
            elif eleccion == "2":
                Lance = crear_oponente("Lance")
                combate = AlgoritmoDeBatalla()
                combate.LUCHA_CONTRA_ENTRENADOR(self.steven, Lance)

            elif eleccion == "3":
                tienda = Tienda()
                tienda.recibir_jugador(self.steven)

            elif eleccion.upper() == "E":
                # Menú interno, igual que antes, pero usando self.main_display()
                while True:
                    eleccion_menu = interfaz_usuario(
                        f"""──────────────────────────────────────────────
📋 MENÚ:
1. POKEDEX
2. POKEMONS
3. MOCHILA
4. {self.steven.getNombre()}
5. GUARDAR
6. OPCIONES
7. VOLVER AL JUEGO
──────────────────────────────────────────────

Presiona la tecla correspondiente para seleccionar una acción.""",
                        display=self.main_display(),
                        is_input=True,
                        validacion=lambda x: x.lower() in ["1", "2", "3", "4", "5", "6", "7"],
                        mensaje_raise="Opción no válida. Intenta de nuevo."
                    )

                    if eleccion_menu == "1":
                        print("Pokedex: ¡Aún no disponible!")
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





# Para ejecutar el juego:
if __name__ == "__main__":
    # Ensure all imported/dependent classes and functions are defined above or in imported files
    # For example: AlgoritmoDeBatalla, Bosque, Tienda, data.interfaz_usuario



    # En algún punto de inicialización global, o dentro de Game.__init__:
    pueblo = Pueblo()
    bosque = BosqueViejoPokemon()

    # Por ejemplo, en el Pueblo hay puertas que llevan al Bosque:
    #  - Supongamos que en el Pueblo, el tile '9' de la fila 5 (índice 5) y columna 0 
    #    es la puerta de entrada al Bosque. Cuando se pise esa posición, queremos:
    #    - Cambiar a 'bosque'
    #    - Aparecer en el Bosque en la coordenada (fila 5, columna 0) (u otra que elijas).
    pueblo.set_vecino_por_coord((9, 0), bosque, coord_entrada=(2, 2))

    # Y recíprocamente, en el Bosque hay una puerta que lleva de vuelta al Pueblo:
    bosque.set_vecino_por_coord((5, 5), pueblo, coord_entrada=(2, 2))

    # Instancias
    pueblo_costa    = PuebloCosta()
    cueva_marina    = CuevaMarina()
    barco_pesquero  = BarcoPesquero()
    playa           = Playa()

    # Vinculamos los vecinos en “Playa”:
    # – Si el jugador pisa (2, 20) en la Playa, entra a PuebloCosta en (fila 1, col 1).
    playa.set_vecino_por_coord((2, 20), pueblo_costa, coord_entrada=(1, 1))
    # – Si pisa (5, 0), va a CuevaMarina y entra en (2, 2).
    playa.set_vecino_por_coord((5, 0), cueva_marina, coord_entrada=(2, 2))
    # – Si pisa (5, 20), va a BarcoPesquero y entra en (2, 4).
    playa.set_vecino_por_coord((5, 20), barco_pesquero, coord_entrada=(2, 4))

    # También conviene configurar la salida recíproca en cada uno de estos mapas:
    # (las coordenadas de “entrada” pueden ser diferentes en cada uno)
    pueblo_costa.set_vecino_por_coord((1, 18), playa, coord_entrada=(2, 20))
    cueva_marina.set_vecino_por_coord((2, 3),   playa, coord_entrada=(5, 0))
    barco_pesquero.set_vecino_por_coord((2, 4), playa, coord_entrada=(5, 20))



    game_instance = Game()
    game_instance.run()