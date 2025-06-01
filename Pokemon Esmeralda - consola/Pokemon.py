from Movimiento import *
import random
#OPCION 3


"""
COSAS POR HACER:
-arreglar la parte de la evolucion para que funcione correctamente
-arreglar la parte de SQL en en la tablas que esten relacionadas con pokemon
"""

import random

# Diccionario de naturalezas
NATURALEZAS = {
    "Fuerte": [1, 1, 1, 1, 1],
    "Osada": [0.9, 1.1, 1, 1, 1],
    "Modesta": [0.9, 1, 1.1, 1, 1],
    "Serena": [0.9, 1, 1, 1.1, 1],
    "Miedosa": [0.9, 1, 1, 1, 1.1],
    "Huraña": [1.1, 0.9, 1, 1, 1],
    "Docil": [1, 1, 1, 1, 1],
    "Afable": [1, 0.9, 1.1, 1, 1],
    "Amable": [1, 0.9, 1, 1.1, 1],
    "Activa": [1, 0.9, 1, 1, 1.1],
    "Firme": [1.1, 1, 0.9, 1, 1],
    "Agitada": [1, 1.1, 0.9, 1, 1],
    "Timida": [1, 1, 1, 1, 1],
    "Cauta": [1, 1, 0.9, 1.1, 1],
    "Alegre": [1, 1, 0.9, 1, 1.1],
    "Picara": [1.1, 1, 1, 0.9, 1],
    "Floja": [1, 1.1, 1, 0.9, 1],
    "Alocada": [1, 1, 1, 0.9, 1],
    "Rara": [1, 1, 1, 1.1, 1],
    "Ingenua": [1, 1, 1, 0.9, 1],
    "Audaz": [1.1, 1, 1, 1, 0.9],
    "Placida": [1, 1.1, 1, 1, 0.9],
    "Mansa": [1, 1, 1.1, 1, 0.9],
    "Grosera": [1, 1, 1, 1.1, 0.9],
    "Seria": [1, 1, 1, 1, 1],
}

# Lista de nombres de naturalezas
NOM_NATURALEZAS = list(NATURALEZAS.keys())




class Pokemon:
    def __init__(self, nombre, especie, 
                 B_ps, B_ataque, B_ataque_especial, B_defensa, B_defensa_especial, B_velocidad, tipo1, tipo2, 
                 ratioDeCaptura, formula, exp_Base, puntosEVSqueda, movimiento1, movimiento2, movimiento3, movimiento4, 
                 nivel):#✔✔✔
        self.nombre = nombre
        self.especie = especie
        self.n_id = random.randint(0, 65535)
        #Los stacks base del pokemon
        self.B_ps = B_ps
        self.B_ataque = B_ataque
        self.B_ataque_especial = B_ataque_especial
        self.B_defensa = B_defensa
        self.B_defensa_especial = B_defensa_especial
        self.B_velocidad = B_velocidad

        #Atributos clave para los stats
        self.tipo1 = tipo1
        self.tipo2 = tipo2
        self.nivel = nivel
        self.ratioDeCaptura = ratioDeCaptura
        self.formula = formula
        self.exp_Base = exp_Base
        self.puntosDeEzfuerzo = [
            0, 0, 0, 0, 0, 0
        ]

        puntosEVSqueda = puntosEVSqueda.split(",")
        puntosEVtupla = (int(puntosEVSqueda[0]),int(puntosEVSqueda[1]))
        self.puntosQueBlinda = puntosEVtupla



        #Movimientos del pokemon
        self.movimiento1 = movimiento1
        self.movimiento2 = movimiento2
        self.movimiento3 = movimiento3
        self.movimiento4 = movimiento4
        self.slotsDeMovimientos = [self.movimiento1,self.movimiento2,self.movimiento3,self.movimiento4]



        #IVs y Naturaleza del pokemon
        self.IVs = [random.randint(1, 32) for _ in range(6)]
        self.Naturaleza = ""
        self.NaturalezaValores = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.ps = 0
        self.M_ps = 0
        self.ataque = 0
        self.ataque_especial = 0
        self.defensa = 0
        self.defensa_especial = 0
        self.velocidad = 0
        self.experiencia = 0
        
        self.Naturaleza = random.choice(NOM_NATURALEZAS)
        self.NaturalezaValores = NATURALEZAS[self.Naturaleza]
        self.Establecer_Stats()
        self.experiencia = self.Establecer_exp(self.formula, self.nivel)



        consulta_estado = f"""
            SELECT *
            FROM estado
            WHERE id_estado = 1
        """
        cursor.execute(consulta_estado)
        estado_consultado = cursor.fetchall()[0][1:]
        self.estado_poke = Estado(*estado_consultado)




    def mostrar_informacion(self):#✔✔✔
        txt = []
        txt.append("◤────────────────────────────────────◥")
        txt.append(f"    🌀los stats de {self.nombre} son🌀")
        txt.append("┌────────────────────────────────────┐")
        txt.append(f"│  Nivel:{self.nivel}         Vida:{self.ps}/{self.M_ps}         │")
        txt.append(f"│  Ataque:{self.ataque}        Ataque Especial:{self.ataque_especial}   │")
        txt.append(f"│  Defensa:{self.defensa}       Defensa Especial:{self.defensa_especial}  │")
        txt.append(f"│  Velocidad:{self.velocidad}     Naturaleza:{self.Naturaleza}    │")
        txt.append(f"│  Estado:{self.estado_poke.nombre}  Experiencia:{self.experiencia}   │")
        txt.append("└────────────────────────────────────┘")
        txt.append("┌────────────────────────────────────┐")
        txt.append(f"│  Movimiento #1: {self.slotsDeMovimientos[0].nombre}   │")
        txt.append(f"│  Movimiento #2: {self.slotsDeMovimientos[1].nombre}   │")
        txt.append(f"│  Movimiento #3: {self.slotsDeMovimientos[2].nombre}   │")
        txt.append(f"│  Movimiento #4: {self.slotsDeMovimientos[3].nombre}   │")
        txt.append("└────────────────────────────────────┘")
        txt.append("┌────────────────────────────────────┐")
        txt.append(f"│  Ivs: {", ".join(map(str, self.IVs))}        │")
        txt.append(f"│  Pnt.Efz: {", ".join(map(str, self.puntosDeEzfuerzo))}         │")
        txt.append("└────────────────────────────────────┘")
        txt.append(f"◣────────────────────────────────────◢")
        
        return "\n".join(txt)



    def mostrarAtaques(self):#✔✔✔
        txt = []
        
        txt.append(f"◤{"─"*90}◥")
        txt.append(f"│ 1. {self.slotsDeMovimientos[0].getNombre()} pp: {self.slotsDeMovimientos[0].getPP()} / {self.slotsDeMovimientos[0].getMPP()}                        2. {self.slotsDeMovimientos[1].getNombre()} pp: {self.slotsDeMovimientos[1].getPP()} / {self.slotsDeMovimientos[1].getMPP()}")
        txt.append(f"│    Tipo: {self.slotsDeMovimientos[0].getTipo()}                                   Tipo: {self.slotsDeMovimientos[1].getTipo()}")
        txt.append(f"│")
        txt.append(f"│\n│ 3. {self.slotsDeMovimientos[2].getNombre()} pp: {self.slotsDeMovimientos[2].getPP()}/ {self.slotsDeMovimientos[2].getMPP()}                        4. {self.slotsDeMovimientos[3].getNombre()} pp: {self.slotsDeMovimientos[3].getPP()}/ {self.slotsDeMovimientos[3].getMPP()}")
        txt.append(f"│    Tipo: {self.slotsDeMovimientos[2].getTipo()}                                  Tipo: {self.slotsDeMovimientos[3].getTipo()}")
        txt.append(f"◣{"─"*90}◢")
        
        return "\n".join(txt)




    def aumentar(self, Base, num, Naturaleza):#✔✔✔
        """
        Calcula el valor de un stat del Pokémon ajustado por su naturaleza.

        Args:
            Base (int): El valor base del stat.
            num (int): El índice del stat en las listas de IVs y puntos de esfuerzo.
            Naturaleza (float): El multiplicador de la naturaleza para el stat.

        Returns:
            int: El valor ajustado del stat, redondeado al entero más cercano.
        """
        han = (((((2*Base)+self.IVs[num]+(self.puntosDeEzfuerzo[num]/4))*self.nivel)/100)+5)*Naturaleza
        return round(han)




    def Establecer_Stats(self):#✔✔✔
        """
        Calcula y establece los stats finales del Pokémon.

        Esta función calcula los valores finales de los stats del Pokémon, 
        incluyendo PS (Puntos de Salud), ataque, ataque especial, defensa, 
        defensa especial y velocidad, ajustándolos por los valores base, 
        IVs, puntos de esfuerzo y naturaleza.

        Returns:
            None
        """
        vida_base = ((((2*self.B_ps)+self.IVs[0]+(self.puntosDeEzfuerzo[0]/4))*self.nivel)/100)+self.nivel+10
        self.ps = round(vida_base)
        self.M_ps = round(vida_base)
        self.ataque = self.aumentar(self.B_ataque, 1, self.NaturalezaValores[0])
        self.ataque_especial = self.aumentar(self.B_ataque_especial, 4, self.NaturalezaValores[1])
        self.defensa = self.aumentar(self.B_defensa, 2, self.NaturalezaValores[2])
        self.defensa_especial = self.aumentar(self.B_defensa_especial, 5, self.NaturalezaValores[3])
        self.velocidad = self.aumentar(self.B_velocidad, 3, self.NaturalezaValores[4])




    def Establecer_exp(self, metodo, nivel):#✔✔✔
        """
        Establece la experiencia del Pokémon según un método y nivel dados.

        Args:
            metodo (str): El método de crecimiento de experiencia. Puede ser "Rapido", "Medio", "Lento" o "Parabolico".
            nivel (int): El nivel del Pokémon para el cual se calcula la experiencia.

        Returns:
            int: La cantidad de experiencia necesaria para alcanzar el nivel dado.
        """
        formulas = {
            "Rapido": (4 * nivel ** 3) // 5,
            "Medio": nivel ** 3,
            "Lento": (5 * nivel ** 3) // 4,
            "Parabolico": (6 * nivel ** 3) // 5 - 15 * nivel ** 2 + 100 * nivel - 140
        }
        
        return round(formulas[metodo])



    #ver bien donde irian las funciones y ver los ataques especiales
    def Atacar(self, enemigo, seleccion):
        ATAQUE = self.slotsDeMovimientos[seleccion]
        self.slotsDeMovimientos[seleccion].setPP(self.slotsDeMovimientos[seleccion].getPP()-1)

        bono = 1.5 if ATAQUE.getTipo() in (self.tipo1, self.tipo2) else 1

        def get_effectiveness(attack_type, defense_type):
            query = f"""
                SELECT efectividad
                FROM tipo
                WHERE tipo_atacante = '{attack_type.lower()}' AND tipo_receptor = '{defense_type.lower()}'"""
            print(f"ataque = {attack_type.lower()}, defensa = {defense_type.lower()}, querry = {query}")
            return cursor.execute(query).fetchall()[0][0]

        efc1 = get_effectiveness(ATAQUE.getTipo(), enemigo.getTipo())
        efc2 = get_effectiveness(ATAQUE.getTipo(), enemigo.getTipoSecundario()) if enemigo.getTipoSecundario() else 1

        efectividad = efc1 * efc2
        
        variacion = random.randint(85,100)

        nivelDeAtacante = self.nivel

        C_ataque = self.ataque_especial if ATAQUE.clase == "Especial" else self.ataque

        C_defensa = enemigo.getDefensaEspecial() if ATAQUE.clase == "Especial" else enemigo.getDefensa()

        potencia_ataque = ATAQUE.getPotencia()

        mensajes = []
        if potencia_ataque != 0:
            daño = round(int(0.01 * bono * efectividad * variacion * (((0.2 * nivelDeAtacante + 1) * C_ataque * potencia_ataque) / (25 * C_defensa) + 2)))
            
            print("Valor de las variables:")
            print(f"bono = {bono}")
            print(f"efectividad = {efectividad}")
            print(f"variacion = {variacion}")
            print(f"nivelDeAtacante = {nivelDeAtacante}")
            print(f"C_ataque = {C_ataque}")
            print(f"potencia_ataque = {potencia_ataque}")
            print(f"C_defensa = {C_defensa}")

            print("\nResultado final:")
            print(f"Resultado = {daño}")

            
            
            
            
            mensajes.append(f"🩸🩸🩸 el ataque de {self.nombre} ah causado {daño} puntos de Daño a {enemigo.nombre}  🩸🩸🩸")
            enemigo.setPs(enemigo.getPs()-daño)

        self.slotsDeMovimientos[seleccion].setPP(self.slotsDeMovimientos[seleccion].getPP()-1)
        

        if enemigo.getEstado().getNombre() == "Normal🍞" and ATAQUE.getEfectoSecundario().getNombre() != "Normal🍞":
            if ATAQUE.getProbabilidadDelEfecto() >= random.randint(0, 100):
                enemigo.setEstado(ATAQUE.getEfectoSecundario())
                mensajes.extend(enemigo.getEstado().aplicar_segundo_efecto(enemigo))
                mensajes.append(f"🦝🦝🦝 El estado de {enemigo.getNombre()} ah cambiado a {enemigo.getEstado().getNombre()} 🦝🦝🦝")

            else:
                mensajes.append(f"🪬🪬🪬 EL ATAQUE NO AH ALCANZADO A APLICAR EL EFECTO SECUNDARIO  🪬")
        
        return mensajes



    #RELACIONES CON DE MAS ENTIDADES
    def recibir_objeto(self, medicina):
        medicina.aplicar_efecto_pokemon(self)
    


    #METODOS CORRESPONEIDNTES CON LA SUBIDA DE NIVEL
    def subir_de_nivel(self):#✔✔✔
        self.Establecer_Stats()
        self.hay_movimiento_por_aprender()
        return self.se_puede_evolucionar()
    
    

    def hay_movimiento_por_aprender(self):#✔✔✔
        nombrePoke = self.nombre
        nivelPoke = self.nivel

        consultar_movimiento = f"""
            SELECT movimiento.id_movimiento, movimiento.nombre AS nombre_movimiento
            FROM pokemon
            JOIN pokemon_movimiento ON pokemon.id_pokemon = pokemon_movimiento.id_pokemon
            JOIN movimiento ON pokemon_movimiento.id_movimiento = movimiento.id_movimiento
            WHERE pokemon.nombre = '{nombrePoke}' AND pokemon_movimiento.nivel = {nivelPoke}
            LIMIT 0, 1000;
        """
        cursor.execute(consultar_movimiento)
        try:
            id_de_movimiento = cursor.fetchall()[0]

        except IndexError:
            return None


        id_para_consulta = id_de_movimiento[0]
        consulta_del_movimiento = f"""
            SELECT * 
            FROM movimiento
            WHERE id_movimiento = {id_para_consulta}  
        """
        cursor.execute(consulta_del_movimiento)
        datos_movimiento = cursor.fetchall()[0]
        self.aprender_nuevo_movimiento(datos_movimiento)



    def aprender_nuevo_movimiento(self, datosMovimiento):#✔✔✔
        consulta_efecto_movimiento = f"""
            SELECT *
            FROM estado
            WHERE id_estado = {datosMovimiento[-1]}
        """
        cursor.execute(consulta_efecto_movimiento)
        efecto_consultado = Estado(*cursor.fetchall()[0][1:])
        movimientoNuevo = Movimiento(*datosMovimiento[1:len(datosMovimiento)-1],efecto_consultado)  


        cantidad = sum(1 for x in range(4) if self.slotsDeMovimientos[x].getNombre() != "")
        if cantidad < 4:#aun tiene espacio para un nuevo movimiento
            print(f"Felicidades, {self.nombre} ah aprendido el movimiento {movimientoNuevo.getNombre()}!!!")
            self.slotsDeMovimientos[cantidad] = movimientoNuevo
            return None


        while True:
            print(f"{self.nombre} actualmente tiene cuatro movimientos.\nPor favor, selecciona cuál de estos movimientos te gustaría que sea reemplazado por {movimientoNuevo.getNombre()}.")
            self.mostrarAtaques()
            seleccion_movimiento = int(input(f"Si deseas que {self.nombre} no aprenda {movimientoNuevo.getNombre()} pulsa 5.\n==>"))

            if seleccion_movimiento == 5:
                print(f"{self.nombre} se queda todos sus movimientos intactos")
                break

            try:
                print(f"{self.nombre} ah olvidado {self.slotsDeMovimientos[seleccion_movimiento-1].getNombre()} y ah aprendido el movimiento {movimientoNuevo.getNombre()}!!!")
                self.slotsDeMovimientos[seleccion_movimiento-1] = movimientoNuevo
                break
            
            except:
                print("XXX ESCOGE UNA OPCION VALIDAAAA XXX")
    


    def se_puede_evolucionar(self):#✔✔✔
        print("=" * 34)
        nombrePoke = self.nombre
        nivelPoke = self.nivel
        print(nivelPoke, nombrePoke)
        consultar_evolucion = f"""
            SELECT * 
            FROM pokemon
            WHERE id_pokemon = (
                SELECT e.id_evolucion
                FROM evolucion_pokemon as e
                JOIN pokemon as p ON p.id_pokemon = e.id_pre_evolucion
                WHERE nivel_evolucion = {int(nivelPoke)} AND p.nombre = '{nombrePoke}'
            );
        """
        cursor.execute(consultar_evolucion)
        try:
            datosEvolucion = cursor.fetchall()[0]

            print(datosEvolucion)
            print(f"{self.nombre} esta a punto de evolucionar")
            evolucion = Pokemon(*datosEvolucion[1:15],*self.slotsDeMovimientos, self.nivel)
            evolucion.IVs = self.IVs
            evolucion.puntosDeEzfuerzo = self.puntosDeEzfuerzo
            evolucion.Establecer_Stats()
            return evolucion
            
        except IndexError:
            return None
            












    def getNombre(self):
        return self.nombre

    def setNombre(self, nuevoNombre):
        self.nombre = nuevoNombre

    def getEspecie(self):
        return self.especie

    def getPs(self):
        return self.ps

    def setPs(self, nuevoPs):
        if nuevoPs <= 0:
            self.ps = 0

            consulta_estado = f"""
                SELECT *
                FROM estado
                WHERE id_estado = 14
            """
            cursor.execute(consulta_estado)
            estado_consultado = cursor.fetchall()[0][1:]
            self.estado_poke = Estado(*estado_consultado)
            return
        if nuevoPs > self.M_ps:
            self.ps = self.M_ps
            return
        self.ps = nuevoPs

    def getMps(self):
        return self.M_ps

    def getAtaque(self):
        return self.ataque

    def setAtaque(self, ataque):
        self.ataque = ataque

    def getAtaqueEspecial(self):
        return self.ataqueEspecial

    def setAtaqueEspecial(self, ataqueEspecial):
        self.ataqueEspecial = ataqueEspecial

    def getDefensa(self):
        return self.defensa

    def setDefensa(self, defensa):
        self.defensa = defensa

    def getDefensaEspecial(self):
        return self.defensa_especial

    def setDefensaEspecial(self, defensa_especial):
        self.defensa_especial = defensa_especial

    def getVelocidad(self):
        return self.velocidad

    def setVelocidad(self, velocidad):
        self.velocidad = velocidad

    def getNivel(self):
        return self.nivel

    def setNivel(self, nuevoNivel):
        self.nivel = nuevoNivel
        return self.subir_de_nivel()
        

    def getTipo(self):
        return self.tipo1

    def getTipoSecundario(self):
        return self.tipo2

    def getEstado(self):
        return self.estado_poke

    def setEstado(self, nuevoEstado):
        self.estado_poke = nuevoEstado

    def getFormula(self):
        return self.formula

    def getExperiencia(self):
        return self.experiencia

    def setExperiencia(self, nuevaExp):
        self.experiencia += nuevaExp

    def getMovimiento(self, selec):
        return self.slotsDeMovimientos[selec]
    
    def getCantidadDeMovimientos(self):
        cont = 0
        for movimiento in self.slotsDeMovimientos:
            if movimiento.getNombre() != "":
                cont += 1
        return cont

    def setMovimiento(self, nuevoMovimiento):
        self.movimientos.append(nuevoMovimiento)

    def getExp_Base(self):
        return self.exp_Base

    def getRatioDeCaptura(self):
        return self.ratioDeCaptura

    def setPuntosDeEzfuerzo(self, Asumar):
        self.puntosDeEzfuerzo[Asumar[0]] += Asumar[1]
        ps_actuales = self.ps
        self.Establecer_Stats()
        self.ps = ps_actuales

    def getPuntosBlindar(self):
        return self.puntosQueBlinda
