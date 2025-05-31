from Pokemon import *
from Algoritmo_De_Batalla import *
import random




class Area:
    def __init__(self, nombre, char_map):
        self.nombre = nombre
        self.char_map = char_map.strip()
        self.matriz = self.generar_matriz()
        # Ahora la clave será una tupla (fila, columna)
        self.mapas_vecinos = {}

    def generar_matriz(self):
        return [list(fila) for fila in self.char_map.split('\n')]

    def set_vecino_por_coord(self, coord_puerta, area_destino, coord_entrada):
        """
        coord_puerta: tupla (fila, columna) indicando dónde está la puerta en este mapa.
        area_destino: la instancia de Area (o subclase) a la que se quiere ir.
        coord_entrada: tupla (fila_entrada, col_entrada) indicando dónde debe aparecer el jugador en la nueva área.
        """
        self.mapas_vecinos[coord_puerta] = (area_destino, coord_entrada)

    def obtener_vecino_por_coord(self, coord):
        """
        Si coord (fila, columna) es una puerta configurada, devuelve (area_destino, coord_entrada).
        Si no, devuelve None.
        """
        return self.mapas_vecinos.get(coord, None)



class PuebloCosta(Area):
    def __init__(self):
        char_map = """
11111111111111111111
1000000000000000901
10000000000000000001
10000000000000000001
11111111111111111111
"""
        super().__init__(nombre="Pueblo Costa", char_map=char_map)

class CuevaMarina(Area):
    def __init__(self):
        char_map = """
1111111
1000001
1090001
1000001
1111111
"""
        super().__init__(nombre="Cueva Marina", char_map=char_map)

class BarcoPesquero(Area):
    def __init__(self):
        char_map = """
111111111
100000001
100090001
100000001
111111111
"""
        super().__init__(nombre="Barco Pesquero", char_map=char_map)

class Playa(Area):
    def __init__(self):
        char_map = """
111111111111111111111
100000000000000000001
100000000020000000021
100000000000000000001
100000000000000000001
900000000000000000009
100000000000000000001
100000000000000000001
100000000000000000001
100000000000000000001
111111111111111111111
"""
        super().__init__(nombre="Playa", char_map=char_map)

        # Aquí van las tres puertas (en este ejemplo, las casillas con '9'):
        # - puerta arriba (fila 2, col 20) → PuebloCosta, 
        # - puerta izquierda (fila 5, col 0) → CuevaMarina, 
        # - puerta derecha (fila 5, col 20) → BarcoPesquero

        # COORDENADAS basadas en el char_map anterior (cuenta líneas y columnas empezando en 0):
        # - Puerta 1: en la fila 2, columna 20 (el último '1' de la línea “10000000002........21”)
        # - Puerta 2: en la fila 5, columna 0   (es ese '9' del char_map)
        # - Puerta 3: en la fila 5, columna 20  (el último '9' de la línea “900000000000000000009”)

        # NOTA: ajusta las coordenadas si cambias el char_map. Este es un ejemplo ilustrativo.




class Pueblo(Area):
    def __init__(self):
        char_map = """
111111111911111111111
100000000000000000001
100000000000000000001
100000000000000000001
100000000000000000001
900000000000000000009
100000000000000000001
100000000000000000001
100000000000000000001
100000000000000000001
111111111111111111111
"""
        super().__init__(nombre="Pueblo", char_map=char_map)
        # Aquí podrías inicializar atributos específicos (p. ej., NPCs, tiendas, etc.)





class BosqueViejoPokemon(Area):
    def __init__(self):
        """
        Inicializa la clase BosqueViejoPokemon obteniendo las probabilidades de aparición de los Pokémon
        en el Bosque Verde desde la base de datos.
        """
        self.nombre = "Bosque Verde"

        char_map = """
111111111111111111111
100000000000000000001
100000000000000000001
100000000000000000001
100000000000000000001
100000000000000000009
102000000000000000001
122202000000000000001
122222020000000000001
122222222000000000001
111111111111111111111
"""


        super().__init__(nombre="Bosque Verde", char_map=char_map)
        consulta_posibilidades = """
        SELECT p.nombre, b.porcentaje_aparicion 
        FROM bosqueverde b 
        JOIN pokemon p ON b.id_pokemon = p.id_pokemon
        """
        try:
            self.probabilidades = {nombre: porcentaje for nombre, porcentaje in cursor.execute(consulta_posibilidades).fetchall()}
        except sqlite3.Error as e:
            print(f"Error al obtener las probabilidades de aparición: {e}")
            self.probabilidades = {}



    def calcular_pokemon_a_salir(self, opciones):
        """
        Calcula el Pokémon que aparecerá basado en las probabilidades de aparición.

        :param opciones: Un diccionario con los nombres de los Pokémon y sus probabilidades de aparición.
        :return: El nombre del Pokémon que aparece.
        """
        return "Bulbasaur"
        total_probabilidad = sum(opciones.values())
        probabilidad_acumulada = 0
        num_aleatorio = random.uniform(0, 1)

        for opcion, probabilidad in opciones.items():
            probabilidad_acumulada += probabilidad / total_probabilidad
            if num_aleatorio <= probabilidad_acumulada:
                return opcion



    def calcular_movimientos_pokemon(self, id_pokemon, nivel):
        """
        Calcula los movimientos que puede aprender un Pokémon basado en su nivel.

        :param id_pokemon: El ID del Pokémon.
        :param nivel: El nivel del Pokémon.
        :return: Una lista de objetos Movimiento que el Pokémon puede usar.
        """
        consulta_movimientos = f"""
        SELECT id_movimiento
        FROM pokemon_movimiento
        WHERE nivel <= {nivel} AND id_pokemon = {id_pokemon}
        """
        try:
            cursor.execute(consulta_movimientos)
            posibles_movimientos = [t[0] for t in cursor.fetchall()]
            cantidad = 4 if len(posibles_movimientos) > 4 else len(posibles_movimientos)
            id_movimientos = random.sample(posibles_movimientos, cantidad)
            id_movimientos += [1] * (4 - len(id_movimientos)) if len(id_movimientos) < 4 else []
            movimientos_creados = []

            for id_mov in id_movimientos:
                consulta_movimiento = f"SELECT * FROM movimiento WHERE id_movimiento = {id_mov}"
                cursor.execute(consulta_movimiento)
                datos_movimiento = cursor.fetchone()
                
                consulta_ef_secundario = f"SELECT * FROM estado WHERE id_estado = {datos_movimiento[-1]}"
                cursor.execute(consulta_ef_secundario)
                datos_ef_secundario = cursor.fetchone()
                
                movimiento = Movimiento(*datos_movimiento[1:-1], Estado(*datos_ef_secundario[1:]))
                movimientos_creados.append(movimiento)

            return movimientos_creados
        except sqlite3.Error as e:
            print(f"Error al calcular movimientos: {e}")
            return []



    def crear_pokemon_salvaje(self):
        """
        Crea un Pokémon salvaje con nivel y movimientos aleatorios dentro del rango permitido.

        :return: Un objeto Pokémon con los datos generados.
        """
        nombre_elegido = self.calcular_pokemon_a_salir(self.probabilidades)
        consulta_datos_pokemon = f"""
        SELECT p.*, b.nivel_min, b.nivel_max 
        FROM bosqueverde b 
        JOIN pokemon p ON p.id_pokemon = b.id_pokemon 
        WHERE p.nombre = '{nombre_elegido}'
        """
        try:
            datos_pokemon_salvaje = cursor.execute(consulta_datos_pokemon).fetchone()
            nivel_pokemon_salvaje = random.randint(datos_pokemon_salvaje[15], datos_pokemon_salvaje[16])
            movimientos = self.calcular_movimientos_pokemon(datos_pokemon_salvaje[0], nivel_pokemon_salvaje)
            pokemon_salvaje_creado = Pokemon(*datos_pokemon_salvaje[1:15], *movimientos, nivel_pokemon_salvaje)
            return pokemon_salvaje_creado
        except sqlite3.Error as e:
            print(f"Error al crear Pokémon salvaje: {e}")
            return None



    def __str__(self):
        """
        Representación en cadena del Bosque Verde.

        :return: Descripción del Bosque Verde.
        """
        return (
            "Bosque Verde: El Bosque Verde es un bosque en el cual los árboles de esta zona son muy gruesos, "
            "por lo que entra muy poca luz. En él se encuentran principalmente Pokémon de tipo bicho. Es un gran laberinto, "
            "por lo que muchas personas se han perdido en él. También, aunque sea un bosque al aire libre, no se puede usar vuelo."
        )



    def iniciar_combate_pokemon(self, jugador):
        """
        Inicia un combate entre el jugador y un Pokémon salvaje.

        :param jugador: El jugador que va a combatir.
        """
        pokemon_salvaje = self.crear_pokemon_salvaje()
        if pokemon_salvaje:
            combate = AlgoritmoDeBatalla()
            combate.LUCHA_CONTRA_POKEMON(jugador, pokemon_salvaje)
        else:
            print("No se pudo crear un Pokémon salvaje para el combate.")
