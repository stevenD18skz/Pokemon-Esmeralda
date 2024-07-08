from Pokemon import *
from Entrenador import *
import math
import os
import time
#OPCION 3

"""
-combates dobles
-combates triples
-combate contra ordas de pokemones
-combate contra ordas de entrendoes
-combate inverso
"""
class AlgoritmoDeBatalla:
    def __init__(self):
        self.turno = 1
        self.PokemonesQueLucharon = []

        self.QUESI = None
        self.KAIDO = None
        self.PLAYER = None
        self.validacion = ""




    def establecer_formula(self, metodo, nivel):#✔✔✔
        formulas = {
            "Rapido": int((4 * nivel ** 3) / 5),
            "Medio": nivel ** 3,
            "Lento": int((5 * nivel ** 3) / 4),
            "Parabolico": int((6 * nivel ** 3) / 5 - 15 * nivel ** 2 + 100 * nivel - 140)
        }
        return formulas[metodo]





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
        os.system('cls' if os.name == 'nt' else 'clear')
        print("❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ")
        PvidaRival = round((self.KAIDO.getPs() * 100) / self.KAIDO.getMps())
        Pvida = round((self.QUESI.getPs() * 100) / self.QUESI.getMps())
        print(
            f"{self.KAIDO.getNombre()}🦅    Nv:{self.KAIDO.getNivel()}"
            f"\nPS:💙{self.barra_de_vida(self.KAIDO, 50)}💙 = {self.KAIDO.getPs()}/{self.KAIDO.getMps()} = {PvidaRival}%"
            f"\nEstado:{self.KAIDO.getEstado().getNombre()}"
            "\n\n\n\n\n\n\n"
            f"                                       {self.QUESI.getNombre()}🐣    Nv:{self.QUESI.getNivel()}"
            f"\n                                       PS:💙{self.barra_de_vida(self.QUESI, 50)}💙 = {self.QUESI.getPs()}/{self.QUESI.getMps()} = {Pvida}%"
            f"\n                                       Estado:{self.QUESI.getEstado().getNombre()}                                               EXP:{self.QUESI.getExperiencia()-(self.establecer_formula(self.QUESI.getFormula(), self.QUESI.getNivel()))}/{(self.establecer_formula(self.QUESI.getFormula(), self.QUESI.getNivel()+1)) - self.establecer_formula(self.QUESI.getFormula(), self.QUESI.getNivel())}"
            f"\n                                       {self.barra_de_pokeballs()}\n"
        )

    def mensaje_game(self, mensaje):
        self.imprimir_escenario_de_batalla()
        print(f"{mensaje}")
        time.sleep(2)

    def mensajes_exterior(self, mensajes):
        for mensaje in mensajes:
            self.mensaje_game(mensaje)
            time.sleep(2)








    def realizar_captura_pokemon(self, BallLanzada):#✔✔✔
        PSmax = self.KAIDO.getMps()
        PSactual = self.KAIDO.getPs()
        RatioCapt = self.KAIDO.getRatioDeCaptura()
        RatioPokeBall = BallLanzada.getRatio()
        BonoExt = self.KAIDO.getEstado().getBonoEnCaptura()

        formulaA = (((3 * PSmax - 2 * PSactual) * RatioCapt * RatioPokeBall) / (3 * PSmax)) * BonoExt
        if formulaA >= 255:
            print("👑👑👑capturas al pokemon👑👑👑")
            return True

        else:
            formulaB = 65535 * math.pow(formulaA / 255, 1.0 / 4.0)
            numeros = [random.randint(0, 65535) for _ in range(4)]

            temblores = 0
            for x in range(4):
                if numeros[x] <= formulaB:
                    temblores += 1
                    print("LA PELOTA REBOTA", temblores, "VECES...")

            if temblores == 4:
                print("👑👑👑capturas al pokemon👑👑👑")
                self.PLAYER.Adquirir_Pokemon(self.KAIDO)
                return True

            print("❌❌❌el pokemon ha escapado❌❌❌")
            return False



    def el_entrenador_puede_seguir(self, Entrenador_a_revisar):#✔✔✔
        pokemones_incapaces_de_pelear = 0
        for pokemon in Entrenador_a_revisar.equipo_Pokemon:
            if pokemon.getPs() == 0 or pokemon.getEspecie() == "NINE":
                pokemones_incapaces_de_pelear += 1

        if pokemones_incapaces_de_pelear != 6:
            return True

        return False
    

        #return any(pokemon.getPs() != 0 and pokemon.getEspecie() != "NINE" for pokemon in Entrenador_a_revisar.equipo_Pokemon)



    def get_attack_selection(self):
        # Define constants
        BACK_OPTION = 5
        MIN_ATTACK_INDEX = 0
        MAX_ATTACK_INDEX = 4

        while True:
            self.imprimir_escenario_de_batalla()
            print(f"⚔⚔¿que ataque deberia usar {self.QUESI.getNombre()}⚔⚔:")
            self.QUESI.mostrarAtaques()
            seleccion_ataque = int(input(f"\n{BACK_OPTION}. Atras\n⚜== ")) - 1

            if seleccion_ataque + 1 == BACK_OPTION:
                return None

            try:
                selected_attack = self.QUESI.getMovimiento(seleccion_ataque)
            except IndexError:
                self.mensaje_game("❌❌❌Escoge una Opcion valida porfavor❌❌❌")
                continue

            if selected_attack.getNombre() == "":
                self.mensaje_game("❌❌❌Escoge una Opcion valida porfavor❌❌❌")
            elif selected_attack.getPP() == 0:
                self.mensaje_game(f"{selected_attack.getNombre()} no se puede realizar ya que su pp es 0")
            else:
                return seleccion_ataque



    def get_pokemon_selection(self):
        EXIT_OPTION = 7
        MIN_POKEMON_INDEX = 0
        INVALID_POKEMON = "NINE"
        DEBILITADO = "Debilitado😷"

        while True:
            self.mensaje_game(f"Escoge el pokemon que deseas que salga a luchar\n")
            self.PLAYER.imprimir_pokemons()
            seleccion_cambio = int(input(f"Pulsa {EXIT_OPTION} para salir.\n⚜== ")) - 1

            if seleccion_cambio + 1 == EXIT_OPTION:
                return None

            try:
                selected_pokemon = self.PLAYER.equipo_Pokemon[seleccion_cambio]
            except IndexError:
                self.mensaje_game("❌❌❌Escoge un pokemon valido porfavor❌❌❌")
                continue

            if selected_pokemon.getEspecie() == INVALID_POKEMON:
                self.mensaje_game("❌❌❌Escoge un pokemon valido porfavor❌❌❌")
            elif selected_pokemon.getEstado().getNombre() == DEBILITADO:
                self.mensaje_game(f"❌❌{selected_pokemon.getNombre()} no ha podido entrar a la batalla debido a que está Debilitado❌❌")
            elif seleccion_cambio == MIN_POKEMON_INDEX:
                self.mensaje_game(f"❌{selected_pokemon.getNombre()} ya está luchando, selecciona otro pokemon❌")
            else:
                return seleccion_cambio
    



    def switch_pokemon(self, seleccion_cambio):
        MIN_POKEMON_INDEX = 0
        self.mensaje_game(f"🔀🔀🔀{self.PLAYER.equipo_Pokemon[MIN_POKEMON_INDEX].getNombre()} ha sido cambio_de_pokemoniado por {self.PLAYER.equipo_Pokemon[seleccion_cambio].getNombre()}🔀🔀🔀")
        self.PokemonesQueLucharon.append(self.PLAYER.equipo_Pokemon[seleccion_cambio])
        self.PLAYER.equipo_Pokemon[seleccion_cambio], self.PLAYER.equipo_Pokemon[MIN_POKEMON_INDEX] = self.PLAYER.equipo_Pokemon[MIN_POKEMON_INDEX], self.PLAYER.equipo_Pokemon[seleccion_cambio]
        self.QUESI = self.PLAYER.equipo_Pokemon[MIN_POKEMON_INDEX]





    def attempt_escape(self):
        RANDOM_RANGE = 255
        ESCAPE_MULTIPLIER = 128
        ESCAPE_ADDITION = 30
        ESCAPE_MODULUS = 256

        calculo = (((self.QUESI.getVelocidad() * ESCAPE_MULTIPLIER) / self.KAIDO.getVelocidad()) + ESCAPE_ADDITION) % ESCAPE_MODULUS
        numero = random.randint(0, RANDOM_RANGE)

        if numero < calculo:
            self.mensaje_game("🌪️🌪️🌪️ el pokemon escapa del combate 🌪️🌪️🌪️")
            return True
        else:
            self.mensaje_game("no has podido escapar del combateeee")
            return False





    def relizar_ataques(self, ataqueDeQuesito, ataqueDelOponente):
        sorted_pokemones = sorted([self.QUESI, self.KAIDO], key=lambda pokemonExm: pokemonExm.getVelocidad(), reverse=True)
        datosParaAtacar = {
            self.QUESI         :[self.QUESI,         ataqueDeQuesito,   self.KAIDO],
            self.KAIDO :[self.KAIDO, ataqueDelOponente, self.QUESI]
        }

        for atacante in sorted_pokemones:
            if atacante.getPs() == 0:
                break

            elif datosParaAtacar[atacante][1] == -1:
                pass #el pokemon hizo algo diferentae a atacar en el turno
            else:
                puede_moverse, mensajes = atacante.getEstado().ver_si_se_puede_mover(atacante)
                self.mensajes_exterior(mensajes)
                if puede_moverse:
                    pass
                else:
                    print("🧶🧶🧶Es el momento de atacar de " + atacante.getNombre() + " 🧶🧶🧶")
                    print(f"🥊🥊🥊{atacante.getNombre()} ah usado el movimiento {atacante.getMovimiento(datosParaAtacar[atacante][1]).getNombre()}🥊🥊🥊")
                    atacante.Atacar(datosParaAtacar[atacante][2], datosParaAtacar[atacante][1])
                    print(f"💔💔💔los ps de {datosParaAtacar[atacante][2].getNombre()} quedan en {datosParaAtacar[atacante][2].getPs()}💔💔💔")







    def ALGORITMO_DE_LA_BATALLA(self, pokemonRival):
        self.QUESI = self.PLAYER.equipo_Pokemon[0]
        self.KAIDO = pokemonRival
        self.PokemonesQueLucharon.append(self.QUESI)
        
        self.mensaje_game(f"pokemon: {self.QUESI} nivel{self.QUESI.getNivel()}, vida:{self.QUESI.getPs()}")

        while self.QUESI.getPs() > 0 and self.KAIDO.getPs() > 0:
            mainSeleccion = 0
            ataqueDeQuesito = -1
            cami = True


            while cami:
                self.imprimir_escenario_de_batalla()
                self.mensaje_game(f"❓❓Que Deberia Hacer {self.QUESI.getNombre()}❓❓:⚔1.Lucha⚔     🎒2.Mochila🎒 \n{' '*35}🧮3.Pokemon🧮   🍃4.Huida🍃")
                mainSeleccion = int(input("⚜== "))

                if mainSeleccion == 1: #✔✔✔
                    while True:
                        seleccion_ataque = self.get_attack_selection()
                        if seleccion_ataque is None:
                            break
                        else:
                            ataqueDeQuesito = seleccion_ataque
                            cami = False
                            break



                elif mainSeleccion == 2:
                    while True:
                        objeto_sacado = self.PLAYER.getMochila().abrir_mochila()
                        #no saco ningun objeto
                        if not objeto_sacado:
                            print("(se cierra la mochila)")
                            break

                        eleccion_uso = int(input("1.usar       2.salir\n=="))
                        if eleccion_uso == 1:
                            if objeto_sacado.getTipo() != "pokéball":
                                while True:
                                    self.PLAYER.imprimir_pokemons()
                                    objetivo = int(input(f"///Ah que pokemon le quieres dar la medicina\n== "))-1
                                    if (self.PLAYER.equipo_Pokemon[objetivo].getPs() == 0 or
                                        self.PLAYER.equipo_Pokemon[objetivo].getEspecie() == "NINE" or
                                        objetivo < 0 or objetivo > 5):
                                        print("❌❌❌ POR FAVOR ELIGE UNA OPCIÓN VÁLIDA, POR FAVOR ❌❌❌\n")
                                    else:
                                        break
                                
                                objeto_sacado.sanarPokemon(self.PLAYER.equipo_Pokemon[objetivo])
                                print(f"🍂🍂🍂 SE AH USADO EL OBJETOOOO 🍂🍂🍂")
                                cami = False
                                break
                                
                            else:
                                if self.validacion == "OFICIAL":
                                    self.mensaje_game("no puedes escapar de un combate contra un entrenador")
                                    break

                                if (self.realizar_captura_pokemon(objeto_sacado)):
                                    cami = False
                                    return
                                else:
                                    break
                                


                elif mainSeleccion == 3:#✔✔✔
                    while True:
                        seleccion_cambio = self.get_pokemon_selection()
                        if seleccion_cambio is None:
                            break
                        else:
                            self.switch_pokemon(seleccion_cambio)
                            break



                elif mainSeleccion == 4: #✔✔✔
                    if self.validacion == "OFICIAL":
                        self.mensaje_game("no puedes escapar de un combate contra un entrenador")
                    else:
                        if self.attempt_escape():
                            return
                        else:
                            cami = False



                else:
                    self.mensaje_game("❌❌❌ POR FAVOR ELIGE UNA OPCIÓN VÁLIDA, POR FAVOR ❌❌❌\n")


            self.relizar_ataques(ataqueDeQuesito,1)

            self.mensajes_exterior(self.QUESI.getEstado().realizarDaño(self.QUESI, self.KAIDO))
            self.mensajes_exterior(self.KAIDO.getEstado().realizarDaño(self.KAIDO, self.QUESI))
            print("❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃ႣᄎႣ❃\n\n\n\n\n\n")










    def acciones_al_terminar_la_lucha(self, verificacion):
        if verificacion:#EL JUGADOR PIERDE
            print(f"{self.PLAYER.equipo_Pokemon[0].getNombre()} Se ha debilitado.")

            while True:
                cambio_de_pokemon = int(input(f"{self.PLAYER.imprimir_pokemons()}\n///Por qué Pokémon quieres cambio_de_pokemoniar a {self.PLAYER.equipo_Pokemon[0].getNombre()} para continuar la batalla: "))-1
                if (self.PLAYER.equipo_Pokemon[cambio_de_pokemon].getPs() == 0 or
                    self.PLAYER.equipo_Pokemon[cambio_de_pokemon].getEspecie() == "NINE" or
                    cambio_de_pokemon < 0 or cambio_de_pokemon > 5):
                    print("❌❌❌ POR FAVOR ELIGE UNA OPCIÓN VÁLIDA, POR FAVOR ❌❌❌\n")
                else:
                    break
            
            print(f"🍂🍂🍂 {self.PLAYER.equipo_Pokemon[0].getNombre()}  se ha debilitado, {self.PLAYER.equipo_Pokemon[cambio_de_pokemon].getNombre()}  ha salido al combate 🍂🍂🍂")
            reserva = self.PLAYER.equipo_Pokemon[0]
            self.PLAYER.equipo_Pokemon[0] = self.PLAYER.equipo_Pokemon[cambio_de_pokemon]
            self.PLAYER.equipo_Pokemon[cambio_de_pokemon] = reserva


        else:#EL JUGADOR GANA
            experiencia_individual = round(round((self.KAIDO.getExp_Base() * self.KAIDO.getNivel() * 1.5) / 7) / len(self.PokemonesQueLucharon))
            caracteristicas = {
                0:"ps", 1:"Ataque", 2:"Defensa", 3:"Velocidad", 4:"Ataque especial", 5:"Defensa especial"
            }

            for pokemon_victorioso in self.PokemonesQueLucharon:
                if pokemon_victorioso.getPs() == 0:
                    pass
                
                else:
                    print(f"🎆🎆🎆 ¡Bien hecho, {pokemon_victorioso.getNombre()} ha ganado {experiencia_individual} puntos de experiencia! 🎆🎆🎆\n🧣🧣🧣 {pokemon_victorioso.getNombre()} ha aumentado {self.KAIDO.getPuntosBlindar()[1]} puntos de esfuerzo en {caracteristicas[self.KAIDO.getPuntosBlindar()[0]]} 🧣🧣🧣")

                    pokemon_victorioso.setExperiencia(experiencia_individual)
                    pokemon_victorioso.setPuntosDeEzfuerzo(self.KAIDO.getPuntosBlindar())

                    for nivel in range(101):
                        experiencia_requerida_para_estar_en_el_nivel = self.establecer_formula(pokemon_victorioso.getFormula(), nivel)

                        if (pokemon_victorioso.getExperiencia() >= experiencia_requerida_para_estar_en_el_nivel and pokemon_victorioso.getNivel() < nivel):
                            print(f"📉📉📉 ¡Felicidades {pokemon_victorioso.getNombre()} ha subido al nivel {nivel}! 📉📉📉")
                            evolucion = pokemon_victorioso.setNivel(nivel)

                            if evolucion == None:
                                print("no hay evolucion")
                            
                            else:
                                self.PLAYER.evolucionar_su_pokemon(pokemon_victorioso.n_id, evolucion)

            self.PokemonesQueLucharon.clear()






    def LUCHA_CONTRA_ENTRENADOR(self, JUGADOR, OPONENTE):
        self.PLAYER, self.validacion = JUGADOR, "OFICIAL",  
        while True: #self.el_entrenador_puede_seguir(self.PLAYER) and self.el_entrenador_puede_seguir(OPONENTE):
            print(f"🍸🍸🍸 {OPONENTE.getNombre()} HA SACADO A {OPONENTE.equipo_Pokemon[0].getNombre()} AL COMBATE 🍸🍸🍸")
            self.ALGORITMO_DE_LA_BATALLA(OPONENTE.equipo_Pokemon[0])

            #ALGUNO DE LOS ENTRENADORES YA NO PUEDE SEGUIR
            if not self.el_entrenador_puede_seguir(self.PLAYER) or not self.el_entrenador_puede_seguir(OPONENTE):
                break

            #EL POKEMON DEL JUGADOR PERDIO PERO AUN SIGUE EL COMBATE
            if self.PLAYER.equipo_Pokemon[0].getPs() == 0:
                print(f"El {OPONENTE.equipo_Pokemon[0].getNombre()} ha vencido a tu Pokémon.")
                self.acciones_al_terminar_la_lucha(True)

            #EL POKEMON DEL RIVAL PERDIO
            else:
                print(f"🏅🏅🏅🏅🏅🏅🏅🏅 FELICIDADES, HAS PODIDO DERROTAR AL {OPONENTE.equipo_Pokemon[0].getNombre()} DE {OPONENTE.getNombre()} 🏅🏅🏅🏅🏅🏅🏅")
                self.acciones_al_terminar_la_lucha(False)
                del OPONENTE.equipo_Pokemon[0]



        if not self.el_entrenador_puede_seguir(self.PLAYER):
            print(f"💥💥💥El combate ya no puede continuar ya que el entrenador {self.PLAYER.getNombre()} se ha quedado sin pokemon 💥💥💥")
            print(f"🌠🌠🌠 Lo sentimos, todos tus Pokémon se han debilitado. {OPONENTE.getNombre()} ha sido el vencedor. 🌠🌠🌠")
            print(f"Has perdido 1000 dólares")
            self.PLAYER.setDinero(self.PLAYER.getDinero() - 1000)
            return

        elif not self.el_entrenador_puede_seguir(OPONENTE):
            print("˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚")
            print(f"✨✨✨✨✨ FELICIDADES {self.PLAYER.getNombre()}, HAS LOGRADO VENCER A {OPONENTE.getNombre()}, Y HAS GANADO EL COMBATE ✨✨✨✨✨")
            print("˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚")
            print(f"Has ganado 1000 dólares por vencer.")
            self.PLAYER.setDinero(850)
            return


    def LUCHA_CONTRA_POKEMON(self, JUGADOR, pokemonAEnfrentar):
        self.PLAYER, self.validacion, self.KAIDO, self.QUESI = JUGADOR, "SALVAJE", pokemonAEnfrentar, JUGADOR.equipo_Pokemon[0]
        self.PokemonesQueLucharon.append(self.QUESI)
        self.mensaje_game(f"🌳🌳🌳El pokemon {pokemonAEnfrentar.getNombre()} ah salido de un arbusto🌳🌳🌳")
        self.mensaje_game(f"{pokemonAEnfrentar.getNombre()} está listo para luchar, tu combate contra el pokemon salvaje comienza")
        while True: #self.el_entrenador_puede_seguir(self.PLAYER) and pokemonAEnfrentar.getPs() != 0:
            self.ALGORITMO_DE_LA_BATALLA(pokemonAEnfrentar)

            if self.PLAYER.equipo_Pokemon[0].getPs() == 0:
                print(f"{pokemonAEnfrentar.getNombre()} Ah vencido a {self.PLAYER.equipo_Pokemon[0].getNombre()}")
                self.acciones_al_terminar_la_lucha(True)

            else:#el self.PLAYER le gano al pokemon
                print("˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚")
                print("           🏅🏅🏅🏅🏅🏅🏅🏅 FELICIDADES, HAS PODIDO DERROTAR AL POKEMON SALVAJE 🏅🏅🏅🏅🏅🏅🏅")
                print("˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚˚✧₊⁎❝ົཽ≀ˍ̮ຽ⁎⁺˳✧༚༚\n")
                self.acciones_al_terminar_la_lucha(False)
                return