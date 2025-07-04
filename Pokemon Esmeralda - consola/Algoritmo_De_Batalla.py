from Pokemon import *
from Entrenador import *
import math
import os
import time
from data import interfaz_usuario
from enum import Enum



BACK_OPTION = "X"


class AccionCombate(Enum):
    LUCHAR = 1
    MOCHILA = 2
    CAMBIAR = 3
    HUIDA = 4



class EstadoCombate(Enum):
    VICTORIA = "victoria"
    DERROTA = "derrota"
    HUIDA = "huida"



class AlgoritmoDeBatalla:
    def __init__(self):
        self.turno = 1
        self.PokemonesQueLucharon = []

        self.CURRENTFIGHTER = None
        self.OPPONENTPOKEMON = None
        self.PLAYER = None

        self.encounter_type = ""
        self.ENEMY_TRAINER = None



    #METODOS PARA EL ESCENARIO
    def mensaje_batalla(self, *mensaje, is_input=False, validacion=None, mensaje_raise=""):
        """
        Función auxiliar para llamar a self.mensaje_batalla con el display preestablecido para batallas.
        
        Parámetros:
        -----------
        mensaje : str
            El mensaje principal que se mostrará al usuario.
        
        is_input : bool, opcional
            Indica si se espera una entrada del usuario.
        
        validacion : function, opcional
            Una función que toma la entrada del usuario como argumento y devuelve True si la entrada es válida, 
            o False si no lo es.
        
        mensaje_raise : str, opcional
            El mensaje que se mostrará si la validación de la entrada falla.
        """
        return interfaz_usuario(
            *mensaje,
            display=self.imprimir_escenario_de_batalla(),
            is_input=is_input,
            validacion=validacion,
            mensaje_raise=mensaje_raise
        )



    def barra_de_vida(self, pokemon, tamanno):#✔✔✔
        BV_vida = int(pokemon.getPs() * (tamanno / pokemon.getMps()))
        aux = "|" * BV_vida + "-" * (int(tamanno) - BV_vida)
        return aux

    

    def barra_de_pokeballs(self, trainer):#⭕🔴⚪⚫✔✔✔
        barra = ""
        for pokemon in trainer.equipo_Pokemon:
            if pokemon.getEspecie() == "NINE":
                barra += "⚪ "

            elif pokemon.getPs() == 0:
                barra += "⚫ "

            else:
                barra += "🔴 "

        return barra



    def imprimir_escenario_de_batalla(self):#✔✔✔
        txt = []
        txt.append("❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ")
        PvidaRival = round((self.OPPONENTPOKEMON.getPs() * 100) / self.OPPONENTPOKEMON.getMps())
        Pvida = round((self.CURRENTFIGHTER.getPs() * 100) / self.CURRENTFIGHTER.getMps())
        txt.append(
            f"{self.barra_de_pokeballs(self.ENEMY_TRAINER) if self.encounter_type == "ENTRENADOR" else ""}"
            f"\n{self.OPPONENTPOKEMON.getNombre()}🦅    Nv:{self.OPPONENTPOKEMON.getNivel()}"
            f"\nPS:💙{self.barra_de_vida(self.OPPONENTPOKEMON, 50)}💙 = {self.OPPONENTPOKEMON.getPs()}/{self.OPPONENTPOKEMON.getMps()} = {PvidaRival}%"
            f"\nEstado:{self.OPPONENTPOKEMON.getEstado().getNombre()}"
            "\n\n\n\n\n\n\n"
            f"                                       {self.CURRENTFIGHTER.getNombre()}🐣    Nv:{self.CURRENTFIGHTER.getNivel()}"
            f"\n                                       PS:💙{self.barra_de_vida(self.CURRENTFIGHTER, 50)}💙 = {self.CURRENTFIGHTER.getPs()}/{self.CURRENTFIGHTER.getMps()} = {Pvida}%"
            f"\n                                       Estado:{self.CURRENTFIGHTER.getEstado().getNombre()}                                               EXP:{self.CURRENTFIGHTER.getExperiencia()-(self.CURRENTFIGHTER.Establecer_exp(self.CURRENTFIGHTER.getFormula(), self.CURRENTFIGHTER.getNivel()))}/{(self.CURRENTFIGHTER.Establecer_exp(self.CURRENTFIGHTER.getFormula(), self.CURRENTFIGHTER.getNivel()+1)) - self.CURRENTFIGHTER.Establecer_exp(self.CURRENTFIGHTER.getFormula(), self.CURRENTFIGHTER.getNivel())}"
            f"\n                                       {self.barra_de_pokeballs(self.PLAYER)}\n"
        )
        return '\n'.join(txt)





    #OPCION DE ATACAR
    def get_attack_selection(self):
        while True:
            seleccion_ataque = self.mensaje_batalla(
                f"⚔⚔¿que ataque deberia usar {self.CURRENTFIGHTER.getNombre()}⚔⚔:\n {self.CURRENTFIGHTER.mostrarAtaques()}\n{BACK_OPTION}. Atras",
                is_input=True,
                validacion=lambda x: x == BACK_OPTION or 1 <= int(x) <= self.CURRENTFIGHTER.getCantidadDeMovimientos(),
                mensaje_raise=f"❌❌❌Escoge una Opcion valida porfavor❌❌❌"
            )

            if seleccion_ataque == BACK_OPTION:
                return None

            seleccion_ataque = int(seleccion_ataque) - 1 
            selected_attack = self.CURRENTFIGHTER.getMovimiento(seleccion_ataque)

            if selected_attack.getPP() == 0:
                self.mensaje_batalla(f"❌❌❌{selected_attack.getNombre()} no se puede realizar ya que su pp es 0❌❌❌")
                continue
                
            return seleccion_ataque
            

    #OPCION DE MOCHILA
    def realizar_captura_pokemon(self, BallLanzada):
        PSmax = self.OPPONENTPOKEMON.getMps()
        PSactual = self.OPPONENTPOKEMON.getPs()
        RatioCapt = self.OPPONENTPOKEMON.getRatioDeCaptura()
        RatioPokeBall = BallLanzada.getRatio()
        BonoExt = self.OPPONENTPOKEMON.getEstado().getBonoEnCaptura()

        formulaA = (((3 * PSmax - 2 * PSactual) * RatioCapt * RatioPokeBall) / (3 * PSmax)) * BonoExt
        if formulaA >= 255:
            self.mensaje_batalla("👑👑👑capturas al pokemon👑👑👑")
            return True

        else:
            formulaB = 65535 * math.pow(formulaA / 255, 1.0 / 4.0)
            numeros = [random.randint(0, 65535) for _ in range(4)]

            temblores = 0
            for x in range(4):
                if numeros[x] <= formulaB:
                    temblores += 1
                    self.mensaje_batalla("LA PELOTA REBOTA", temblores, "VECES...")

            if temblores == 4:
                self.mensaje_batalla("👑👑👑capturas al pokemon👑👑👑")
                self.PLAYER.Adquirir_Pokemon(self.OPPONENTPOKEMON)
                return True

            self.mensaje_batalla("❌❌❌el pokemon ha escapado❌❌❌")
            return False


    #OPCION DE CAMBIO DE POKEMON
    def get_pokemon_selection(self):
        while True:
            seleccion_cambio = self.mensaje_batalla(
                f"Escoge el pokemon que deseas que salga a luchar\n{self.PLAYER.imprimir_pokemons()}\nPulsa {BACK_OPTION} para salir",
                is_input=True,
                validacion=lambda x: x == "X" or  1 <= int(x) <= self.PLAYER.getCantidadDePokemons(),
                mensaje_raise="❌❌❌Escoge un pokemon valido porfavor❌❌❌"
            )

            if seleccion_cambio == BACK_OPTION:
                return None

            seleccion_cambio = int(seleccion_cambio) - 1
            selected_pokemon = self.PLAYER.equipo_Pokemon[seleccion_cambio]
    
            if seleccion_cambio == 0:
                self.mensaje_batalla(f"❌{selected_pokemon.getNombre()} ya está luchando, selecciona otro pokemon❌")
                continue
        
            elif selected_pokemon.getEstado().getNombre() == "Debilitado😷":
                self.mensaje_batalla(f"❌❌{selected_pokemon.getNombre()} no ha podido entrar a la batalla debido a que está Debilitado❌❌")
                continue
                
            return seleccion_cambio
    

    #OPCION DE HUIR
    def attempt_escape(self):
        RANDOM_RANGE = 255
        ESCAPE_MULTIPLIER = 128
        ESCAPE_ADDITION = 30
        ESCAPE_MODULUS = 256

        calculo = (((self.CURRENTFIGHTER.getVelocidad() * ESCAPE_MULTIPLIER) / self.OPPONENTPOKEMON.getVelocidad()) + ESCAPE_ADDITION) % ESCAPE_MODULUS
        numero = random.randint(0, RANDOM_RANGE)

        if numero < calculo:
            self.mensaje_batalla("🌪️🌪️🌪️ el pokemon escapa del combate 🌪️🌪️🌪️")
            return True
        else:
            self.mensaje_batalla("no has podido escapar del combateeee")
            return False
        

    #OPCION DE REALIZAR ATAQUES
    def relizar_ataques(self, ataqueDeQuesito, ataqueDelOponente):
        sorted_pokemones = sorted([self.CURRENTFIGHTER, self.OPPONENTPOKEMON], key=lambda pokemonExm: pokemonExm.getVelocidad(), reverse=True)
        datosParaAtacar = {
            self.CURRENTFIGHTER         :[self.CURRENTFIGHTER,         ataqueDeQuesito,   self.OPPONENTPOKEMON],
            self.OPPONENTPOKEMON :[self.OPPONENTPOKEMON, ataqueDelOponente, self.CURRENTFIGHTER]
        }

        for atacante in sorted_pokemones:
            if atacante.getPs() == 0 or datosParaAtacar[atacante][1] == -1:
                continue

            puede_moverse, mensajes = atacante.getEstado().ver_si_se_puede_mover(atacante)
            self.mensaje_batalla(*mensajes)
            
            if not puede_moverse:
                self.mensaje_batalla("🧶🧶🧶Es el momento de atacar de " + atacante.getNombre() + " 🧶🧶🧶")
                self.mensaje_batalla(f"🥊🥊🥊{atacante.getNombre()} ah usado el movimiento {atacante.getMovimiento(datosParaAtacar[atacante][1]).getNombre()}🥊🥊🥊")
                mensaje_ataque = atacante.Atacar(datosParaAtacar[atacante][2], datosParaAtacar[atacante][1])
                self.mensaje_batalla(*mensaje_ataque)
                self.mensaje_batalla(f"💔💔💔los ps de {datosParaAtacar[atacante][2].getNombre()} quedan en {datosParaAtacar[atacante][2].getPs()}💔💔💔")


    #OPCION DE CAMBIO DE POKEMON
    def switch_pokemon(self, seleccion_cambio):
        MIN_POKEMON_INDEX = 0
        self.mensaje_batalla(f"🔀🔀🔀{self.PLAYER.equipo_Pokemon[MIN_POKEMON_INDEX].getNombre()} ha sido cambio_de_pokemoniado por {self.PLAYER.equipo_Pokemon[seleccion_cambio].getNombre()}🔀🔀🔀")
        self.PokemonesQueLucharon.append(self.PLAYER.equipo_Pokemon[seleccion_cambio])
        self.PLAYER.equipo_Pokemon[seleccion_cambio], self.PLAYER.equipo_Pokemon[MIN_POKEMON_INDEX] = self.PLAYER.equipo_Pokemon[MIN_POKEMON_INDEX], self.PLAYER.equipo_Pokemon[seleccion_cambio]
        self.CURRENTFIGHTER = self.PLAYER.equipo_Pokemon[MIN_POKEMON_INDEX]



    #ALGORITMO DE LA BATALLA
    def ALGORITMO_DE_LA_BATALLA(self):
        while self.CURRENTFIGHTER.getPs() > 0 and self.OPPONENTPOKEMON.getPs() > 0:
            mainSeleccion = 0
            ataqueDeQuesito = -1
            cami = True

            while cami:
                mainSeleccion = AccionCombate(
                    int(self.mensaje_batalla(
                        f"❓❓Que Deberia Hacer {self.CURRENTFIGHTER.getNombre()}❓❓:⚔1.Lucha⚔     🎒2.Mochila🎒 \n{' '*35}🧮3.Pokemon🧮   🍃4.Huida🍃",
                        is_input=True,
                        validacion=lambda x: x.isdigit() and 1 <= int(x) <= 4,
                        mensaje_raise="❌❌❌ POR FAVOR ELIGE UNA OPCIÓN VÁLIDA, POR FAVOR ❌❌❌\n"
                    ))
                )

                match mainSeleccion:
                    case AccionCombate.LUCHAR:
                        seleccion_ataque = self.get_attack_selection()
                        ataqueDeQuesito, cami = (ataqueDeQuesito, cami) if seleccion_ataque is None else (seleccion_ataque, False)



                    case AccionCombate.MOCHILA:
                        punto_control_2 = True
                        while punto_control_2:
                            objeto_sacado = self.PLAYER.getMochila().sacar_objeto()
                            
                            #no saco ningun objeto
                            if not objeto_sacado:
                                self.mensaje_batalla("(se cerro la mochila sin sacar nigun objeto)")
                                punto_control_2 = False
                                continue

                            eleccion_uso = int(self.mensaje_batalla(
                                "1.usar       2.salir(escoger otro)",
                                is_input=True,
                                validacion=lambda x: x in ['1','2'],
                                mensaje_raise="Escoge una opcion entre (1 . 2)"
                            ))
                            
                            if eleccion_uso == 2:
                                continue

                            if objeto_sacado.getTipo() == "pokéball":
                                if self.encounter_type == "ENTRENADOR":
                                    self.mensaje_batalla("no puedes capturar de un combate contra un entrenador")
                                    continue

                                capturo_pokemon = self.realizar_captura_pokemon(objeto_sacado)
                                if capturo_pokemon:
                                    return
                                
                                cami = False
                                punto_control_2 = False
                                

                            
                            objetivo = int(self.mensaje_batalla(
                                f"{self.PLAYER.imprimir_pokemons()}\n///Ah que pokemon le quieres dar la medicina",
                                is_input=True,
                                validacion=lambda x: x.isdigit() and 1 <= int(x) <= self.PLAYER.getCantidadDePokemons(),
                                mensaje_raise="escoge un pokemon valido"
                            ))-1



                            pokemon_a_sanar = self.PLAYER.equipo_Pokemon[objetivo]
                            used, messages = pokemon_a_sanar.recibir_objeto(objeto_sacado)

                            if used:
                                self.mensaje_batalla(*messages)
                                cami = False
                                punto_control_2 = False
                                break
                        
                                
    
                                    
                                    
                
                    case AccionCombate.CAMBIAR:
                        seleccion_cambio = self.get_pokemon_selection()
                        if seleccion_cambio is not None:
                            self.switch_pokemon(seleccion_cambio)



                    case AccionCombate.HUIDA:
                        if self.encounter_type == "ENTRENADOR":
                            self.mensaje_batalla("no puedes escapar de un combate contra un entrenador")
                        elif self.attempt_escape():
                            return EstadoCombate.HUIDA
                        else:
                            cami = False        


            self.relizar_ataques(ataqueDeQuesito, random.randint(0, self.OPPONENTPOKEMON.getCantidadDeMovimientos()-1))   
            self.mensaje_batalla(*self.CURRENTFIGHTER.getEstado().realizarDaño(self.CURRENTFIGHTER, self.OPPONENTPOKEMON))
            self.mensaje_batalla(*self.OPPONENTPOKEMON.getEstado().realizarDaño(self.OPPONENTPOKEMON, self.CURRENTFIGHTER))
            self.mensaje_batalla("❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃\n\n\n\n\n\n")


    #ACCIONES AL TERMINAR LA LUCHA
    def acciones_al_terminar_la_lucha(self, estado: EstadoCombate):
        if estado == EstadoCombate.VICTORIA:
            experiencia_individual = round(round((self.OPPONENTPOKEMON.getExp_Base() * self.OPPONENTPOKEMON.getNivel() * 1.5) / 7) / len(self.PokemonesQueLucharon))
            caracteristicas = {
                0:"ps", 1:"Ataque", 2:"Defensa", 3:"Velocidad", 4:"Ataque especial", 5:"Defensa especial"
            }

            for pokemon_victorioso in self.PokemonesQueLucharon:
                if pokemon_victorioso.getPs() == 0:
                    continue
                
                self.mensaje_batalla(f"""
                                     🎆🎆🎆 ¡Bien hecho, {pokemon_victorioso.getNombre()} ha ganado {experiencia_individual} puntos de experiencia! 🎆🎆🎆
                                     \n🧣🧣🧣 {pokemon_victorioso.getNombre()} ha aumentado {self.OPPONENTPOKEMON.getPuntosBlindar()[1]} puntos de esfuerzo en {caracteristicas[self.OPPONENTPOKEMON.getPuntosBlindar()[0]]} 🧣🧣🧣
                                    """)

                pokemon_victorioso.setExperiencia(experiencia_individual)
                pokemon_victorioso.setPuntosDeEzfuerzo(self.OPPONENTPOKEMON.getPuntosBlindar())

                for nivel in range(101):
                    experiencia_requerida_para_estar_en_el_nivel = pokemon_victorioso.Establecer_exp(pokemon_victorioso.getFormula(), nivel)

                    if (pokemon_victorioso.getExperiencia() >= experiencia_requerida_para_estar_en_el_nivel and pokemon_victorioso.getNivel() < nivel):
                        self.mensaje_batalla(f"📉📉📉 ¡Felicidades {pokemon_victorioso.getNombre()} ha subido al nivel {nivel}! 📉📉📉")
                        evolucion = pokemon_victorioso.setNivel(nivel)

                        if evolucion == None:
                            self.mensaje_batalla("no hay evolucion")
                            continue
                        
                        self.PLAYER.evolucionar_su_pokemon(pokemon_victorioso.n_id, evolucion)

            self.PokemonesQueLucharon.clear()



        elif estado == EstadoCombate.DERROTA:
            self.mensaje_batalla(f"{self.PLAYER.equipo_Pokemon[0].getNombre()} Se ha debilitado.")

            while True:
                cambio_de_pokemon = int(self.mensaje_batalla(
                    f"{self.PLAYER.imprimir_pokemons()}\n///Por qué Pokémon quieres cambio_de_pokemoniar a {self.PLAYER.equipo_Pokemon[0].getNombre()} para continuar la batalla: ",
                    is_input=True,
                    validacion=lambda x: x.isdigit() and 1 <= int(x) <= self.PLAYER.getCantidadDePokemons(),
                    mensaje_raise="❌❌❌ POR FAVOR ELIGE UNA OPCIÓN VÁLIDA, POR FAVOR ❌❌❌\n",
                ))-1
                if (self.PLAYER.equipo_Pokemon[cambio_de_pokemon].getPs() == 0):
                    self.mensaje_batalla("❌❌❌ ESTE POKEMON ESTA DEBILITADO POR LO QUE NO PUEDE PELEAR ❌❌❌\n")
                    continue

                break
            
            self.mensaje_batalla(f"🍂🍂🍂 {self.PLAYER.equipo_Pokemon[0].getNombre()}  se ha debilitado, {self.PLAYER.equipo_Pokemon[cambio_de_pokemon].getNombre()}  ha salido al combate 🍂🍂🍂")
            
            reserva = self.PLAYER.equipo_Pokemon[0]
            self.PLAYER.equipo_Pokemon[0] = self.PLAYER.equipo_Pokemon[cambio_de_pokemon]
            self.PLAYER.equipo_Pokemon[cambio_de_pokemon] = reserva


  

        elif estado == EstadoCombate.HUIDA:
            self.mensaje_batalla("🏃‍♂️🏃‍♂️🏃‍♂️ Has huido del combate. 🏃‍♂️🏃‍♂️🏃‍♂️")


    #VERIFICAR SI EL ENTRENADOR PUEDE SEGUIR
    def el_entrenador_puede_seguir(self, Entrenador_a_revisar):
        return any(pokemon.getPs() != 0 and pokemon.getEspecie() != "NINE" for pokemon in Entrenador_a_revisar.equipo_Pokemon)



    """
    METODOS PARA LAS BATALLAS
    """
    def LUCHA_CONTRA_ENTRENADOR(self, JUGADOR, OPONENTE):
        self.PLAYER, self.ENEMY_TRAINER, self.encounter_type = JUGADOR, OPONENTE, "ENTRENADOR",  
        while True:
            
            self.CURRENTFIGHTER = self.PLAYER.equipo_Pokemon[0]
            self.OPPONENTPOKEMON = self.ENEMY_TRAINER.equipo_Pokemon[0]
            self.PokemonesQueLucharon.append(self.CURRENTFIGHTER)
            self.mensaje_batalla(f"🍸🍸🍸 {self.ENEMY_TRAINER.getNombre()} HA SACADO A {self.ENEMY_TRAINER.equipo_Pokemon[0].getNombre()} AL COMBATE 🍸🍸🍸")

            resultado_lucha = self.ALGORITMO_DE_LA_BATALLA()
            self.acciones_al_terminar_la_lucha(resultado_lucha)

            if resultado_lucha == EstadoCombate.VICTORIA:
                self.mensaje_batalla(f"🏅FELICIDADES, HAS PODIDO DERROTAR AL {OPONENTE.equipo_Pokemon[0].getNombre()} DE {OPONENTE.getNombre()} 🏅")
                del OPONENTE.equipo_Pokemon[0]

                if not self.el_entrenador_puede_seguir(OPONENTE):
                    self.mensaje_batalla(f"""VENCISTE A  {OPONENTE.getNombre()}, Y HAS GANAS EL COMBATE Has ganado 1000 dólares por vencer.""")
                    self.PLAYER.setDinero(1000)
                    break

            elif resultado_lucha == EstadoCombate.DERROTA:
                self.mensaje_batalla(f"El {OPONENTE.equipo_Pokemon[0].getNombre()} ha vencido a tu Pokémon.")
                if not self.el_entrenador_puede_seguir(self.PLAYER):
                    self.mensaje_batalla(f"""💥💥💥El combate ya no puede continuar ya que el entrenador {self.PLAYER.getNombre()} se ha quedado sin pokemon 💥💥💥")
                                        \n🌠🌠🌠 Lo sentimos, todos tus Pokémon se han debilitado. {OPONENTE.getNombre()} ha sido el vencedor. 🌠🌠🌠")
                                        \nHas perdido 1000 dólares""")
                    self.PLAYER.setDinero(self.PLAYER.getDinero() - 1000)
                    break

                self.mensaje_batalla(f"🍂🍂🍂 {self.PLAYER.equipo_Pokemon[0].getNombre()}  se ha debilitado, {self.PLAYER.equipo_Pokemon[1].getNombre()}  ha salido al combate 🍂🍂🍂")

            elif resultado_lucha == EstadoCombate.HUIDA:
                self.mensaje_batalla("🏃‍♂️🏃‍♂️🏃‍♂️ Has huido del combate. 🏃‍♂️🏃‍♂️🏃‍♂️")
                break


    def LUCHA_CONTRA_POKEMON(self, JUGADOR, pokemonAEnfrentar):
        self.PLAYER, self.encounter_type, self.OPPONENTPOKEMON, self.CURRENTFIGHTER = JUGADOR, "SALVAJE", pokemonAEnfrentar, JUGADOR.equipo_Pokemon[0]
        self.PokemonesQueLucharon.append(self.CURRENTFIGHTER)
        self.mensaje_batalla(f"🌳🌳🌳El pokemon {pokemonAEnfrentar.getNombre()} ah salido de un arbusto🌳🌳🌳")
        self.mensaje_batalla(f"{pokemonAEnfrentar.getNombre()} está listo para luchar, tu combate contra el pokemon salvaje comienza")
        
        while True:            
            resultado = self.ALGORITMO_DE_LA_BATALLA()
            self.acciones_al_terminar_la_lucha(resultado)

            if resultado == EstadoCombate.VICTORIA: 
                self.mensaje_batalla("""
                                     ˚✧₊⁎❝ཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧          
                                     🏅🏅🏅🏅🏅🏅🏅🏅 FELICIDADES, HAS PODIDO DERROTAR AL POKEMON SALVAJE 🏅🏅🏅🏅🏅🏅🏅 
                                     ˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚
                                     """)
                return

            elif resultado == EstadoCombate.DERROTA:
                self.mensaje_batalla(f"{pokemonAEnfrentar.getNombre()} Ah vencido a tu pokemon")


            elif resultado == EstadoCombate.HUIDA:
                self.mensaje_batalla("🏃‍♂️🏃‍♂️🏃‍♂️ Has huido del combate. 🏃‍♂️🏃‍♂️🏃‍♂️")
                break


    def LUCHA_DE_DOS_POKEMONES(self, JUGADOR, pokemonAEnfrentar):
        pass



    def LUCHA_CONTRA_TRIPLES(self, JUGADOR, pokemonAEnfrentar):
        pass



    def LUCHA_CONTRA_ORDAS_POKEMONES(self, JUGADOR, *args):
        for pokemonAEnfrentar in args:
            self.PLAYER, self.encounter_type, self.OPPONENTPOKEMON, self.CURRENTFIGHTER = JUGADOR, "ORDAS", args[0], JUGADOR.equipo_Pokemon[0]
            self.PokemonesQueLucharon.append(self.CURRENTFIGHTER)
            self.mensaje_batalla(f"🌳🌳🌳El pokemon {self.OPPONENTPOKEMON.getNombre()} ah salido de un arbusto🌳🌳🌳")
            self.mensaje_batalla(f"{self.OPPONENTPOKEMON.getNombre()} está listo para luchar, tu combate contra el pokemon salvaje comienza")
            
            while True:
                self.ALGORITMO_DE_LA_BATALLA()

                if self.PLAYER.equipo_Pokemon[0].getPs() == 0:
                    self.mensaje_batalla(f"{pokemonAEnfrentar.getNombre()} Ah vencido a {self.PLAYER.equipo_Pokemon[0].getNombre()}")
                    self.acciones_al_terminar_la_lucha(True)

                else:#el jugador le gano al pokemon
                    self.mensaje_batalla("˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚            🏅🏅🏅🏅🏅🏅🏅🏅 FELICIDADES, HAS PODIDO DERROTAR AL POKEMON SALVAJE 🏅🏅🏅🏅🏅🏅🏅 ˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚")
                    
                    self.acciones_al_terminar_la_lucha(False)
                    break



    def LUCHA_CONTRA_ORDAS_ENTRENADORES(self, JUGADOR, pokemonAEnfrentar):
        self.PLAYER, self.encounter_type, self.OPPONENTPOKEMON, self.CURRENTFIGHTER = JUGADOR, "ORDAS", pokemonAEnfrentar, JUGADOR.equipo_Pokemon[0]
        self.PokemonesQueLucharon.append(self.CURRENTFIGHTER)
        self.mensaje_batalla(f"🌳🌳🌳El pokemon {pokemonAEnfrentar.getNombre()} ah salido de un arbusto🌳🌳🌳")
        self.mensaje_batalla(f"{pokemonAEnfrentar.getNombre()} está listo para luchar, tu combate contra el pokemon salvaje comienza")
        
        while True:
            self.ALGORITMO_DE_LA_BATALLA()

            if self.PLAYER.equipo_Pokemon[0].getPs() == 0:
                self.mensaje_batalla(f"{pokemonAEnfrentar.getNombre()} Ah vencido a {self.PLAYER.equipo_Pokemon[0].getNombre()}")
                self.acciones_al_terminar_la_lucha(True)

            else:
                self.mensaje_batalla("")

