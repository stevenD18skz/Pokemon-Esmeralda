from Mochila import *
from Entrenador import *
from data import mensaje_game, mensajes_exterior
#OPCION 3



class Tienda:
		"""
		Representa una tienda Pokémon donde los clientes pueden comprar y vender objetos.

		Attributes:
				nombre (str): El nombre de la tienda.
				cliente (Cliente): El cliente actual en la tienda.
				inventario (list): La lista de objetos disponibles en la tienda.

		Methods:
				mostrar_inventario():
						Muestra el inventario de la tienda.
				comprar():
						Permite al cliente comprar objetos de la tienda.
				verificar_disponibilidad(objeto, cantidad):
						Verifica si hay suficiente cantidad de un objeto en la mochila del cliente.
				vender():
						Permite al cliente vender objetos a la tienda.
				salir():
						Muestra un mensaje de despedida y finaliza la interacción.
				recibir_jugador(cliente):
						Inicializa la interacción con un nuevo cliente.
		"""

		def __init__(self):
				"""
				Inicializa una nueva instancia de la tienda Pokémon con un inventario vacío.
				"""
				self.nombre = "Tienda Pokemon"
				self.cliente = None
				self.inventario = self.cargar_inventario()


		def cargar_inventario(self):
				"""
				Carga el inventario de la tienda desde la base de datos.
				
				Returns:
						list: Lista de objetos disponibles en la tienda.
				"""
				CONSULTA_INVENTARIO = """
						SELECT nombre, precio_compra, precio_venta FROM pokeball 
						UNION 
						SELECT nombre, precio_compra, precio_venta FROM Medicina
				"""
				cursor.execute(CONSULTA_INVENTARIO)
				return cursor.fetchall()

				

		def mostrar_inventario(self):
				"""
				Muestra el inventario de la tienda con los nombres y precios de los objetos.
				"""
				print("				 🌟 Inventorio Mágico 🌟")
				print("════════════════════════════════════════════")
				for i, objeto in enumerate(self.inventario, start=1):
						print(f"🔮 {i}. {objeto[0]:<20} 💰 {objeto[1]:>5} monedas")
				print("════════════════════════════════════════════")
				print("┌────────────────────────┐")
				print(f"|	 Dinero: {self.cliente.getDinero()}	 ")
				print("└────────────────────────┘")



		def comprar(self):
				"""
				Permite al cliente comprar objetos del inventario de la tienda.
				"""
				eleccion = None
				while True:
						try:
								if eleccion is None:
									eleccion = int(mensaje_game("¿Qué producto quieres llevarte?", self.mostrar_inventario, isInput=True)) - 1 if eleccion is None else None
								if 0 <= eleccion < len(self.inventario):
										item_comprado = crearItem(self.inventario[eleccion][0])
										cantidad = int(mensaje_game(f"{self.inventario[eleccion][0]}?, buena elección\n¿Cuántas quieres llevarte?", self.mostrar_inventario, isInput=True))
										confirmacion = int(mensaje_game(f"Sería un total de {item_comprado.getPrecioCompra() * cantidad}, ¿estás seguro?\n1.Sí\n2.No", self.mostrar_inventario, isInput=True))

										if confirmacion == 1:
												if self.cliente.getDinero() >= item_comprado.getPrecioCompra() * cantidad:
														self.cliente.setDinero(self.cliente.getDinero() - item_comprado.getPrecioCompra() * cantidad)
														mensaje_game(self.cliente.getMochila().guardar_objeto(item_comprado, cantidad), self.mostrar_inventario)
												else:
														mensaje_game("No tienes suficiente dinero", self.mostrar_inventario)
										else:
												mensaje_game("Compra cancelada.", self.mostrar_inventario)
								else:
										mensaje_game("Escoge un item válido por favor", self.mostrar_inventario)
								break
						except ValueError:
								mensaje_game("Entrada no válida. Por favor, introduce un número.", self.mostrar_inventario)
				return False



		def verificar_disponibilidad(self, objeto, cantidad):
				"""
				Verifica si hay suficiente cantidad de un objeto en la mochila del cliente.

				Args:
						objeto (str): El nombre del objeto a verificar.
						cantidad (int): La cantidad del objeto a verificar.

				Returns:
						bool: True si hay suficiente cantidad, False de lo contrario.
				"""
				for item, cantidad_disponible in self.cliente.getMochila().bolsilloAbierto:
						if item == objeto:
								return cantidad_disponible >= cantidad
				return False



		def vender(self):
				"""
				Permite al cliente vender objetos a la tienda.
				"""
				objeto = self.cliente.getMochila().abrir_mochila()

				while True:
						try:
								cantidad = mensaje_game(f"¿Cuántos {objeto.getNombre()} quiere vender?\n(x para salir)", self.mostrar_inventario, isInput=True)
								if cantidad.lower() == "x":
										return False

								cantidad = int(cantidad)
								if self.verificar_disponibilidad(objeto, cantidad):
										break
								else:
										mensaje_game(f"No tienes suficientes {objeto.getNombre()} para vender", self.mostrar_inventario)
						except ValueError:
								mensaje_game("Entrada no válida. Por favor, introduce un número.", self.mostrar_inventario)

				consultar_precio = f"""
						SELECT precio_venta FROM pokeball 
						UNION 
						SELECT precio_venta FROM Medicina 
						WHERE nombre = '{objeto.getNombre()}'
				"""
				precio = cursor.execute(consultar_precio).fetchone()[0]
				oferta = precio * cantidad

				self.cliente.getMochila().tirar(objeto, cantidad)
				mensaje_game(f"Has vendido {cantidad} {objeto.getNombre()}, toma tu dinero, {oferta}$", self.mostrar_inventario)
				self.cliente.setDinero(self.cliente.getDinero() + oferta)
				return False
		


		def salir(self):
				"""
				Muestra un mensaje de despedida y finaliza la interacción.
				"""
				mensaje_game("Hasta la próxima, vuelve pronto", self.mostrar_inventario)
				return True



		def recibir_jugador(self, cliente):
				"""
				Inicializa la interacción con un nuevo cliente.

				Args:
						cliente (Cliente): El cliente que entra a la tienda.
				"""
				self.cliente = cliente
				mensaje_game(f"Bienvenido a la tienda, {cliente.getNombre()}.\n¡Podrías echar un vistazo a nuestro inventario!", self.mostrar_inventario)

				opciones = {
						1: self.comprar,
						2: self.vender,
						3: self.salir
				}

				while True:
						try:
								opcion_elegida = int(mensaje_game("¿En qué puedo ayudarte?\n1. Comprar\n2. Vender\n3. Salir", self.mostrar_inventario, isInput=True))
								if opcion_elegida in opciones and opciones[opcion_elegida]():
										return
						except ValueError:
							mensaje_game("Entrada no válida. Por favor, elige una opción válida (1, 2 o 3).", self.mostrar_inventario)
