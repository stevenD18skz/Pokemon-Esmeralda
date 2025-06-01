from Pokemon import *
from Algoritmo_De_Batalla import *
import random

from Estrucutra import *



class Area:
    def __init__(self, nombre, mapa_layout_str):
        self.nombre = nombre
        self.mapa_layout_str = mapa_layout_str.strip()
        self.matriz = [list(fila) for fila in self.mapa_layout_str.split('\n')]
        # Ahora la clave será una tupla (fila, columna)
        self.mapas_vecinos = {}

        
        self.estructuras =  {}
        self.mapa_con_estructuras = [list(row) for row in self.matriz]
        self.store = Tienda()

        # Dimensiones del mapa
        self.alto = len(self.mapa_con_estructuras)
        self.ancho = len(self.mapa_con_estructuras[0]) if self.alto > 0 else 0



    def set_vecino_por_coord(self, coord_puerta, area_destino, coord_entrada):
        """
        coord_puerta: tupla (fila, columna) indicando dónde está la puerta en este mapa.
        area_destino: la instancia de Area (o subclase) a la que se quiere ir.
        coord_entrada: tupla (fila_entrada, col_entrada) indicando dónde debe aparecer el jugador en la nueva área.
        """
        self.mapas_vecinos[coord_puerta] = (area_destino, coord_entrada)
    


    def agregar_estructura(self, coord_estructura, estructura_destino, estructura_entrada):
        """
        coord_puerta: tupla (fila, columna) indicando dónde está la puerta en este mapa.
        area_destino: la instancia de Area (o subclase) a la que se quiere ir.
        coord_entrada: tupla (fila_entrada, col_entrada) indicando dónde debe aparecer el jugador en la nueva área.
        """
        self.estructuras[coord_estructura] = (estructura_destino, estructura_entrada)



    def obtener_estructura_en_posicion(self, fila, col):
        """
        Devuelve la estructura cuya entrada está en las coordenadas dadas, o None.
        """
        for est in self.estructuras:
            if est.posicion_entrada_area == (fila, col):
                return est
        return None



    def dibujar_mapa_area(self, pos_jugador=None, marca_jugador='P'):
        """
        Devuelve un string del mapa del área, opcionalmente con el jugador.
        """
        mapa_temp = [list(row) for row in self.mapa_con_estructuras] # Copia para no modificar el original
        if pos_jugador:
            pj_fila, pj_col = pos_jugador
            if 0 <= pj_fila < self.alto and 0 <= pj_col < self.ancho:
                # Guardar el tile original antes de poner al jugador
                # tile_original = mapa_temp[pj_fila][pj_col] # Necesitarás esto si el jugador "cubre" algo
                mapa_temp[pj_fila][pj_col] = marca_jugador
        
        # Aquí podrías tener un diccionario de assets como en tu clase Game
        assets_mapa = {'1': "🌲", '0': "⬜️", 'T': "🏪", 'C': "🏥", 'E': "🏠", 'P': "🚶"}
        
        txt_mapa = [f"--- {self.nombre} ---"]
        for fila_idx, fila_lista in enumerate(mapa_temp):
            linea_renderizada = []
            for col_idx, celda in enumerate(fila_lista):
                linea_renderizada.append(assets_mapa.get(celda, celda)) # Usa asset o el carácter original
            txt_mapa.append(" ".join(linea_renderizada)) # Añade espacios para mejor visualización
        return "\n".join(txt_mapa)





class Playa(Area):
    def __init__(self):
        self.nombre = "Playa"
        mapa_layout_str = """
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
        super().__init__(nombre=self.nombre, mapa_layout_str=mapa_layout_str)



class Pueblo(Area):
    def __init__(self):
        self.nombre = "Pueblo Marino"
        mapa_layout_str = """
111111111911111111111
100000000000000000001
100000000000000000001
1000F000000000S000001
100000000000000000001
900000000000000000009
100000000000000000001
1000H000000000H000001
100000000000000000001
100000000000000000001
111111111111111111111
"""
        super().__init__(nombre=self.nombre, mapa_layout_str=mapa_layout_str)

        tienda = Tienda()
        self.agregar_estructura((3, 14), tienda, (4,4))
        


class BosqueViejoPokemon(Area):
    def __init__(self):
        """
        Inicializa la clase BosqueViejoPokemon obteniendo las probabilidades de aparición de los Pokémon
        en el Bosque Verde desde la base de datos.
        """
        self.nombre = "bosqueverde"
        mapa_layout_str = """
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
        super().__init__(nombre=self.nombre, mapa_layout_str=mapa_layout_str)

        consulta_posibilidades = f"""
        SELECT p.nombre, b.porcentaje_aparicion 
        FROM {self.nombre} b 
        JOIN pokemon p ON b.id_pokemon = p.id_pokemon
        """
        self.probabilidades = {nombre: porcentaje for nombre, porcentaje in cursor.execute(consulta_posibilidades).fetchall()}
       
       



    def calcular_pokemon_a_salir(self, opciones):
        """
        Calcula el Pokémon que aparecerá basado en las probabilidades de aparición.

        :param opciones: Un diccionario con los nombres de los Pokémon y sus probabilidades de aparición.
        :return: El nombre del Pokémon que aparece.
        """
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
    



    def crear_pokemon_salvaje(self):
        """
        Crea un Pokémon salvaje con nivel y movimientos aleatorios dentro del rango permitido.

        :return: Un objeto Pokémon con los datos generados.
        """
        nombre_elegido = self.calcular_pokemon_a_salir(self.probabilidades)
        consulta_datos_pokemon = f"""
        SELECT p.*, b.nivel_min, b.nivel_max 
        FROM {self.nombre} b 
        JOIN pokemon p ON p.id_pokemon = b.id_pokemon 
        WHERE p.nombre = '{nombre_elegido}'
        """
        datos_pokemon_salvaje = cursor.execute(consulta_datos_pokemon).fetchone()
        nivel_pokemon_salvaje = random.randint(datos_pokemon_salvaje[15], datos_pokemon_salvaje[16])
        movimientos = self.calcular_movimientos_pokemon(datos_pokemon_salvaje[0], nivel_pokemon_salvaje)
        pokemon_salvaje_creado = Pokemon(*datos_pokemon_salvaje[1:15], *movimientos, nivel_pokemon_salvaje)
        return pokemon_salvaje_creado
    



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