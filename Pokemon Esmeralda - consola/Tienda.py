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
				Devuelve una cadena con el inventario de la tienda con los nombres y precios de los objetos.
				"""
				inventario_str = "					 🌟 Inventorio Mágico 🌟\n"
				inventario_str += "════════════════════════════════════════════\n"
				for i, objeto in enumerate(self.inventario, start=1):
						inventario_str += f"🔮 {i}. {objeto[0]:<20} 💰 {objeto[1]:>5} monedas\n"
				inventario_str += "════════════════════════════════════════════\n"
				inventario_str += "┌────────────────────────┐\n"
				inventario_str += f"|    Dinero: {self.cliente.getDinero()}    \n"
				inventario_str += "└────────────────────────┘\n"
				return inventario_str



		def comprar(self):
				def elegir_producto():
						mensaje = f"¿Qué producto quieres llevarte?\n(x para salir)"
						eleccion = mensaje_game(
								mensaje=mensaje, 
								display=self.mostrar_inventario(),
								is_input=True,
								validacion=lambda x: x.lower() == "x" or (x.isdigit() and 1 <= int(x) <= len(self.inventario)),
								mensaje_raise=f"Escoge un item válido por favor .(1 - {len(self.inventario)})"
						)
						if eleccion.lower() == "x":
								return "salir"
      
						return int(eleccion) - 1

				def elegir_cantidad():
						mensaje = f"{item_comprado.getNombre()}?, buena elección\n¿Cuántas quieres llevarte?"
						cantidad = mensaje_game(
								mensaje=mensaje, 
								display=self.mostrar_inventario(),
								is_input=True,
								validacion=lambda x: x.isdigit() and int(x) > 0,
								mensaje_raise="Ingresa el numero de producto que quieres comprar"
						)
						return int(cantidad)

				def confirmar_compra():
						total = item_comprado.getPrecioCompra()*cantidad
						mensaje = f"Sería un total de {total}. ¿Deseas realizar la compra?\n(y. Sí n. Cambiar cantidad p. Cambiar producto x. Salir)"
						eleccion = mensaje_game(
								mensaje=mensaje,
								display=self.mostrar_inventario(),
								is_input=True,
								validacion=lambda x: x.lower() in ["y", "n", "p", "x"],
								mensaje_raise="Ingresa una opción válida (y, n, p, x)"
						)
						return eleccion.lower()

				estado = "producto"
				item_comprado = None
				cantidad = None

				while estado != "salir":
						if estado == "producto":
								eleccion = elegir_producto()
								if eleccion == "salir":
										estado = "salir"
										return False
        
								item_comprado = crearItem(self.inventario[eleccion][0])
								estado = "cantidad"

						elif estado == "cantidad":
								cantidad = elegir_cantidad()
								estado = "confirmar"

						elif estado == "confirmar":
								eleccion = confirmar_compra()
        
								if eleccion == "y":  # Realiza la compra
										if self.cliente.getDinero() >= item_comprado.getPrecioCompra() * cantidad:
												self.cliente.setDinero(self.cliente.getDinero() - item_comprado.getPrecioCompra() * cantidad)
												mensaje_game(self.cliente.getMochila().guardar_objeto(item_comprado, cantidad), self.mostrar_inventario())
            
												estado, eleccion, cantidad = "producto", None, None
												
										else:
												mensaje_game("No tienes suficiente dinero", self.mostrar_inventario())

								elif eleccion == "n":
										estado = "cantidad"

								elif eleccion == "p":
										estado = "producto"

								elif eleccion == "x":
										mensaje_game("Compra cancelada.", self.mostrar_inventario())
										estado = "salir"



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
				return True



		def vender(self):
				"""
				Permite al cliente vender objetos a la tienda.
				"""
				objeto = self.cliente.getMochila().abrir_mochila()

				while True:
					cantidad = mensaje_game(
									mensaje=f"¿Cuántos {objeto.getNombre()} quieres vender?\n('x' para salir)",
									display=self.mostrar_inventario(),
									is_input=True,
									validacion=lambda x: x.lower() == "x" or (x.isdigit() and int(x) > 0),
									mensaje_raise="Ingresa una cantidad válida."
					)

					if cantidad.lower() == "x":
									return False

					cantidad = int(cantidad)
					if cantidad <= 0 or not self.verificar_disponibilidad(objeto, cantidad):
									mensaje_game(f"No tienes suficientes {objeto.getNombre()} para vender", display=self.mostrar_inventario())
									continue
          
					break

				# Consulta de precio y cálculo de oferta
				consultar_precio = f"""
								SELECT precio_venta 
								FROM pokeball 
								WHERE nombre = '{objeto.getNombre()}'
								UNION 
								SELECT precio_venta 
								FROM Medicina 
								WHERE nombre = '{objeto.getNombre()}'
				"""
				precio = cursor.execute(consultar_precio).fetchone()[0]
				oferta = precio * cantidad

				# Realizar la venta y actualizar el dinero del cliente
				self.cliente.getMochila().tirar(objeto, cantidad)
				self.cliente.setDinero(self.cliente.getDinero() + oferta)

				# Mostrar mensaje de confirmación al usuario
				mensaje_game(
								mensaje=f"Has vendido {cantidad} {objeto.getNombre()}(s), has ganado {oferta}$",
								display=self.mostrar_inventario()
				)

				return False
		


		def salir(self):
				"""
				Muestra un mensaje de despedida y finaliza la interacción.
				"""
				mensaje_game("Hasta la próxima, vuelve pronto", self.mostrar_inventario())
				return True



		def recibir_jugador(self, cliente):
				"""
				Inicializa la interacción con un nuevo cliente.

				Args:
						cliente (Cliente): El cliente que entra a la tienda.
				"""
				self.cliente = cliente
				mensaje_game(f"Bienvenido a la tienda, {cliente.getNombre()}.\n¡Podrías echar un vistazo a nuestro inventario!", display=self.mostrar_inventario())
				opciones = {
						"c": self.comprar,
						"v": self.vender,
						"x": self.salir
				}
				
				while True:
					accion_tienda = mensaje_game(
       				mensaje="¿En qué puedo ayudarte?\nC. Comprar\nV. Vender\nX. Salir",
							display=self.mostrar_inventario(),
							is_input=True,
							validacion=lambda x: x.lower() in ["c","v","x"],
       				mensaje_raise="Entrada no válida. Por favor, elige una opción válida (C, V o X)."
       		)
     
					if opciones[accion_tienda.lower()]():
						return