from Pokemon import *
from Algoritmo_De_Batalla import *
import random
#OPCION 3


class BosqueViejoPokemon:
    def __init__(self):
        self.nombre = "Bosque Verde"
        consulta_posibilidades = "SELECT p.nombre, b.porcentaje_aparicion FROM bosqueverde b JOIN pokemon p ON b.id_pokemon = p.id_pokemon"
        self.probabilidades = {nombre: porcentaje for nombre, porcentaje in cursor.execute(consulta_posibilidades).fetchall()}


    def calcular_pokemon_a_salir(self, opciones):#✔✔✔
        return "Bulbasaur"
        total_probabilidad = sum(opciones.values())
        probabilidad_acumulada = 0
        num_aleatorio = random.uniform(0, 1)

        for opcion, probabilidad in opciones.items():
            probabilidad_acumulada += probabilidad / total_probabilidad
            if num_aleatorio <= probabilidad_acumulada:
                return opcion



    def calcular_movimientos_pokemon(self, id_pokemonE, nivelPokemon):#✔✔✔
        consulta_movimiento = f"""
                SELECT id_movimiento
                from pokemon_movimiento
                WHERE nivel <= {nivelPokemon} AND id_pokemon == {id_pokemonE}
        """
        cursor.execute(consulta_movimiento)
        posibles_movimientos = [t[0] for t in cursor.fetchall()]
        cantidad = 4 if len(posibles_movimientos) > 4 else len(posibles_movimientos)
        id_movimientos = random.sample(posibles_movimientos, cantidad)
        nuevas_listas = id_movimientos + [1] * (4 - len(id_movimientos)) if len(id_movimientos) < 4 else id_movimientos
        moivimietos_creados = []
        for x in range(4):
            consulta_movimiento = "SELECT * FROM movimiento WHERE id_movimiento = '" + str(nuevas_listas[x]) + "'"
            cursor.execute(consulta_movimiento)
            datos_movimiento = cursor.fetchall()[0]
            consulta_efSecundario = "SELECT * FROM estado WHERE id_estado = '" + str(datos_movimiento[-1]) + "'"
            cursor.execute(consulta_efSecundario)
            datos_efSecundario = cursor.fetchall()[0]
            crear_movimiento = Movimiento(*datos_movimiento[1:-1], Estado(*datos_efSecundario[1:]))
            moivimietos_creados.append(crear_movimiento)
        list(map(lambda x: print(x.getNombre()), moivimietos_creados))
        return moivimietos_creados




    def crear_pokemon_salvaje(self):#✔✔✔
        nombre_elegido = self.calcular_pokemon_a_salir(self.probabilidades)
        consulta_datos_pokemon = "SELECT p.*, b.nivel_min, b.nivel_max FROM bosqueverde as b JOIN pokemon as p ON p.id_pokemon = b.id_pokemon WHERE p.nombre = '" + nombre_elegido + "'"
        datos_pokemon_salvaje = cursor.execute(consulta_datos_pokemon).fetchall()[0]
        nivel_pokemon_salvaje = random.randint(datos_pokemon_salvaje[15], datos_pokemon_salvaje[16])
        moivimietos_creados = self.calcular_movimientos_pokemon(datos_pokemon_salvaje[0], nivel_pokemon_salvaje)
        pokemon_salvaje_creado = Pokemon(*datos_pokemon_salvaje[1:15],*moivimietos_creados, nivel_pokemon_salvaje)
        moivimietos_creados.clear()
        return pokemon_salvaje_creado



    def __str__(self):#✔✔✔
        return f"""Bosque Verde: El Bosque Verde es un bosque en el cual los árboles de esta zona son muy gruesos, por lo que entra muy poca luz. 
                En él se encuentran principalmente Pokémon de tipo bicho. Es un gran laberinto, por lo que muchas personas se han perdido en él. También, 
                aunque sea un bosque al aire libre, no se puede usar vuelo."""




    def iniciar_combate_pokemon(self, jugador):#✔✔✔
        pokemon_salvaje = self.crear_pokemon_salvaje()
        figth = AlgoritmoDeBatalla()
        figth.LUCHA_CONTRA_POKEMON(jugador, pokemon_salvaje)