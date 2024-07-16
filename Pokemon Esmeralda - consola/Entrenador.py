from Pokemon import *

from Mochila import *
#OPCION 3


#equipoDelCampeon = [crear_pokemon_campeon(x[1:]) for x in datos_equipo]
"""
COSAS POR HACER:
-arreglar la parte de la evolucion 
"""



class Entrenadores:
    def __init__(self, nombre, dinero, edad, estatus, mochila, #✔✔✔
                 pk_1, pk_2, pk_3, pk_4, pk_5, pk_6):
        self.nombre = nombre
        self.dinero = dinero
        self.edad = edad
        self.estatus = estatus
        self.mochila = mochila
        self.contadorVictorias = 0
        self.contadorDerrotas = 0
        self.equipo_Pokemon = [pk_1, pk_2, pk_3, pk_4, pk_5, pk_6]



    def mostrar_informacion(self):#✔✔✔
        print("Nombre:", self.nombre)
        print("Dinero:", self.dinero)
        print("Edad:", self.edad)
        print("Estatus:", self.estatus)
        print("Contador de Victorias:", self.contadorVictorias)
        print("Contador de Derrotas: ", self.contadorDerrotas)
        print("Equipo Pokemon:")
        for pokemon in self.equipo_Pokemon:
            print(f" - {pokemon.getNombre()} (Nivel {pokemon.getNivel()})")



    def imprimir_pokemons(self):
        txt = []
        for i in range(0, 6, 2):
            txt.append(f"{i+1}.{self.equipo_Pokemon[i].getNombre()}                  {i+2}.{self.equipo_Pokemon[i+1].getNombre()}")
            txt.append(f"Nv: {self.equipo_Pokemon[i].getNivel()}    Est: {self.equipo_Pokemon[i].getEstado().getNombre()}      Nv: {self.equipo_Pokemon[i+1].getNivel()}    Est: {self.equipo_Pokemon[i+1].getEstado().getNombre()}")
            txt.append(f"💚>{self.equipo_Pokemon[i].getPs()}/{self.equipo_Pokemon[i].getMps()}<💚              💚>{self.equipo_Pokemon[i+1].getPs()}/{self.equipo_Pokemon[i+1].getMps()}<💚\n")
        
        return '\n'.join(txt)




    def Adquirir_Pokemon(self, poke):#✔✔✔
        if poke.getEspecie() == "NINE":
            return
        for espacio in range(6):
            if self.equipo_Pokemon[espacio].getEspecie() == "NINE":
                self.equipo_Pokemon[espacio] = poke
                print(f"{poke.getNombre()} se ha unido al equipo de {self.nombre}.")
                return
        print("el pokemon ah sido mandado al valle")



    def usar_mochila(self):
        while True:
            objeto_sacado = self.mochila.abrir_mochila()
            #no saco ningun objeto
            if not objeto_sacado:
                print("(se cierra la mochila)")
                return
            
            eleccion_uso = int(input("1.usar       2.dar\n3.tirar      4.salir\n=="))

            if eleccion_uso == 4:
                pass

            elif eleccion_uso == 1:
                if objeto_sacado.getTipo() != "pokéball":
                    while True:
                        self.imprimir_pokemons()
                        objetivo = int(input(f"///Ah que pokemon le quieres dar la medicina\n== "))-1
                        if (self.equipo_Pokemon[objetivo].getPs() == 0 or
                            self.equipo_Pokemon[objetivo].getEspecie() == "NINE" or
                            objetivo < 0 or objetivo > 5):
                            print("❌❌❌ POR FAVOR ELIGE UNA OPCIÓN VÁLIDA, POR FAVOR ❌❌❌\n")
                        else:
                            break
                    
                    objeto_sacado.sanarPokemon(self.equipo_Pokemon[objetivo])
                    print(f"🍂🍂🍂 SE AH USADO EL OBJETOOOO 🍂🍂🍂")
                
                else:
                    print("cada objeto a su tiempo")



    def evolucionar_su_pokemon(self, ant, evo):#✔✔✔
        indice = 0
        for i in range(6):
            if self.equipo_Pokemon[i].n_id == ant:
                indice = i

        print(f"quieres que {self.equipo_Pokemon[indice].nombre} evolucione a {evo.nombre}???")
        decision = int(input("==="))

        if decision == 2:
            return

        self.equipo_Pokemon[indice] = evo
        print(f"AH EVOLUCIONADO A {evo.nombre}!!!!!!!!!!!")





    def getNombre(self):
        return self.nombre

    def setNombre(self, nuevoNombre):
        self.nombre = nuevoNombre

    def getDinero(self):
        return self.dinero

    def setDinero(self, valor):
        self.dinero = valor

    def getEdad(self):
        return self.edad

    def getMochila(self):
        return self.mochila



def crear_pokemon_entrenador(nombrePokemon, nivel = 50):
    consulta = "SELECT * FROM pokemon WHERE nombre = '" + nombrePokemon + "'"
    datos_del_pokemon = cursor.execute(consulta).fetchall()[0]
    id_movimientos = ['3','11','8','12']
    moivimietos_creados = []
    for x in range(4):
        consulta_del_movimiento = "SELECT * FROM movimiento WHERE id_movimiento = '" + str(id_movimientos[x]) + "'"
        datos_movimiento = cursor.execute(consulta_del_movimiento).fetchall()[0]

        consulta_efSecundario = "SELECT * FROM estado WHERE id_estado = '" + str(datos_movimiento[-1]) + "'"
        datos_efSecundario = cursor.execute(consulta_efSecundario).fetchall()[0]

        crear_movimiento = Movimiento(*datos_movimiento[1:-1], Estado(*datos_efSecundario[1:]))
        moivimietos_creados.append(crear_movimiento)

    pokemon_creado = Pokemon(*datos_del_pokemon[1:15],*moivimietos_creados, nivel)
    moivimietos_creados.clear()
    return pokemon_creado



def crear_pokemon_campeon(datos_pokemon_campeon):
    consulta_datos_pokemon = f"""
        SELECT *
        FROM pokemon
        WHERE id_pokemon = {datos_pokemon_campeon[0]}"""
    datos_pokemon = cursor.execute(consulta_datos_pokemon).fetchall()[0][1:15]
    id_movimientos = datos_pokemon_campeon[2:6]

    moivimietos_creados = []
    for x in id_movimientos:
        consulta_movimiento = "SELECT * FROM movimiento WHERE id_movimiento = '" + str(x) + "'"
        datos_movimiento = cursor.execute(consulta_movimiento).fetchall()[0]

        consulta_efSecundario = "SELECT * FROM estado WHERE id_estado = '" + str(datos_movimiento[-1]) + "'"
        datos_efecto = cursor.execute(consulta_efSecundario)
        datos_efSecundario = cursor.fetchall()[0]

        crear_movimiento = Movimiento(*datos_movimiento[1:-1], Estado(*datos_efSecundario[1:]))
        moivimietos_creados.append(crear_movimiento)

    pokemon_campeon = Pokemon(*datos_pokemon,*moivimietos_creados, datos_pokemon_campeon[1])
    moivimietos_creados.clear()
    return pokemon_campeon



def crear_oponente(campeon):
    consultar_datos_campeon = f"""
        SELECT *
        FROM campeon
        WHERE nombre = "{campeon}";
    """
    datos_campeon = cursor.execute(consultar_datos_campeon).fetchall()[0][1:]


    consultar_datos_equipo = f"""
        SELECT *
        FROM campeon_pokemon
        WHERE id_campeon = "{campeon}";
    """
    datos_equipo = cursor.execute(consultar_datos_equipo).fetchall()
    equipoDelCampeon = []

    for i in range(6):
        try:
            equipoDelCampeon.append(crear_pokemon_campeon(datos_equipo[i][1:]))
        except:
            equipoDelCampeon.append(crear_pokemon_entrenador(""))

    #equipoDelCampeon = [crear_pokemon_campeon(datos_equipo[i][1:]) if i < len(datos_equipo) else crear_pokemon_entrenador("") for i in range(6)]
    #equipoDelCampeon = map(lambda x: crear_pokemon_campeon(x[1:]), datos_equipo)
    return Entrenadores(*datos_campeon, Mochila(), *equipoDelCampeon)