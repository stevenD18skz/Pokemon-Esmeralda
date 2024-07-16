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

steven = Entrenadores("Steven", 100000, 15, "entrenador pokemon", Mochila(), 
                      crear_pokemon_entrenador("Sobble"), 
                      crear_pokemon_entrenador("Ivysaur"), 
                      crear_pokemon_entrenador("Bulbasaur"), 
                      crear_pokemon_entrenador("Fennekin"), 
                      crear_pokemon_entrenador("Sobble"), 
                      crear_pokemon_entrenador("Oshawott")
                      )


def main_display():
    txt = []
    txt.append("──────────────────────────────────────────────")
    txt.append("👤 Jugador: Ash      💰 Dinero: 100000      ⏰ Hora: 12:00 PM")
    txt.append("──────────────────────────────────────────────")
    txt.append("")
    txt.append("                🌳🌳🌳🌳🌳🌳🌳🌳🌳")
    txt.append("                🌳                  🌳")
    txt.append("                🌳  🏠👨           🌳")
    txt.append("                ←                       →")
    txt.append("                🌳                  🌳")
    txt.append("                🌳                  🌳")
    txt.append("                🌳🌳🌳🌳🌳🌳🌳🌳🌳")
                    
    return "\n".join(txt)
 


while True:
    eleccion = interfaz_usuario(
        f"""──────────────────────────────────────────────\n📋 Acciones:\n1. Ir al bosque     2. Luchar contra un entrenador     3. Ir a la tienda\nE. Menú             X. Salir del juego\n──────────────────────────────────────────────\n\nPresiona la tecla correspondiente para seleccionar una acción.
        """,
        display=main_display(),
        is_input=True,
        validacion=lambda x: x.lower() in ["1","2","3","e","x",],
        mensaje_raise="xxxxxxxxxxxxxxxxxxxxx"
    )


    if eleccion == "1":
        BosqueViejoPokemon().iniciar_combate_pokemon(steven)


    elif eleccion == "2":
        Lance = crear_oponente("Lance")
        figth = AlgoritmoDeBatalla()
        figth.LUCHA_CONTRA_ENTRENADOR(steven, Lance)


    elif eleccion == "3":
        store = Tienda()
        store.recibir_jugador(steven)


    elif eleccion.upper() == "E":
        while True:
            eleccion_menu = interfaz_usuario(
                f"""──────────────────────────────────────────────\n📋 Acciones:\n1.POKEDEX\n2.POKEMONS\n3.MOCHILA\n4.{steven.getNombre()}\n5.GUARDAR\n6.OPCIONES\n7.SALIR\n──────────────────────────────────────────────\n\nPresiona la tecla correspondiente para seleccionar una acción.
                """,
                display=main_display(),
                is_input=True,
                validacion=lambda x: x.lower() in ["1","2","3","4","5","6","7"],
                mensaje_raise="xxxxxxxxxxxxxxxxxxxxx"
            )
                    
            
            
            
            if eleccion_menu == "1":
                print("aun no disponible")
            if eleccion_menu == "2":
                interfaz_usuario(steven.imprimir_pokemons())
            if eleccion_menu == "3":
                steven.usar_mochila()
            if eleccion_menu == "4":
                interfaz_usuario( steven.mostrar_informacion())
            if eleccion_menu == "5":
                print("aun no disponible")
            if eleccion_menu == "6":
                print("aun no disponible")
            if eleccion_menu == "7":
                break

    elif eleccion.upper() == "X":
        break