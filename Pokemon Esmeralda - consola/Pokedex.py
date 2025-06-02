from data import *      # Se asume que aquí están las instancias de datos necesarias
from Pokemon import *   # Se asume que tu clase Pokemon define atributos como nombre, tipo, nivel, descripción, stats, habilidades...
from data import interfaz_usuario  # Ajusta la ruta si tu función se llama/interpreta distinto

class Pokedex:
    def __init__(self):
        """
        Inicializa una Pokédex vacía. 
        - self.pokemon: lista de objetos Pokemon agregados (vistos).
        - self.pokemon_vistos: conjunto de nombres para evitar duplicados.
        """
        consulta = "SELECT nombre FROM pokemon"  # Cambia el ID según lo que necesites
        datos_del_pokemon = cursor.execute(consulta).fetchall()
        print(datos_del_pokemon)

        self.pokemon = [self.crear_pokemon_pokedex(p) for p in 
                        ['Bulbasaur', 'Ivysaur', 'Chikorita', 'Treecko', 'Turtwig', 'Snivy', 'Rowlet', 'Squirtle', 'Totodile', 'Mudkip', 'Piplup', 'Oshawott', 'Popplio', 'Charmander', 'Cyndaquil', 'Torchic', 'Chimchar', 'Tepig', 'Litten', 'Chespin', 'Fennekin', 'Froakie', 'Grookey', 'Scorbunny', 'Sobble', 'Dragonite', 'Gyarados', 'Charizard', 'Dragonair', 'Salamence', 'Garchomp']
                        ]
        self.pokemon_vistos = set(['Bulbasaur', 'Chikorita', 'Turtwig'])

        self.focus_index = 0
        self.visible_index = 0
        self.max_visible_index = 10
        self.max_per_page = 10  


    def crear_pokemon_pokedex(self, nombrePokemon, nivel=50):
        consulta = "SELECT * FROM pokemon WHERE nombre = '" + nombrePokemon + "'"
        datos_del_pokemon = cursor.execute(consulta).fetchall()[0]
        pokemon_creado = Pokemon(*datos_del_pokemon[1:15],*[None, None, None, None], nivel)
        return pokemon_creado



    def agregar_pokemon(self, pokemon_obj):
        """
        Agrega un objeto Pokemon a la Pokédex, si no estaba ya agregado.
        - pokemon_obj debe ser una instancia de tu clase Pokemon.
        """
        if pokemon_obj.nombre not in self.pokemon_vistos:
            self.pokemon.append(pokemon_obj)
            self.pokemon_vistos.add(pokemon_obj.nombre)



    def construir_display_lista(self):
        """
        Construye el texto que se mostrará en la pantalla principal de la Pokédex:
        - Un encabezado (por ejemplo "📒 Tu Pokédex")
        - La lista de Pokémon (índice, nombre, tipo y nivel)
        - Una pequeña instrucción al pie con la tecla para salir
        """
        líneas = []
        líneas.append(f"visibles: {self.visible_index} - {self.max_visible_index} pk {len(self.pokemon)}\n")
        líneas.append(f"foco: {self.focus_index}\n")
        líneas.append("📒─── TU POKÉDEX ───📒\n")
        líneas.append("  Índice | Nombre               | Tipo         | Nivel\n")
        líneas.append("───────────────────────────────────────────────────────────\n")

        if not self.pokemon:
            líneas.append("  (Aún no has agregado ningún Pokémon.)\n")
        else:
            indice = self.visible_index + 1
            for  p in self.pokemon[self.visible_index:self.max_visible_index]:
                # Nombre alineado a 20 caracteres, tipo a 12, nivel a 3
                focus = "👉" if self.focus_index == indice - 1 else "  "
                nombre = p.nombre[:20].ljust(20)
                # Si tu clase Pokemon tuviese dos tipos, podrías hacer: f"{p.tipo1}/{p.tipo2}"
                tipo = getattr(p, "tipo", "?")  # Si no existe atributo "tipo", se pone "?"
                tipo = str(tipo)[:12].ljust(12)
                nivel = str(getattr(p, "nivel", "?")).rjust(3)
                estatus = "🎃" if p.nombre in self.pokemon_vistos else "👻"  # Emoji de visto

                líneas.append(f"{focus} {indice:>2}    | {nombre} | {tipo} | {nivel} {estatus} \n")
                
                indice += 1

        líneas.append("\nPulsa el número del Pokémon para ver detalles.\n")
        líneas.append("O pulsa 'x' para salir de la Pokédex.\n")
        return "".join(líneas)



    def ver_detalles(self, pokemon_obj):
        """
        Muestra en consola todos los atributos del objeto pokemon_obj.
        Utiliza introspección para mostrar cualquier campo que tenga la clase Pokemon.
        """
        líneas = []
        líneas.append(f"🔍── Detalles de {pokemon_obj.nombre} ──🔍\n\n")

        # Atributos “básicos” (si existen):
        if hasattr(pokemon_obj, "nombre"):
            líneas.append(f"Nombre      : {pokemon_obj.nombre}\n")
        if hasattr(pokemon_obj, "numero"):
            líneas.append(f"Número      : {pokemon_obj.numero}\n")
        # Si tienes separados tipo1 / tipo2:
        if hasattr(pokemon_obj, "tipo"):
            líneas.append(f"Tipo(s)     : {pokemon_obj.tipo}\n")
        if hasattr(pokemon_obj, "nivel"):
            líneas.append(f"Nivel       : {pokemon_obj.nivel}\n")
        if hasattr(pokemon_obj, "descripcion"):
            líneas.append(f"Descripción : {pokemon_obj.descripcion}\n")

        # Estadísticas: si tu clase usa un diccionario stats
        if hasattr(pokemon_obj, "stats") and isinstance(pokemon_obj.stats, dict):
            líneas.append("\nEstadísticas:\n")
            for clave, valor in pokemon_obj.stats.items():
                líneas.append(f"  • {clave.capitalize():<10}: {valor}\n")

        # Habilidades / Movimientos: si tu clase lo define como lista
        if hasattr(pokemon_obj, "habilidades") and isinstance(pokemon_obj.habilidades, (list, tuple)):
            líneas.append("\nHabilidades:\n")
            for hab in pokemon_obj.habilidades:
                líneas.append(f"  - {hab}\n")

        if hasattr(pokemon_obj, "movimientos") and isinstance(pokemon_obj.movimientos, (list, tuple)):
            líneas.append("\nMovimientos:\n")
            for mv in pokemon_obj.movimientos:
                líneas.append(f"  - {mv}\n")

        # Cualquier otro atributo que pudiera interesar:
        # (Por ejemplo: peso, altura, especie…)
        extras = []
        for attr, val in pokemon_obj.__dict__.items():
            if attr in ("nombre", "numero", "tipo", "nivel", "descripcion", "stats", "habilidades", "movimientos"):
                continue
            extras.append((attr, val))

        if extras:
            líneas.append("\nAtributos adicionales:\n")
            for attr, val in extras:
                líneas.append(f"  • {attr} = {val}\n")

        líneas.append("\n(Pulsa cualquier tecla para volver a la lista)\n")
        texto_detalle = "".join(líneas)

        # Mostramos el detalle, y esperamos a que pulse algo para regresar
        interfaz_usuario(texto_detalle, is_input=False)



    def iniciar_interfaz(self):
        """
        Loop principal de la Pokédex. Muestra la lista y permite:
         - Pulsar 'x' para salir.
         - Pulsar '1'...'9' (u otro dígito) para ver detalles de ese Pokémon.
         - Si la validación falla (p.ej. número fuera de rango), se repite el menú.
        """
        while True:
            # 1) Construimos la pantalla con la lista de Pokémon
            sel = interfaz_usuario(
                "¿Qué quieres hacer?",
                display=self.construir_display_lista(),
                is_input=True,
                validacion=lambda x: x.upper() in ["X", "W", "S", "E"],
                mensaje_raise="Por favor, pulsa una opcion valida o 'x' para salir."
            )

            # Salimos de la Pokédex
            if sel == "x":
                break

            # Si no es 'x', es un dígito
            direction = {
                'W': -1,  # Mover hacia arriba
                'S': 1,   # Mover hacia abajo
            }

            # Lo marcamos como “visto” (en realidad ya debe estar en la lista),
            # y mostramos detalles
            if sel == "E":
                pokemon_elegido = self.pokemon[self.focus_index]
                self.ver_detalles(pokemon_elegido)


            
            else:
                self.focus_index = min(max(0, self.focus_index + direction.get(sel, 0)), len(self.pokemon) - 1)

                if sel == "S":
                    self.max_visible_index = max(self.max_visible_index,  self.focus_index + 1)
                    self.visible_index = self.max_visible_index - self.max_per_page
                
                elif sel == "W":    
                    self.visible_index = min(self.visible_index,  self.focus_index - 1)
                    self.max_visible_index = self.visible_index + self.max_per_page


        return

