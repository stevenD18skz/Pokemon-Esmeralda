from Pokemon import *
from Entrenador import *
import math
import os
import time
from data import interfaz_usuario
from enum import Enum



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

        self.QUESI = None
        self.KAIDO = None
        self.PLAYER = None
        self.validacion = ""



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

    

    def barra_de_pokeballs(self):#⭕🔴⚪⚫✔✔✔
        barra = ""
        for pokemon in self.PLAYER.equipo_Pokemon:
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
        PvidaRival = round((self.KAIDO.getPs() * 100) / self.KAIDO.getMps())
        Pvida = round((self.QUESI.getPs() * 100) / self.QUESI.getMps())
        txt.append(
            f"{self.KAIDO.getNombre()}🦅    Nv:{self.KAIDO.getNivel()}"
            f"\nPS:💙{self.barra_de_vida(self.KAIDO, 50)}💙 = {self.KAIDO.getPs()}/{self.KAIDO.getMps()} = {PvidaRival}%"
            f"\nEstado:{self.KAIDO.getEstado().getNombre()}"
            "\n\n\n\n\n\n\n"
            f"                                       {self.QUESI.getNombre()}🐣    Nv:{self.QUESI.getNivel()}"
            f"\n                                       PS:💙{self.barra_de_vida(self.QUESI, 50)}💙 = {self.QUESI.getPs()}/{self.QUESI.getMps()} = {Pvida}%"
            f"\n                                       Estado:{self.QUESI.getEstado().getNombre()}                                               EXP:{self.QUESI.getExperiencia()-(self.QUESI.Establecer_exp(self.QUESI.getFormula(), self.QUESI.getNivel()))}/{(self.QUESI.Establecer_exp(self.QUESI.getFormula(), self.QUESI.getNivel()+1)) - self.QUESI.Establecer_exp(self.QUESI.getFormula(), self.QUESI.getNivel())}"
            f"\n                                       {self.barra_de_pokeballs()}\n"
        )
        return '\n'.join(txt)




    #OPCION DE ATACAR
    def get_attack_selection(self):
        # Define constants
        BACK_OPTION = "x"

        while True:
            seleccion_ataque = self.mensaje_batalla(
                f"⚔⚔¿que ataque deberia usar {self.QUESI.getNombre()}⚔⚔:\n {self.QUESI.mostrarAtaques()}\n{BACK_OPTION}. Atras",
                is_input=True,
                validacion=lambda x: x in ["1","2","3","4","x"],
                mensaje_raise="❌❌❌Escoge una Opcion valida porfavor❌❌❌"
            )

            if seleccion_ataque.lower() == "x":
                return None

            seleccion_ataque = int(seleccion_ataque) - 1 
            selected_attack = self.QUESI.getMovimiento(seleccion_ataque)

            if selected_attack.getNombre() == "":
                self.mensaje_batalla("❌❌❌Escoge un ataque valido❌❌❌", )
            
            elif selected_attack.getPP() == 0:
                self.mensaje_batalla(f"❌❌❌{selected_attack.getNombre()} no se puede realizar ya que su pp es 0❌❌❌")
                
            else:
                return seleccion_ataque
            

    #OPCION DE MOCHILA
    def realizar_captura_pokemon(self, BallLanzada):
        PSmax = self.KAIDO.getMps()
        PSactual = self.KAIDO.getPs()
        RatioCapt = self.KAIDO.getRatioDeCaptura()
        RatioPokeBall = BallLanzada.getRatio()
        BonoExt = self.KAIDO.getEstado().getBonoEnCaptura()

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
                self.PLAYER.Adquirir_Pokemon(self.KAIDO)
                return True

            self.mensaje_batalla("❌❌❌el pokemon ha escapado❌❌❌")
            return False


    #OPCION DE CAMBIO DE POKEMON
    def get_pokemon_selection(self):
        EXIT_OPTION = "x"
        MIN_POKEMON_INDEX = 0
        INVALID_POKEMON = "NINE"
        DEBILITADO = "Debilitado😷"

        while True:
            seleccion_cambio = self.mensaje_batalla(
                f"Escoge el pokemon que deseas que salga a luchar\n{self.PLAYER.imprimir_pokemons()}\nPulsa {EXIT_OPTION} para salir",
                is_input=True,
                validacion=lambda x: x.lower() == "x" or (x.isdigit() and 1 <= int(x) <= 6),
                mensaje_raise="❌❌❌Escoge un pokemon valido porfavor❌❌❌"
            )

            if seleccion_cambio.lower() == EXIT_OPTION:
                return None


            seleccion_cambio = int(seleccion_cambio) - 1
            selected_pokemon = self.PLAYER.equipo_Pokemon[seleccion_cambio]

            if selected_pokemon.getEspecie() == INVALID_POKEMON:
                self.mensaje_batalla(f"❌❌❌Escoge un pokemon valido porfavor❌❌❌")
                
            elif selected_pokemon.getEstado().getNombre() == DEBILITADO:
                self.mensaje_batalla(f"❌❌{selected_pokemon.getNombre()} no ha podido entrar a la batalla debido a que está Debilitado❌❌")
                
            elif seleccion_cambio == MIN_POKEMON_INDEX:
                self.mensaje_batalla(f"❌{selected_pokemon.getNombre()} ya está luchando, selecciona otro pokemon❌")
                
            else:
                return seleccion_cambio
    


    #OPCION DE POKEMON
    def switch_pokemon(self, seleccion_cambio):
        MIN_POKEMON_INDEX = 0
        self.mensaje_batalla(f"🔀🔀🔀{self.PLAYER.equipo_Pokemon[MIN_POKEMON_INDEX].getNombre()} ha sido cambio_de_pokemoniado por {self.PLAYER.equipo_Pokemon[seleccion_cambio].getNombre()}🔀🔀🔀")
        self.PokemonesQueLucharon.append(self.PLAYER.equipo_Pokemon[seleccion_cambio])
        self.PLAYER.equipo_Pokemon[seleccion_cambio], self.PLAYER.equipo_Pokemon[MIN_POKEMON_INDEX] = self.PLAYER.equipo_Pokemon[MIN_POKEMON_INDEX], self.PLAYER.equipo_Pokemon[seleccion_cambio]
        self.QUESI = self.PLAYER.equipo_Pokemon[MIN_POKEMON_INDEX]



    #OPCION DE HUIR
    def attempt_escape(self):
        RANDOM_RANGE = 255
        ESCAPE_MULTIPLIER = 128
        ESCAPE_ADDITION = 30
        ESCAPE_MODULUS = 256

        calculo = (((self.QUESI.getVelocidad() * ESCAPE_MULTIPLIER) / self.KAIDO.getVelocidad()) + ESCAPE_ADDITION) % ESCAPE_MODULUS
        numero = random.randint(0, RANDOM_RANGE)

        if numero < calculo:
            self.mensaje_batalla("🌪️🌪️🌪️ el pokemon escapa del combate 🌪️🌪️🌪️")
            return True
        else:
            self.mensaje_batalla("no has podido escapar del combateeee")
            return False
        


    def relizar_ataques(self, ataqueDeQuesito, ataqueDelOponente):
        sorted_pokemones = sorted([self.QUESI, self.KAIDO], key=lambda pokemonExm: pokemonExm.getVelocidad(), reverse=True)
        datosParaAtacar = {
            self.QUESI         :[self.QUESI,         ataqueDeQuesito,   self.KAIDO],
            self.KAIDO :[self.KAIDO, ataqueDelOponente, self.QUESI]
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


    


    def ALGORITMO_DE_LA_BATALLA(self, pokemonRival):
        self.QUESI = self.PLAYER.equipo_Pokemon[0]
        self.KAIDO = pokemonRival
        self.PokemonesQueLucharon.append(self.QUESI)

        while self.QUESI.getPs() > 0 and self.KAIDO.getPs() > 0:
            mainSeleccion = 0
            ataqueDeQuesito = -1
            cami = True


            while cami:
                mainSeleccion = AccionCombate(
                    int(self.mensaje_batalla(
                        f"❓❓Que Deberia Hacer {self.QUESI.getNombre()}❓❓:⚔1.Lucha⚔     🎒2.Mochila🎒 \n{' '*35}🧮3.Pokemon🧮   🍃4.Huida🍃",
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
                                self.mensaje_batalla("(se cerro la mochila)")
                                break

                            eleccion_uso = int(self.mensaje_batalla(
                                "1.usar       2.salir",
                                is_input=True,
                                validacion=lambda x: x in ['1','2'],
                                mensaje_raise="Escoge una opcion entre (1 . 2)"
                            ))
                            
                            if eleccion_uso == 2:
                                continue
                            
                            
                            if objeto_sacado.getTipo() != "pokéball":
                                while True:
                                    objetivo = int(self.mensaje_batalla(
                                        f"{self.PLAYER.imprimir_pokemons()}\n///Ah que pokemon le quieres dar la medicina",
                                        is_input=True,
                                        validacion=lambda x: x.isdigit() and 1 <= int(x) <= 6,
                                        mensaje_raise="escoge un pokemon valido"
                                    ))-1
                                    
                                    
                                    if (self.PLAYER.equipo_Pokemon[objetivo].getPs() == 0 or
                                        self.PLAYER.equipo_Pokemon[objetivo].getEspecie() == "NINE"
                                        ):
                                        self.mensaje_batalla("❌❌❌ POR FAVOR ELIGE UNA OPCIÓN VÁLIDA, POR FAVOR ❌❌❌\n")
                                        continue
                                    
                                    break

                                pokemon_a_sanar = self.PLAYER.equipo_Pokemon[objetivo]
                                
                                used, message = pokemon_a_sanar.recibir_objeto(objeto_sacado)
                                
                                if used:
                                    self.mensaje_batalla(*message)
                                    cami = False
                                    punto_control_2 = False
                                    break
                            
                                
                            else:
                                if self.validacion == "OFICIAL":
                                    self.mensaje_batalla("no puedes capturar de un combate contra un entrenador")
                                    continue

                                if self.realizar_captura_pokemon(objeto_sacado):
                                    return
                                
                                break
                                    
                                    
                
                    case AccionCombate.CAMBIAR:
                        seleccion_cambio = self.get_pokemon_selection()
                        if seleccion_cambio is not None:
                            self.switch_pokemon(seleccion_cambio)



                    case AccionCombate.HUIDA:
                        if self.validacion == "OFICIAL":
                            self.mensaje_batalla("no puedes escapar de un combate contra un entrenador")
                        elif self.attempt_escape():
                            return EstadoCombate.HUIDA
                        else:
                            cami = False        


            self.relizar_ataques(ataqueDeQuesito, random.randint(0, self.KAIDO.getCantidadDeMovimientos()-1))   
            self.mensaje_batalla(*self.QUESI.getEstado().realizarDaño(self.QUESI, self.KAIDO))
            self.mensaje_batalla(*self.KAIDO.getEstado().realizarDaño(self.KAIDO, self.QUESI))
            self.mensaje_batalla("❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃\n\n\n\n\n\n")




    def acciones_al_terminar_la_lucha(self, estado: EstadoCombate):
        if estado == EstadoCombate.VICTORIA:
            experiencia_individual = round(round((self.KAIDO.getExp_Base() * self.KAIDO.getNivel() * 1.5) / 7) / len(self.PokemonesQueLucharon))
            caracteristicas = {
                0:"ps", 1:"Ataque", 2:"Defensa", 3:"Velocidad", 4:"Ataque especial", 5:"Defensa especial"
            }

            for pokemon_victorioso in self.PokemonesQueLucharon:
                if pokemon_victorioso.getPs() == 0:
                    continue
                
                self.mensaje_batalla(f"""
                                     🎆🎆🎆 ¡Bien hecho, {pokemon_victorioso.getNombre()} ha ganado {experiencia_individual} puntos de experiencia! 🎆🎆🎆
                                     \n🧣🧣🧣 {pokemon_victorioso.getNombre()} ha aumentado {self.KAIDO.getPuntosBlindar()[1]} puntos de esfuerzo en {caracteristicas[self.KAIDO.getPuntosBlindar()[0]]} 🧣🧣🧣
                                    """)

                pokemon_victorioso.setExperiencia(experiencia_individual)
                pokemon_victorioso.setPuntosDeEzfuerzo(self.KAIDO.getPuntosBlindar())

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



    def el_entrenador_puede_seguir(self, Entrenador_a_revisar):
        return any(pokemon.getPs() != 0 and pokemon.getEspecie() != "NINE" for pokemon in Entrenador_a_revisar.equipo_Pokemon)






    #OPCION DE LUCHA
    def LUCHA_CONTRA_ENTRENADOR(self, JUGADOR, OPONENTE):
        self.PLAYER, self.validacion = JUGADOR, "OFICIAL",  
        while True: #self.el_entrenador_puede_seguir(self.PLAYER) and self.el_entrenador_puede_seguir(OPONENTE):
            self.mensaje_batalla(f"🍸🍸🍸 {OPONENTE.getNombre()} HA SACADO A {OPONENTE.equipo_Pokemon[0].getNombre()} AL COMBATE 🍸🍸🍸")

            resultado = self.ALGORITMO_DE_LA_BATALLA(OPONENTE.equipo_Pokemon[0])
            self.acciones_al_terminar_la_lucha(resultado)

            if resultado == EstadoCombate.VICTORIA:
                self.mensaje_batalla(f"🏅🏅🏅🏅🏅🏅🏅🏅 FELICIDADES, HAS PODIDO DERROTAR AL {OPONENTE.equipo_Pokemon[0].getNombre()} DE {OPONENTE.getNombre()} 🏅🏅🏅🏅🏅🏅🏅")
                del OPONENTE.equipo_Pokemon[0]

                if not self.el_entrenador_puede_seguir(OPONENTE):
                    self.mensaje_batalla(f"""˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚ 
                                        \n✨✨✨✨✨ FELICIDADES {self.PLAYER.getNombre()}, HAS LOGRADO VENCER A {OPONENTE.getNombre()}, Y HAS GANADO EL COMBATE ✨✨✨✨✨ 
                                        \n˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚")
                                        \nHas ganado 1000 dólares por vencer.""")
                    self.PLAYER.setDinero(1000)
                    break

            elif resultado == EstadoCombate.DERROTA:
                self.mensaje_batalla(f"El {OPONENTE.equipo_Pokemon[0].getNombre()} ha vencido a tu Pokémon.")
                if not self.el_entrenador_puede_seguir(self.PLAYER):
                    self.mensaje_batalla(f"""💥💥💥El combate ya no puede continuar ya que el entrenador {self.PLAYER.getNombre()} se ha quedado sin pokemon 💥💥💥")
                                        \n🌠🌠🌠 Lo sentimos, todos tus Pokémon se han debilitado. {OPONENTE.getNombre()} ha sido el vencedor. 🌠🌠🌠")
                                        \nHas perdido 1000 dólares""")
                    self.PLAYER.setDinero(self.PLAYER.getDinero() - 1000)
                    break

                self.mensaje_batalla(f"🍂🍂🍂 {self.PLAYER.equipo_Pokemon[0].getNombre()}  se ha debilitado, {self.PLAYER.equipo_Pokemon[1].getNombre()}  ha salido al combate 🍂🍂🍂")

            elif resultado == EstadoCombate.HUIDA:
                self.mensaje_batalla("🏃‍♂️🏃‍♂️🏃‍♂️ Has huido del combate. 🏃‍♂️🏃‍♂️🏃‍♂️")
                break



    def LUCHA_CONTRA_POKEMON(self, JUGADOR, pokemonAEnfrentar):
        self.PLAYER, self.validacion, self.KAIDO, self.QUESI = JUGADOR, "SALVAJE", pokemonAEnfrentar, JUGADOR.equipo_Pokemon[0]
        self.PokemonesQueLucharon.append(self.QUESI)
        self.mensaje_batalla(f"🌳🌳🌳El pokemon {pokemonAEnfrentar.getNombre()} ah salido de un arbusto🌳🌳🌳")
        self.mensaje_batalla(f"{pokemonAEnfrentar.getNombre()} está listo para luchar, tu combate contra el pokemon salvaje comienza")
        
        while True:            
            resultado = self.ALGORITMO_DE_LA_BATALLA(pokemonAEnfrentar)
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
            self.PLAYER, self.validacion, self.KAIDO, self.QUESI = JUGADOR, "ORDAS", args[0], JUGADOR.equipo_Pokemon[0]
            self.PokemonesQueLucharon.append(self.QUESI)
            self.mensaje_batalla(f"🌳🌳🌳El pokemon {self.KAIDO.getNombre()} ah salido de un arbusto🌳🌳🌳")
            self.mensaje_batalla(f"{self.KAIDO.getNombre()} está listo para luchar, tu combate contra el pokemon salvaje comienza")
            
            while True:
                self.ALGORITMO_DE_LA_BATALLA(pokemonAEnfrentar)

                if self.PLAYER.equipo_Pokemon[0].getPs() == 0:
                    self.mensaje_batalla(f"{pokemonAEnfrentar.getNombre()} Ah vencido a {self.PLAYER.equipo_Pokemon[0].getNombre()}")
                    self.acciones_al_terminar_la_lucha(True)

                else:#el jugador le gano al pokemon
                    self.mensaje_batalla("˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚            🏅🏅🏅🏅🏅🏅🏅🏅 FELICIDADES, HAS PODIDO DERROTAR AL POKEMON SALVAJE 🏅🏅🏅🏅🏅🏅🏅 ˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚")
                    
                    self.acciones_al_terminar_la_lucha(False)
                    break



    def LUCHA_CONTRA_ORDAS_ENTRENADORES(self, JUGADOR, pokemonAEnfrentar):
        self.PLAYER, self.validacion, self.KAIDO, self.QUESI = JUGADOR, "ORDAS", pokemonAEnfrentar, JUGADOR.equipo_Pokemon[0]
        self.PokemonesQueLucharon.append(self.QUESI)
        self.mensaje_batalla(f"🌳🌳🌳El pokemon {pokemonAEnfrentar.getNombre()} ah salido de un arbusto🌳🌳🌳")
        self.mensaje_batalla(f"{pokemonAEnfrentar.getNombre()} está listo para luchar, tu combate contra el pokemon salvaje comienza")
        
        while True:
            self.ALGORITMO_DE_LA_BATALLA(pokemonAEnfrentar)

            if self.PLAYER.equipo_Pokemon[0].getPs() == 0:
                self.mensaje_batalla(f"{pokemonAEnfrentar.getNombre()} Ah vencido a {self.PLAYER.equipo_Pokemon[0].getNombre()}")
                self.acciones_al_terminar_la_lucha(True)

            else:
                self.mensaje_batalla("")

