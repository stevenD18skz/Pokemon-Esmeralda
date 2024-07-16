from Pokemon import *
from Algoritmo_De_Batalla import *
import random



class BosqueViejoPokemon:
    def __init__(self):
        """
        Inicializa la clase BosqueViejoPokemon obteniendo las probabilidades de aparición de los Pokémon
        en el Bosque Verde desde la base de datos.
        """
        self.nombre = "Bosque Verde"
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
